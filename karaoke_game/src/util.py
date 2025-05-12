import numpy as np
from scipy.signal import get_window, butter, sosfilt, savgol_filter
from scipy.fft import rfft, rfftfreq

from src.config import Config


def band_pass(signal: np.ndarray, lowcut: float, highcut: float, fs: int) -> np.ndarray:
    """Apply a Butterworth bandpass filter to the data."""
    sos = butter(4, [lowcut, highcut], btype="band", fs=fs, output="sos")
    audio_filt = sosfilt(sos, signal)
    return audio_filt


def apply_window(signal: np.ndarray, window_type="hamming"):
    """Apply a windowing function to the signal."""
    window = get_window(window_type, len(signal))
    windowed_signal = signal * window
    return windowed_signal


def smooth_signal(signal: np.ndarray, window_size=64):
    """Smooth the signal using a Savitzky-Golay filter."""
    return savgol_filter(signal, window_size, polyorder=2)


def detect_frequency(signal: np.ndarray, sample_rate: int):
    """Detect the frequency of the given audio signal."""

    # Compute the FFT of the signal
    fft_spectrum = np.abs(rfft(signal))
    frequencies = rfftfreq(len(signal), d=1 / sample_rate)

    # Retrieve the major frequency
    major_idx = np.argmax(fft_spectrum)
    major_freq = frequencies[major_idx]
    return major_freq


def freq_to_midi(frequency: float) -> int:
    """Convert a frequency to a MIDI note number."""
    if frequency <= 0:
        return 0

    midi_note = 12 * np.log2(frequency / 440) + 69
    return int(round(midi_note))


def note_to_y_position(note: int, note_baseline: int) -> float:
    """Convert a MIDI note to a y-position based on the baseline."""
    # Round the note_basline to the nearest octave
    note_baseline = round(note_baseline / 12) * 12
    pitch = note % 12
    octave = note // 12 - 1
    pitch_baseline = note_baseline % 12
    octave_baseline = note_baseline // 12 - 1

    return (
        Config.BASELINE_Y
        + (pitch - pitch_baseline) * (Config.NOTE_HEIGHT + Config.NOTE_VERTICAL_GAP)
        + (octave - octave_baseline) * (Config.NOTE_HEIGHT + Config.NOTE_VERTICAL_GAP) * 12
    )
