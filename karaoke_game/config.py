import os
from pyglet.graphics import Batch

class Config:
    SAMPLING_RATE = 1024 * 4 * 10
    BUFFER_SIZE = 1024 * 4
    
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    SONG_DIRECTORY = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "songs")) + os.sep
    BATCH = Batch()
    
    PIXELS_PER_SECOND = 150  # e.g., 1 second of music maps to 100 pixels
    PLAY_LINE_X = WINDOW_WIDTH / 2
    BASELINE_Y = 100 

    COMPLETED_NOTE_COLOR = (255, 215, 0) # Gold
    DEFAULT_NOTE_COLOR = (128, 128, 128)  # Gray
    BASE_NOTE_COLORS = [
        (0, 128, 255),  # Blue
        (255, 128, 0),  # Orange
        (128, 0, 255),  # Purple
        (0, 255, 128),  # Cyan
        (255, 0, 128),  # Magenta
        (128, 255, 0),  # Lime
    ]
