from typing import TYPE_CHECKING, Optional, Deque
from collections import deque
import numpy as np
from pyaudio import PyAudio, paInt16
from pyglet.shapes import Circle  # Line is no longer directly used here
from src.config import Config
from src.util import (
    apply_window,
    detect_frequency,
    band_pass,
    freq_to_midi,
    note_to_y_position,
    smooth_signal,
)
from src.common.trail import Trail  # Import the new Trail class

if TYPE_CHECKING:
    from src.common.song import Song
import threading


class FrequencyCursor:
    cursor: Optional[Circle] = None
    frequency: Optional[float] = None
    midi_note: Optional[int] = None
    freq_window: Deque[float] = deque(maxlen=3)

    def __init__(self, song: "Song", assist: int, octave_offset: float) -> None:
        self.song = song
        self.assist = assist
        self.octave_offset = octave_offset
        self.audio = PyAudio()
        self.trail = Trail()  # Instantiate Trail handler

        self.stream = self.audio.open(
            format=paInt16,
            channels=1,
            rate=Config.SAMPLING_RATE,
            input=True,
            frames_per_buffer=Config.BUFFER_SIZE,
            input_device_index=self._get_input_device(),
        )

        self._stop_event = threading.Event()
        self._audio_thread: Optional[threading.Thread] = None

    def start_audio_loop(self):
        """Start the audio processing thread."""
        self._stop_event.clear()
        self._audio_thread = threading.Thread(target=self._run_audio_loop)
        # Allow the main program to exit even if the thread is running
        self._audio_thread.daemon = True
        self._audio_thread.start()

    def close_audio_loop(self):
        """Stop the audio processing thread."""
        self._stop_event.set()
        if self._audio_thread:
            self._audio_thread.join()  # Wait for the thread to finish
            self._audio_thread = None

    def _run_audio_loop(self):
        """Loop to continuously read audio data from the stream."""
        while not self._stop_event.is_set():
            try:
                data = self.stream.read(Config.BUFFER_SIZE, exception_on_overflow=False)
                self._process_audio_data(data)
            except OSError as e:
                print(f"An unexpected error occurred: {e}")
                self.close_audio_loop()
                break

    def _get_input_device(self) -> int:
        """Get the input device index for the audio stream."""
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get("deviceCount")

        for i in range(0, numdevices):
            if (
                self.audio.get_device_info_by_host_api_device_index(0, i).get(
                    "maxInputChannels"
                )
            ) > 0:
                print(
                    "Input Device id ",
                    i,
                    " - ",
                    self.audio.get_device_info_by_host_api_device_index(0, i).get(
                        "name"
                    ),
                )

        print("select audio device:")
        return int(input())

    def _process_audio_data(self, raw_data: bytes) -> None:
        """Process the audio data from the stream."""

        data = np.frombuffer(raw_data, dtype=np.int16)

        # Check if the signal is too weak (no voice input)
        if np.abs(data).mean() < Config.AMPLITUDE_THRESHOLD:
            self.frequency = None
            self.midi_note = None
            return

        # Apply audio processing pipeline
        data = band_pass(data, lowcut=85, highcut=255, fs=Config.SAMPLING_RATE)
        data = smooth_signal(data, window_size=128)
        data = apply_window(data, window_type="hamming")

        # Update sliding window
        freq = detect_frequency(data, sample_rate=Config.SAMPLING_RATE)
        self.freq_window.append(freq)
        self.frequency = sum(self.freq_window) / len(self.freq_window)
        self.midi_note = freq_to_midi(self.frequency) + int(8 * self.octave_offset)

    def init_cursor(self) -> None:
        self.cursor = Circle(
            Config.PLAY_LINE,
            0,
            Config.NOTE_HEIGHT // 2,
            segments=12,
            color=(255, 255, 255),
            batch=Config.BATCH,
        )

    def update(self, delta_time: float) -> None:
        if not self.cursor or not self.frequency:
            self.cursor.x = -self.cursor.radius
            self.trail.update(delta_time, False, None)
            return
        else:
            self.cursor.x = Config.PLAY_LINE

        # Get the y position correlating to the audio frequency
        y_position = note_to_y_position(self.midi_note, self.song.note_baseline)

        # Snap the target y position to the nearest note if within a certain range
        active_note = self.song.active_note()
        if (
            active_note
            and abs(active_note.note - self.midi_note) <= self.assist
        ):
            y_position = active_note.shape_bg.y
            active_note.completion += (
                delta_time
                / active_note.duration
                * (Config.SCROLL_SPEED / Config.NOTE_WIDTH_PER_SECOND)
            )

        self.cursor.y += (y_position - self.cursor.y) * 0.2

        self.trail.update(delta_time, True, self.cursor.y)
