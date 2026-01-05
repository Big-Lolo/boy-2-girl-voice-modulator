"""
Real-time audio processing engine.
Handles pitch shifting, formant manipulation, and audio I/O.
"""
import numpy as np
import sounddevice as sd
from scipy import signal
from scipy.fft import rfft, irfft
from typing import Optional, Callable, Dict, List
from models import VoiceProfile, AudioConfig, AudioDevice
import threading
import time


class AudioProcessor:
    """Real-time audio processor with pitch and formant shifting."""
    
    def __init__(self):
        """Initialize audio processor."""
        self.config = AudioConfig()
        self.profile = VoiceProfile(name="Default")
        self.stream: Optional[sd.Stream] = None
        self.processing_enabled = False
        self.callback_function: Optional[Callable] = None
        
        # Processing parameters
        self.window_size = 2048
        self.hop_size = 512
        self.sample_rate = 48000
        
        # Buffers for overlap-add
        self.input_buffer = np.zeros(self.window_size)
        self.output_buffer = np.zeros(self.window_size)
        
        # Window function for STFT
        self.window = np.hanning(self.window_size)
        
        # Performance monitoring
        self.latency_ms = 0.0
        self.cpu_usage = 0.0
        self.last_process_time = 0.0
    
    @staticmethod
    def get_audio_devices() -> List[AudioDevice]:
        """Get list of available audio devices.
        
        Returns:
            List of AudioDevice objects
        """
        devices = []
        device_list = sd.query_devices()
        
        for idx, device in enumerate(device_list):
            devices.append(AudioDevice(
                index=idx,
                name=device['name'],
                max_input_channels=device['max_input_channels'],
                max_output_channels=device['max_output_channels'],
                default_sample_rate=device['default_samplerate']
            ))
        
        return devices
    
    def update_config(self, config: AudioConfig):
        """Update audio configuration.
        
        Args:
            config: New AudioConfig
        """
        needs_restart = (
            self.config.input_device != config.input_device or
            self.config.output_device != config.output_device or
            self.config.buffer_size != config.buffer_size or
            self.config.sample_rate != config.sample_rate
        )
        
        self.config = config
        self.sample_rate = config.sample_rate
        
        if needs_restart and self.stream is not None:
            self.stop()
            if config.enabled:
                self.start()
    
    def update_profile(self, profile: VoiceProfile):
        """Update voice modulation profile.
        
        Args:
            profile: New VoiceProfile
        """
        self.profile = profile
    
    def _pitch_shift(self, audio: np.ndarray, semitones: float) -> np.ndarray:
        """Apply pitch shifting using phase vocoder.
        
        Args:
            audio: Input audio samples
            semitones: Pitch shift in semitones
            
        Returns:
            Pitch-shifted audio
        """
        if abs(semitones) < 0.01:
            return audio
        
        # Calculate pitch shift ratio
        ratio = 2.0 ** (semitones / 12.0)
        
        # Use linear interpolation for simple pitch shifting
        # For better quality, this could be replaced with a phase vocoder
        indices = np.arange(0, len(audio), ratio)
        indices = np.clip(indices, 0, len(audio) - 1)
        
        # Interpolate
        shifted = np.interp(indices, np.arange(len(audio)), audio)
        
        # Resample to original length
        if len(shifted) != len(audio):
            shifted = signal.resample(shifted, len(audio))
        
        return shifted
    
    def _formant_shift(self, audio: np.ndarray, shift: float) -> np.ndarray:
        """Apply formant shifting using spectral envelope manipulation.
        
        Args:
            audio: Input audio samples
            shift: Formant shift multiplier (0.6-1.4)
            
        Returns:
            Formant-shifted audio
        """
        if abs(shift - 1.0) < 0.01:
            return audio
        
        # Apply FFT
        spectrum = rfft(audio * self.window)
        
        # Frequency bins
        freqs = np.fft.rfftfreq(len(audio), 1/self.sample_rate)
        
        # Shift formants by resampling spectrum
        new_freqs = freqs * shift
        new_spectrum = np.interp(freqs, new_freqs, np.abs(spectrum)) * np.exp(1j * np.angle(spectrum))
        
        # Apply inverse FFT
        shifted = irfft(new_spectrum, len(audio))
        
        return shifted
    
    def _apply_resonance(self, audio: np.ndarray, resonance: float) -> np.ndarray:
        """Apply resonance/richness to audio.
        
        Args:
            audio: Input audio samples
            resonance: Resonance percentage (0-100)
            
        Returns:
            Audio with applied resonance
        """
        if resonance < 1.0:
            return audio
        
        # Apply a simple comb filter for resonance
        resonance_amount = resonance / 100.0
        delay_samples = int(self.sample_rate * 0.01)  # 10ms delay
        
        if len(audio) > delay_samples:
            delayed = np.concatenate([np.zeros(delay_samples), audio[:-delay_samples]])
            audio = audio + (delayed * resonance_amount * 0.3)
        
        return audio
    
    def _apply_brightness(self, audio: np.ndarray, brightness_db: float) -> np.ndarray:
        """Apply brightness adjustment (high-frequency boost/cut).
        
        Args:
            audio: Input audio samples
            brightness_db: Brightness in dB (-10 to +10)
            
        Returns:
            Audio with adjusted brightness
        """
        if abs(brightness_db) < 0.1:
            return audio
        
        # Design high-shelf filter
        nyquist = self.sample_rate / 2
        cutoff = 2000  # Hz
        
        # Convert dB to linear gain
        gain = 10 ** (brightness_db / 20)
        
        # Simple high-frequency boost/cut using FFT
        spectrum = rfft(audio)
        freqs = np.fft.rfftfreq(len(audio), 1/self.sample_rate)
        
        # Create gain curve
        gain_curve = np.ones_like(freqs)
        high_freq_mask = freqs > cutoff
        gain_curve[high_freq_mask] = gain
        
        # Apply gain and inverse FFT
        spectrum *= gain_curve
        audio = irfft(spectrum, len(audio))
        
        return audio
    
    def _process_audio(self, audio: np.ndarray) -> np.ndarray:
        """Process audio with all effects.
        
        Args:
            audio: Input audio samples
            
        Returns:
            Processed audio
        """
        start_time = time.perf_counter()
        
        # Apply pitch shifting
        if abs(self.profile.pitch_shift) > 0.01:
            audio = self._pitch_shift(audio, self.profile.pitch_shift)
        
        # Apply formant shifting
        if abs(self.profile.formant_shift - 1.0) > 0.01:
            audio = self._formant_shift(audio, self.profile.formant_shift)
        
        # Apply resonance
        if self.profile.resonance > 1.0:
            audio = self._apply_resonance(audio, self.profile.resonance)
        
        # Apply brightness
        if abs(self.profile.brightness) > 0.1:
            audio = self._apply_brightness(audio, self.profile.brightness)
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0.95:
            audio = audio * (0.95 / max_val)
        
        # Calculate processing time
        process_time = (time.perf_counter() - start_time) * 1000
        self.last_process_time = process_time
        
        return audio
    
    def _audio_callback(self, indata: np.ndarray, outdata: np.ndarray, 
                       frames: int, time_info, status):
        """Callback function for audio stream.
        
        Args:
            indata: Input audio data
            outdata: Output audio buffer to fill
            frames: Number of frames
            time_info: Timing information
            status: Stream status
        """
        if status:
            print(f"Audio callback status: {status}")
        
        try:
            # Get mono input (average if stereo)
            if indata.shape[1] > 1:
                audio_input = np.mean(indata, axis=1)
            else:
                audio_input = indata[:, 0]
            
            # Process audio if enabled
            if self.processing_enabled:
                audio_output = self._process_audio(audio_input)
            else:
                audio_output = audio_input
            
            # Output to both channels if stereo
            if outdata.shape[1] > 1:
                outdata[:] = audio_output[:, np.newaxis]
            else:
                outdata[:, 0] = audio_output
            
            # Calculate latency
            if time_info.input_buffer_adc_time and time_info.output_buffer_dac_time:
                self.latency_ms = (time_info.output_buffer_dac_time - 
                                  time_info.input_buffer_adc_time) * 1000
            
        except Exception as e:
            print(f"Error in audio callback: {e}")
            outdata.fill(0)
    
    def start(self):
        """Start audio processing stream."""
        if self.stream is not None:
            self.stop()
        
        try:
            self.processing_enabled = True
            
            self.stream = sd.Stream(
                device=(self.config.input_device, self.config.output_device),
                samplerate=self.config.sample_rate,
                blocksize=self.config.buffer_size,
                channels=2,
                dtype='float32',
                callback=self._audio_callback
            )
            
            self.stream.start()
            print(f"Audio stream started: {self.config.buffer_size} buffer, {self.config.sample_rate} Hz")
            
        except Exception as e:
            print(f"Error starting audio stream: {e}")
            self.processing_enabled = False
            raise
    
    def stop(self):
        """Stop audio processing stream."""
        self.processing_enabled = False
        
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            print("Audio stream stopped")
    
    def get_status(self) -> Dict:
        """Get current processing status.
        
        Returns:
            Status dictionary
        """
        input_device_name = None
        output_device_name = None
        
        if self.config.input_device is not None:
            devices = sd.query_devices()
            if self.config.input_device < len(devices):
                input_device_name = devices[self.config.input_device]['name']
        
        if self.config.output_device is not None:
            devices = sd.query_devices()
            if self.config.output_device < len(devices):
                output_device_name = devices[self.config.output_device]['name']
        
        return {
            "enabled": self.processing_enabled,
            "latency_ms": round(self.latency_ms + self.last_process_time, 2),
            "input_device": input_device_name,
            "output_device": output_device_name,
            "cpu_usage": round(self.cpu_usage, 2)
        }
