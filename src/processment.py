import numpy as np

INT16_MIN = -32768
INT16_MAX = 32767

base_phase = 0.0


def senoidal_wave_generator(frequency: float, rate: int, chunk_size: int) -> np.ndarray:
    """Generate a sine wave for ring modulation."""
    global base_phase
    num_samples = chunk_size
    t = (np.arange(num_samples) + base_phase) / rate
    senoidal_wave = np.sin(2 * np.pi * frequency * t)
    base_phase += num_samples
    return senoidal_wave


def process_chunk(data_chunk: np.ndarray, rate: int) -> np.ndarray:
    """Apply a simple processing effect to the audio chunk."""

    # Ring modulation effect
    frequency_mod = 30.0 
    chunk_size = len(data_chunk)
    wave_modulator = senoidal_wave_generator(frequency_mod, rate, chunk_size)
    data_float = data_chunk.astype(np.float32) / INT16_MAX

    data_modulated_float = data_float * wave_modulator
    data_modulated_int = data_modulated_float * INT16_MAX
    data_final = np.clip(data_modulated_int, INT16_MIN, INT16_MAX).astype(np.int16)



    # Filters (EQ and Formantes)

    # Suavizamiento (Smoothing)

    # For demonstration, we'll just return the original chunk without processing.


    gain = 5.0
    data_final = data_final * gain
    data_final = np.clip(data_final, INT16_MIN, INT16_MAX)
   
    return data_final
    