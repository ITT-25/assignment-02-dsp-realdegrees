from typing import TYPE_CHECKING
from pyglet.text import Label
from config import Config

if TYPE_CHECKING:
    from song import Song


class UI:

    def __init__(self, song: "Song"):
        self.song = song

    def init(self) -> None:
        """Initialize the UI elements."""
        self.max_score = float(sum(note.duration for note in self.song.notes))
        self.score_label = Label(
            text=self._get_score_text(),
            x=Config.WINDOW_WIDTH - 20,
            y=Config.WINDOW_HEIGHT - 20,
            font_size=24,
            color=(255, 255, 255, 255),
            batch=Config.BATCH,
            anchor_x="right",
            anchor_y="top",
        )

        self.restart_label = Label(
            text="R = Restart | ESC = Exit",
            x=Config.WINDOW_WIDTH / 2,
            y=Config.WINDOW_HEIGHT / 2,
            font_size=24,
            color=(235, 255, 235, 255),
            batch=Config.BATCH,
            anchor_x="center",
            anchor_y="center",
        )

    def _get_score(self) -> float:
        """Calculate the score based on the current song time and note completion."""
        score = 0
        for note in self.song.notes:
            if note.completion > 0:
                score += note.duration * note.completion
        return score

    def _get_score_text(self, score: float = 0) -> str:
        """Get the score text for the label."""
        return f"Score: {score:.2f}/{self.max_score:.2f}"

    def update(self) -> None:
        """Update the score label."""

        score = self._get_score()

        if self.score_label is not None:
            self.score_label.text = self._get_score_text(score)

        if self.restart_label is not None:
            completed, completed_since = self.song.is_completed() 
            self.restart_label.visible = completed and completed_since > 1 # 1 sec buffer after comletion
