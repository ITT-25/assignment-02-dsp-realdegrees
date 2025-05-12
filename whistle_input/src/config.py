from pyglet.graphics import Batch


class Config:
    SAMPLING_RATE = 1024 * 4 * 2
    BUFFER_SIZE = (
        512 * 2
    )
    AMPLITUDE_THRESHOLD = 250

    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    
    BATCH = Batch()
