import os
from pyglet.graphics import Batch


class Config:
    SAMPLING_RATE = 1024 * 4 * 10
    BUFFER_SIZE = (
        1024 * 10
    )  # ! Buffer minimum 8 or jumps will happen at lower frequencies
    AMPLITUDE_THRESHOLD = 250

    SNAP_THRESHOLD = 4
    SCROLL_SPEED = 200  # Pixels per second for notes and trail

    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    SONG_DIRECTORY = (
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "songs")) + os.sep
    )
    BATCH = Batch()

    PLAY_LINE = min(500, WINDOW_WIDTH // 3)

    BASELINE_Y = WINDOW_HEIGHT // 2

    COMPLETED_NOTE_COLOR = (255, 215, 0)  # Gold
    DEFAULT_NOTE_COLOR = (128, 128, 128)  # Gray
    BASE_NOTE_COLORS = [
        (0, 128, 255),  # Blue
        (255, 128, 0),  # Orange
        (128, 0, 255),  # Purple
        (0, 255, 128),  # Cyan
        (255, 0, 128),  # Magenta
        (128, 255, 0),  # Lime
    ]
    NOTE_HEIGHT = 18
    NOTE_WIDTH_PER_SECOND = 100
