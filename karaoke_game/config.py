import os
from pyglet.graphics import Batch

class Config:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    SONG_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "songs")) + os.sep
    BATCH = Batch()
    TEMPO = 1000