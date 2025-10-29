import numpy as np
import pyworld as pw
from TransformLayer import TransformLayer

class ResearchLayer:
    def __init__(self, samplerate=48000, frame_length_ms=100, overlap=0.5):
        self.samplerate = samplerate
        self.frame_length = int((frame_length_ms / 1000) * samplerate)
        self.hop_length = int(self.frame_length * (1 - overlap))
        self.buffer = np.zeros(0, dtype=np.float64)
        self.frame_period = 5.0  # ms
        self.prev_tail = np.zeros(self.frame_length, dtype=np.float32)
        self.overlap = overlap

        # Transform layer
        self.transform = TransformLayer(samplerate)

    def analyze_and_synthesize(self, frame):
        # Acumula audio
        self.buffer = np.concatenate((self.buffer, frame.flatten()))

        # Si no hay suficientes muestras, devuelve una mezcla entre anterior y actual
        if len(self.buffer) < self.frame_length:
            return frame * 0.9 + self.prev_tail[:len(frame)] * 0.1

        # Toma bloque completo y deja el resto en buffer
        current_block = self.buffer[:self.frame_length]
        self.buffer = self.buffer[self.hop_length:]  # solapamiento

        # --- WORLD analysis ---
        f0, time_axis = pw.harvest(current_block, self.samplerate, frame_period=self.frame_period)
        f0 = self._smooth_f0(f0)
        sp = pw.cheaptrick(current_block, f0, time_axis, self.samplerate)
        ap = pw.d4c(current_block, f0, time_axis, self.samplerate)

        # --- Transformación de voz ---
        f0_mod, sp_mod, ap_mod = self.transform.process(f0, sp, ap)

        # --- Synth ---
        synthesized = pw.synthesize(f0_mod, sp_mod, ap_mod, self.samplerate, frame_period=self.frame_period)

        # --- Crossfade con el bloque anterior ---
        fade_len = int(self.frame_length * self.overlap)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)

        blended = np.copy(synthesized)
        blended[:fade_len] = (
            synthesized[:fade_len] * fade_in +
            self.prev_tail[:fade_len] * fade_out
        )

        # Guarda cola para siguiente mezcla
        self.prev_tail = blended[-self.frame_length:]

        # Ajuste de longitud al tamaño de salida esperado
        out = blended[:len(frame)]
        return out.astype(np.float32)

    def _smooth_f0(self, f0, alpha=0.2):
        """Filtro suavizado exponencial sobre F0."""
        smoothed = np.copy(f0)
        for i in range(1, len(f0)):
            smoothed[i] = alpha * f0[i] + (1 - alpha) * smoothed[i - 1]
        return smoothed
