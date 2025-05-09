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

        x = Config.PLAY_LINE_X + (self.time * Config.PIXELS_PER_SECOND)
        width = self.duration * Config.PIXELS_PER_SECOND
        height = 10
        y = self.note * 5

        self.shape_bg = RoundedRectangle(
            x=x,
            y=y,
            width=width,
            height=height,
            color=(255, 0, 0),
            radius=math.pi,
            batch=Config.BATCH
        )
        self.shape_progress = RoundedRectangle(
            x=x + BORDER_WIDTH,
            y=y + BORDER_WIDTH,
            width=0,  # Progress width starts at 0
            height=height - (BORDER_WIDTH * 2),
            color=(0, 255, 0),
            radius=math.pi,
            batch=Config.BATCH
        )

    def update_position(self, current_song_time: float) -> None:
        """Update the note's X position based on the current song time."""
        current_x_offset = (self.time - current_song_time) * Config.PIXELS_PER_SECOND
        new_x = Config.PLAY_LINE_X + current_x_offset

        self.shape_bg.x = new_x
        self.shape_progress.x = new_x + BORDER_WIDTH

    def __repr__(self):
        return f"Note(duration={self.duration}, time={self.time}, note={self.note}, completion={self.completion})\n"
        
   