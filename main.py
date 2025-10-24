import pyaudio
import numpy as np
import time
from src.audio_manager import AudioManager
from src.processment import process_chunk


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def main_loop():
    """Loop to continuously capture and process audio data."""

    am = AudioManager(format=FORMAT, channels=CHANNELS, rate=RATE, chunk=CHUNK)
    stream_in = am.open_input_stream()
    stream_out = am.open_output_stream()

    print(" Module started. You can talk to microphone. Press Ctrl+C to stop.")

    try:
        while True:
            #First capture audio from microphone.
            data_bytes = stream_in.read(CHUNK, exception_on_overflow=False)

            #Convert byte data to numpy array to process it then.
            data_np = np.frombuffer(data_bytes, dtype=np.int16)

            #Process the audio chunk
            data_processed_np = process_chunk(data_np, RATE)

            #Convert processed numpy array back to bytes.
            data_processed_bytes = data_processed_np.astype(np.int16).tobytes()

            #Play the processed audio.
            stream_out.write(data_processed_bytes)

    except KeyboardInterrupt:
        print("\n Module stopped by user.")
    finally:
        #clean all
        am.close_streams()





if __name__ == "__main__":
    main_loop()