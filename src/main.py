import numpy as np
import time 
from IOAudioLayer import IOAudioLayer
from ResearchLayer import ResearchLayer

def main():
    audio_layer = IOAudioLayer(samplerate=48000, blocksize=3572)
    research_layer = ResearchLayer(samplerate=48000, frame_length_ms=80)

    print("Iniciando stream (Ctrl+C para parar)...")
    audio_layer.start()

    try:
        while True:
            in_block = audio_layer.get_input_block()
            if in_block is None:
                continue

            out_block = research_layer.analyze_and_synthesize(in_block)

            audio_layer.send_output_block(out_block)

    except KeyboardInterrupt:
        print("Stream detenido por el usuario...")

    finally:
        audio_layer.stop()
        print("Stream detenido.")

if __name__ == "__main__":
    main()