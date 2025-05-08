from typing import List
from mido import MidiFile

from karaoke_game.note import Note


class Song:
    """Creates a timeline of pyglet objects to be drawn and processed sequentially on the X axis in the window."""
    # TODO: Init a list of Notes that each represent a tone in the song, group the objects, move the entire group to the left on update
    # TODO: Somehow connect this to the "voice cursor" and update individual note states based on cursor position
    
    def __init__(self, file: MidiFile) -> None:
        """Load and initialize the provided song"""
        self.file = file
        self.notes: List[Note] = []
        for note in self.file.play():
            print(note)
            # TODO: Create a note object for each note in the midi file and add it to the notes group

    
    def update(self, dt: float) -> None:
        """Updates the song's progress"""
        # TODO: Progress the song by moving the notes group and forward update to each note
        pass