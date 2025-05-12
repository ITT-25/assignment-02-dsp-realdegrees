from collections import deque
from itertools import groupby
from typing import Deque, List, Optional
from src.common.voice import Voice
from pynput.keyboard import Controller, Key
from src.config import Config

keyboard = Controller()

class VirtualInput:
    history: Deque[Optional[tuple[float, float]]] = deque(maxlen=20)
    
    def __init__(self, voice: Voice, range: int, verbose: bool):
        self.voice = voice
        self.verbose = verbose
        self.range = range
        
    def update(self, delta_time: float):
        # ! dt might not be needed actually
        self.history.append((self.voice.frequency, delta_time) if self.voice.frequency is not None else None)

        # TODO: Smooth out the values in history
        history_copy = [h for h in self.history if h is not None]
        segments = self._get_history_segments(history_copy)
        
        if len(segments) < 1:
            return
        
        segment = segments[-1]
        
        if len(segment) <= 10:
            return
        
        segment_frequency_delta = segment[0][0] - segment[-1][0]
        
        # Calc the frequency range of the segment and return if the range is not within the threshold
        # Clear the history if the segment is complete and the frequency range was not matched
        frequency_range_match = abs(segment_frequency_delta) >= self.range
        if not frequency_range_match and self.voice.frequency is None:
            if self.verbose:
                print("Segment complete > Range not matched: Clearing history")
            self.history.clear()
            return
        elif not frequency_range_match:
            return
        
        # Get the sign of the frequency delta and emulate key preses accordingly
        frequency_direction = 1 if segment_frequency_delta > 0 else -1
        if frequency_direction > 0:
            keyboard.press(Key.up)
            keyboard.release(Key.up)
        elif frequency_direction < 0:
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            
        self.history.clear()
        if self.verbose:
            print("Segment complete > Range matched: Clearing history")


                
    def _get_history_segments(self, history: List[tuple[float, float]]) -> List[List[tuple[float, float]]]:
        groups = groupby(history, lambda x: x is None)
        segments = [list(group) for is_none, group in groups if not is_none]
        return segments