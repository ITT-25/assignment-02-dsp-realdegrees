from collections import deque
from typing import Deque, Optional
from src.common.voice import Voice
from pynput.keyboard import Controller, Key
from scipy.stats import linregress
import numpy as np

keyboard = Controller()

class VirtualInput:
    history: Deque[Optional[float]] = deque(maxlen=60) # Length doubles as cooldown AND input window because inputs are not processed until history is full
    slope: Optional[float] = None
    
    def __init__(self, voice: Voice, sensitivity: int, verbose: bool):
        self.voice = voice
        self.verbose = verbose
        self.sensitivity = sensitivity
        
    def update(self, delta_time: float):
        self.history.append(self.voice.frequency)

        # Check if the history starts and ends with silence, meaning a short sound was detected
        is_between = self.history[0] is None and self.history[-1] is None
        stripped_history = [h for h in self.history if h is not None]
        if not is_between or len(self.history) < self.history.maxlen or len(stripped_history) == 0:
            return

        # Plot the history on a grid
        x = np.arange(len(stripped_history))
        slope, _, rvalue, _, _ = linregress(x, stripped_history)
        total_frequency_change = slope ** (len(stripped_history) - 1)
        rsquared = rvalue ** 2
        
        # Return if pearson correlation is below .8 (Filters out speech pretty well)
        # Return if the total frequency change is below a magic function value based on sensitivity (it just makes sense)
        if rsquared < 0.8 or total_frequency_change < ((10 - self.sensitivity) * 10):
            return
        
        self.slope = slope
        if self.slope > 0 and abs(self.slope) > (10 - self.sensitivity):
            keyboard.press(Key.up)
            keyboard.release(Key.up)
            self.history.clear()

        if self.slope < 0 and abs(self.slope) > (10 - self.sensitivity):
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            self.history.clear()
