import math
from pyglet.shapes import RoundedRectangle
from config import Config


BORDER_WIDTH = 1


class Note:
    """Wraps a pyglet object and adds per note metadata"""

    def __init__(self, duration: float, time: float, note: int = 0) -> None:
        """Initialize the note with the provided duration and time"""
        self.completion = 0
        self.duration = duration
        self.time = time
        self.note = note
        print(
            f"Note created with duration: {duration}, time: {time}, note: {note}")

        self.shape_bg = RoundedRectangle(
            x=Config.WINDOW_WIDTH + time * 20,
            y=note * 5,
            width=duration * 20,
            height=10,
            color=(255, 0, 0),
            radius=math.pi,
            batch=Config.BATCH
        )
        self.shape_progress = RoundedRectangle(
            x=Config.WINDOW_WIDTH + time * 20 + BORDER_WIDTH,
            y=note * 5 + BORDER_WIDTH,
            width=0,
            height=10 - BORDER_WIDTH,
            color=(0, 255, 0),
            radius=math.pi,
            batch=Config.BATCH
        )

    def move(self, delta: float) -> None:
        """Move the note on the X axis"""
        self.shape_bg.x = self.shape_bg.x - delta * 10
        self.shape_progress.x = (self.shape_bg.x + BORDER_WIDTH)
        
    def __repr__(self):
        return f"Note(duration={self.duration}, time={self.time}, note={self.note}, completion={self.completion})\n"
        
   