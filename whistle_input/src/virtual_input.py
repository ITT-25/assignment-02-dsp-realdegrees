from collections import deque
from typing import Deque, Optional
from src.common.voice import Voice
from pynput.keyboard import Controller, Key

keyboard = Controller()

class VirtualInput:
    history: Deque[Optional[float]] = deque(maxlen=20)
    
    def __init__(self, voice: Voice):
        self.voice = voice
        
    def update(self, delta_time):
        self.history.append(self.voice.frequency if self.voice.frequency is not None else None)

        # TODO: Smooth out the values in history
        history_copy = [h for h in self.history if h is not None]
        
        # TODO: Detect trend based on the trend of the full history
        # Detect trend in history_copy
        if len(history_copy) > 1:
            trend = history_copy[-1] - history_copy[-2]
            if trend > 0:
                keyboard.press(Key.up)
                keyboard.release(Key.up)
            elif trend < 0:
                keyboard.press(Key.down)
                keyboard.release(Key.down)