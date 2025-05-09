import os
from pyglet.graphics import Batch

class Config:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    SONG_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "songs")) + os.sep
    BATCH = Batch()
    PIXELS_PER_SECOND = 100  # e.g., 1 second of music maps to 100 pixels
    PLAY_LINE_X = 150  # The X-coordinate of the play line (e.g., 150px from the left)