import pyaudio

class AudioManager:
    """Class to manage audio input and output streams using PyAudio."""
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        self.p = pyaudio.PyAudio()
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.stream_in = None
        self.stream_out = None

    def open_input_stream(self):
        """Open and return an input audio stream."""
        self.stream_in = self.p.open(format=self.format,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.chunk)
        return self.stream_in

    def open_output_stream(self):
        """Open and return an output audio stream."""
        self.stream_out = self.p.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      output=True,
                                      frames_per_buffer=self.chunk)
        return self.stream_out

    def close_streams(self):
        """Close the audio streams and terminate PyAudio."""
        if self.stream_in is not None:
            self.stream_in.stop_stream()
            self.stream_in.close()
        if self.stream_out is not None:
            self.stream_out.stop_stream()
            self.stream_out.close()
        self.p.terminate()