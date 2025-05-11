import os
from mido import MidiFile
from pyglet import window, clock, app
from config import Config
import click
from song import Song
from voice import FrequencyCursor
from pyglet.shapes import Line

class GameWindow(window.Window):
    def __init__(self, song: Song, cursor: FrequencyCursor):
        super().__init__(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.set_caption("Karaoke Game")
        self.set_visible(True)
        self.cursor = cursor
        self.cursor.init_cursor()
        self.cursor.start_audio_loop()
        self.song = song
        self.song.init_notes()
        
        # Init Playline
        self.playline = Line(x=Config.PLAY_LINE, y=0, x2=Config.PLAY_LINE, y2=Config.WINDOW_HEIGHT, thickness=2, color=(255, 255, 255, 120), batch=Config.BATCH)

    def on_update(self, delta_time):
        self.cursor.update(delta_time)
        self.song.update(delta_time)

    def on_draw(self):
        self.clear()
        Config.BATCH.draw()
        
    def on_resize(self, width, height):
        Config.WINDOW_WIDTH = width
        Config.WINDOW_HEIGHT = height
        return super().on_resize(width, height)

    def on_close(self):
        clock.unschedule(self.on_update)
        self.cursor.close_audio_loop()
        super().on_close()
        app.exit()

@click.command()
@click.option(
    "--song", "-s", required=True, help="The name of the song you want to play", type=str
)
@click.option(
    "--track", "-t", required=False, help="The index of the track that should be used for the voice match", type=int, default=0
)
@click.option(
    "--verbose", "-v", required=False, help="Logs the captured frequency, resulting MIDI note and octave", is_flag=True, default=False
)
@click.option(
    "--octave-offset", "-o", required=False, help="Offsets the octave of audio input by this amount (Set positive for deep voices and negative for high voices)", type=float, default=0
)
def run(song: str, track: int, verbose: bool, octave_offset: float):
    try:
        midi = MidiFile(Config.SONG_DIRECTORY + song + ".mid")
    except Exception:
        print("Unable to find the requested song.")
        available_songs = [
            f"- {file.split('.')[0]}" for file in os.listdir(Config.SONG_DIRECTORY) if file.endswith(".mid")
        ]
        print(f"Available songs:\n{chr(10).join(available_songs)}")
        return
    
    song = Song(midi, track)
    voice = FrequencyCursor(song, octave_offset)

    win = GameWindow(song, voice)
    def update(dt):
        win.on_update(dt)
        if verbose:
            frequency = voice.frequency if voice.frequency is not None else -1
            midi_note = voice.midi_note if voice.midi_note is not None else -1
            
            pitch = midi_note % 12
            octave = midi_note // 12 - 1
            
            if frequency != -1:
                print(f"Frequency: {frequency:.2f} Hz, MIDI Note: {midi_note}, Pitch: {pitch}, Octave: {octave}")
            else:
                print("No frequency detected.")

    clock.schedule_interval(update, 1 / 60.0)
    app.run()


if __name__ == "__main__":
    run()