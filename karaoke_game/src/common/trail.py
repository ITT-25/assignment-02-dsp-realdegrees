from collections import deque
from itertools import groupby
from typing import Deque, List, Optional
from pyglet.shapes import MultiLine
from src.config import Config

class Trail:
    def __init__(self):
        self.segments: List[MultiLine] = []
        self.history: Deque[Optional[tuple[float, float]]] = deque(maxlen=Config.PLAY_LINE)

    def update(self, delta_time: float, cursor_active: bool, current_y: Optional[float]): # Changed: history to current_y, type to Optional[float]
        
        # Update history
        if cursor_active and current_y is not None:
            self.history.append((Config.PLAY_LINE, current_y))
        else:
            self.history.append(None)
            
        # Move history left
        for i in range(len(self.history)):
            if self.history[i] is not None:
                self.history[i] = (self.history[i][0] - Config.SCROLL_SPEED * delta_time, self.history[i][1])
        
        # Split the history into segments between None values
        self.segments = [
            MultiLine(*segment, thickness=3, color=(255, 255, 255), batch=Config.BATCH) for segment in self._get_history_segments()
        ]
        

    def _get_history_segments(self) -> List[List[tuple[float, float]]]:
        groups = groupby(self.history, lambda x: x is None)
        segments = [list(group) for is_none, group in groups if not is_none]
        return segments
