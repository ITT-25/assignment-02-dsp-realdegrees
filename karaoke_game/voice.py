from typing import TYPE_CHECKING, Optional, Deque
from collections import deque
import numpy as np
from pyaudio import PyAudio, paInt16
from pyglet.shapes import Circle
from config import Config
from note import NOTE_HEIGHT
from util import apply_window, detect_frequency, band_pass, freq_to_midi, smooth_signal

if TYPE_CHECKING:
    from song import Song
    
class FrequencyCursor:
    cursor: Optional[Circle] = None

    def __init__(self, song: "Song"):
        self.song = song
        self.audio = PyAudio()
        self.stream = self.audio.open(
            format=paInt16,
            channels=1,
            rate=Config.SAMPLING_RATE,
            input=True,
            frames_per_buffer=Config.BUFFER_SIZE,
            input_device_index=self._get_input_device()
        )
        self.freq_window: Deque[float] = deque(maxlen=5)

    def _get_input_device(self) -> int:
        """Get the input device index for the audio stream."""
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", self.audio.get_device_info_by_host_api_device_index(0, i).get('name'))

        print('select audio device:')
        return int(input())

    def init_cursor(self) -> None:
        self.cursor = Circle(Config.PLAY_LINE_X, 0, 10, segments=12, color=(255, 0, 0), batch=Config.BATCH)


    def frequency(self) -> float:
        """Calculate the frequency of the instance's audio stream by preprocessing/cleaning up the data and applying a fft."""
        
        # Read audio data from stream
        data = self.stream.read(Config.BUFFER_SIZE, exception_on_overflow=False)
        data = np.frombuffer(data, dtype=np.int16)
        
        # Apply audio processing pipeline
        data = band_pass(data, lowcut=80, highcut=700, fs=Config.SAMPLING_RATE)
        data = smooth_signal(data, window_size=Config.BUFFER_SIZE // 8)
        data = apply_window(data, window_type='hamming')

        # Update sliding window
        freq = detect_frequency(data, sample_rate=Config.SAMPLING_RATE)
        self.freq_window.append(freq)
        averaged_freq = sum(self.freq_window) / len(self.freq_window)

        return averaged_freq

    def update(self, delta_time: float) -> None:
        if not self.cursor:
            return

        freq = self.frequency()
        midi_note = freq_to_midi(freq)
        
        # Map frequency to y-position (example mapping, adjust as needed)
        y_position = Config.BASELINE_Y + (midi_note - self.song.note_baseline) * NOTE_HEIGHT
        print(f"y: {y_position}, note: {midi_note}, baseline: {self.song.note_baseline}")
        # Spherical linear interpolation (slerp)
        current_y = self.cursor.y
        self.cursor.y = current_y + (y_position - current_y) * min(delta_time * 5, 1)
        
    
