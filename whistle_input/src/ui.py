from typing import List
from src.config import Config
from pyglet.shapes import BorderedRectangle

class UI:
    selected: int = 0
    boxes: List[BorderedRectangle] = []
    
    def __init__(self) -> None:
        total_height = Config.NUM_BOXES * (Config.BOX_HEIGHT + Config.GAP)
        vertical_offset = (Config.WINDOW_HEIGHT - total_height) / 2
        
        for i in range(Config.NUM_BOXES):
            box = BorderedRectangle(
                x=Config.WINDOW_WIDTH / 2 - Config.BOX_WIDTH / 2,
                y=vertical_offset + i * (Config.BOX_HEIGHT + Config.GAP),
                width=Config.BOX_WIDTH,
                height=Config.BOX_HEIGHT,
                color=(255, 255, 255, 255),
                border_color=(255, 255, 255, 255),
                border=20,
                batch=Config.BATCH,
            )
            self.boxes.append(box)
            
    def update(self) -> None:
        if len(self.boxes) == 0:
            return
        
        for i in range(Config.NUM_BOXES):
            box = self.boxes[i]
            box.border_color = (0, 255, 0, 255) if i == self.selected else (255, 255, 255, 255)

    
    def increment_index(self) -> None:
        self.selected = (self.selected + 1) % Config.NUM_BOXES
    
    def decrement_index(self) -> None:
        self.selected = (self.selected - 1) % Config.NUM_BOXES
    