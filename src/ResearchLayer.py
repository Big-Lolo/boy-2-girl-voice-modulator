import numpy as np
import pyworld as pw




class ResearchLayer:
    def __init__(self, samplerate=48000, frame_length_ms=60):
        self.samplerate = samplerate
        self.frame_length = int((frame_length_ms / 1000) *  samplerate)
        self.buffer = np.zeros(0, dtype=np.float64)

        self.frame_period = 5.0 # in ms

    def analyze_and_synthesize(self, frame):
        self.buffer = np.concatenate((self.buffer, frame.flatten()))

        if len(self.buffer) < self.frame_length:
            return frame


        current_block = self.buffer[:self.frame_length]
        self.buffer = self.buffer[self.frame_length:]

        f0, time_axis = pw.harvest(current_block, self.samplerate, frame_period=self.frame_period)
        sp = pw.cheaptrick(current_block, f0, time_axis, self.samplerate)
        ap = pw.d4c(current_block, f0, time_axis, self.samplerate)

        synthesized = pw.synthesize(f0, sp, ap, self.samplerate, frame_period=self.frame_period)

        synthesized = synthesized[:len(frame)]
        return synthesized.astype(np.float32)
    
