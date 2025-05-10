import numpy as np
from scipy.signal import get_window, butter, sosfilt, savgol_filter
from scipy.fft import rfft, rfftfreq

def band_pass(data: np.ndarray, lowcut: float, highcut: float, fs: int) -> np.ndarray:
    """Apply a Butterworth bandpass filter to the data."""
    sos = butter(4, [lowcut, highcut], btype='band', fs=fs, output='sos')
    audio_filt = sosfilt(sos, data)
    return audio_filt

def apply_window(signal, window_type='hamming'):
    """Apply a windowing function to the signal."""
    window = get_window(window_type, len(signal))
    windowed_signal = signal * window
    return windowed_signal

def smooth_signal(signal, window_size=5):
    """Smooth the signal using a Savitzky-Golay filter."""
    return savgol_filter(signal, window_size, polyorder=2)

def detect_frequency(signal, sample_rate):
    """Detect the frequency of the given audio signal."""

    # Compute the FFT of the signal
    fft_spectrum = np.abs(rfft(signal))
    frequencies = rfftfreq(len(signal), d=1/sample_rate)

    # Retrieve the major frequency
    major_idx = np.argmax(fft_spectrum)
    major_freq = frequencies[major_idx]
    return major_freq

def freq_to_midi(frequency: float) -> int:
    """Convert a frequency to a MIDI note number."""
    midi_note = 12 * np.log2(frequency / 440) + 69
    return int(round(midi_note))

