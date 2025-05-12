from pyglet.graphics import Batch


class Config:
    SAMPLING_RATE = 1024 * 4 * 2
    BUFFER_SIZE = (
        512 * 2
    )
    AMPLITUDE_THRESHOLD = 250

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 500
    
    BATCH = Batch()
    
    NUM_BOXES = 5
    BOX_WIDTH = 300
    BOX_HEIGHT = 80
    GAP = 10
    
    FREQUENCY_MATCH_RANGE = 150 # Hz
