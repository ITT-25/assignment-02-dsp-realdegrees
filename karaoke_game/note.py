import math
from pyglet.shapes import RoundedRectangle
from config import Config

BORDER_WIDTH = 1
NOTE_HEIGHT = 25


class Note:
    """Wraps a pyglet representation of a note and holds additional song relevant metadata."""

    def __init__(self, duration: float, time: float, note: int, baseline: int) -> None:
        """Initialize the note with the provided duration and time"""
        self.completion = 0.0
        self.duration = duration
        self.time = time
        self.note = note

        x = Config.PLAY_LINE_X + (self.time * Config.PIXELS_PER_SECOND)
        width = self.duration * Config.PIXELS_PER_SECOND
        height = NOTE_HEIGHT

        # Calculate y based on the note's value relative to the baseline which ensures notes are stacked correctly
        y = Config.BASELINE_Y + (self.note - baseline) * height
        print(f"y: {y}, note: {self.note}, baseline: {baseline}")
        self.base_color = Config.BASE_NOTE_COLORS[self.note % len(Config.BASE_NOTE_COLORS)]

        self.shape_bg = RoundedRectangle(
            x=x,
            y=y,
            width=width,
            height=height,
            color=Config.DEFAULT_NOTE_COLOR,
            radius=math.pi,
            batch=Config.BATCH
        )
        self.shape_progress = RoundedRectangle(
            x=x + BORDER_WIDTH,
            y=y + BORDER_WIDTH,
            width=0,
            height=height - (BORDER_WIDTH * 2),
            color=self.base_color,
            radius=math.pi,
            batch=Config.BATCH
        )

    def update_position(self, current_song_time: float) -> None:
        """Update the note's X position and progress color based on the current song time and completion."""
        current_x_offset = (self.time - current_song_time) * Config.PIXELS_PER_SECOND
        new_x = Config.PLAY_LINE_X + current_x_offset

        self.shape_bg.x = new_x
        self.shape_progress.x = new_x + BORDER_WIDTH

        # Update progress bar width based on completion
        potential_width = self.shape_bg.width - (BORDER_WIDTH * 2) - math.pi
        self.shape_progress.width = math.pi + potential_width * self.completion

        # Interpolate color based on completion
        start_r, start_g, start_b = self.base_color
        end_r, end_g, end_b = Config.COMPLETED_NOTE_COLOR

        current_r = int(start_r + (end_r - start_r) * self.completion)
        current_g = int(start_g + (end_g - start_g) * self.completion)
        current_b = int(start_b + (end_b - start_b) * self.completion)

        self.shape_progress.color = (current_r, current_g, current_b)

    def __repr__(self):
        return f"Note(duration={self.duration}, time={self.time}, note={self.note}, completion={self.completion})\n"

