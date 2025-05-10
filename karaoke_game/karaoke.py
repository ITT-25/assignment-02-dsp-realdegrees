import os
from mido import MidiFile
from pyglet import window, clock, app
from config import Config
import click
from song import Song
from voice import FrequencyCursor

class GameWindow(window.Window):
    def __init__(self, song: Song, cursor: FrequencyCursor):
        super().__init__(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.set_caption("Karaoke Game")
        self.set_visible(True)
        self.cursor = cursor
        self.cursor.init_cursor()
        self.song = song
        self.song.init_notes()

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
        super().on_close()
        clock.unschedule(self.on_update)
        app.exit()

@click.command()
@click.option(
    "--song", "-s", required=True, help="The name of the song you want to play", type=str
)
@click.option(
    "--track", "-t", required=False, help="The index of the track that should be used for the voice match", type=int, default=0
)
def run(song: str, track: int):
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
    voice = FrequencyCursor(song)

    win = GameWindow(song, voice)
    clock.schedule_interval(win.on_update, 1 / 60.0)
    app.run()


if __name__ == "__main__":
    run()