from typing import Dict, List, Literal, cast
from mido import MidiFile, Message

from note import Note

class TypeSafeMidoMessage():
    song_baseline: int = 0
    
    def __init__(self, message: Message) -> None:
        self.type: Literal["note_on", "note_off"] = cast(Literal["note_on", "note_off"], message.type)
        self.time: float = getattr(message, "time", 0)
        self.note: int = getattr(message, "note", 0)
        self.duration: float = 0
        self.velocity: int = getattr(message, "velocity", 0)
        
class Song:
    """Creates a timeline of pyglet objects to be drawn and processed sequentially on the X axis in the window."""
    # TODO: Somehow connect this to the "voice cursor" and update individual note states based on cursor position
    notes: List[Note] = []
    current_song_time: float = 0.0 # Add current_song_time
    
    def __init__(self, file: MidiFile, track: int) -> None:
        """Load and initialize the provided song"""
        self.file = file
        self.track = track
        self.current_song_time = 0.0 # Initialize current_song_time

    def init_notes(self) -> None:
        """Calculate and set the duration of each note based on the time between note_on and note_off events.
        
        Returns a list of Note objects with their duration and time set."""
        
        time = 0
        note_cache: Dict[int, float] = {}
        notes: List[TypeSafeMidoMessage] = []
        
        for msg in self.file.tracks[self.track]:
            if not hasattr(msg, "type") or not isinstance(msg, Message):
                continue
            
            note = TypeSafeMidoMessage(msg)
            note.time /= 1000  # Convert to seconds
            time += note.time
            
            if note.type == "note_on":
                note_cache[note.note] = time
            elif note.type == "note_off" and note.note in note_cache:
                start_time = note_cache.pop(note.note)
                note.duration = time - start_time
                note.time = start_time
                notes.append(note)
      
        min_time = min([note.time for note in notes])
        self.note_baseline = min([note.note for note in notes])

        for note in notes:
            note.time -= min_time
        

        
        self.notes = [Note(note.duration, note.time, note.note, self.note_baseline) for note in notes]
        
    def update(self, dt: float) -> None:
        """Updates the song's progress"""
        if len(self.notes) == 0:
            return
        
        self.current_song_time += dt
        
        # TODO: store the current voice cursor position to check against the notes
        voice_cursor_position = ...
        for note in self.notes:
            note.update_position(self.current_song_time)
            # TODO: Check for overlap with voice cursor, if overlap increase note completion
