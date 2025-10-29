import sounddevice as sd
import numpy as np
import threading
import queue

class IOAudioLayer:
    def __init__(self, samplerate=48000, blocksize=1024, channels=1, latency='low'):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.latency = latency
        
        self.input_queue = queue.Queue(maxsize=10)

        self.output_queue = queue.Queue(maxsize=10)

        self.stream = None
        self.running = False

    def _callback(self, indata, outdata, frames, time, status):
        if status:
            print(f"Stream status: {status}")

        try:
            self.input_queue.put_nowait(np.copy(indata))
        except queue.Full:
            pass

        try:
            outdata[:] = self.output_queue.get_nowait()
        except queue.Empty:
            outdata[:] = np.zeros_like(indata)

    def start(self):
        self.running = True
        self.stream = sd.Stream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            channels=self.channels,
            dtype='float32',
            latency=self.latency,
            callback=self._callback
        )
        self.stream.start()

    def stop(self):
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
    
    def get_input_block(self):
        try:
            return self.input_queue.get(timeout=0.5)
        except queue.Empty:
            return None
        
    def send_output_block(self, block):
        try:
            self.output_queue.put_nowait(block)
        except queue.Full:
            pass

