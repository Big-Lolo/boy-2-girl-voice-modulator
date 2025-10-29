import numpy as np
import scipy.interpolate as interp

class TransformLayer:
    def __init__(self, samplerate=48000, formant_shift=1.0, f0_shift=1.6, ap_smooth=0.9):
        self.samplerate = samplerate
        self.formant_shift = formant_shift
        self.f0_shift = f0_shift
        self.ap_smooth = ap_smooth
        
    def process(self, f0, sp, ap):
        f0_mod = f0 * self.f0_shift
        sp_mod = self._shift_formants(sp, self.formant_shift)
        ap_mod = np.power(ap, self.ap_smooth)
        
        return f0_mod, sp_mod, ap_mod
    
    def _shift_formants(self, sp, factor):
        n_frames, n_bins = sp.shape
        warped_sp = np.zeros_like(sp)

        freq_axis = np.linspace(0, 1, n_bins)
        warped_axis = np.clip(freq_axis / factor, 0, 1)
        
        for i in range(n_frames):
            interp_func = interp.interp1d(warped_axis, sp[i, :], kind='quadratic', fill_value="extrapolate")
            warped_sp[i, :] = interp_func(freq_axis)

        return warped_sp
