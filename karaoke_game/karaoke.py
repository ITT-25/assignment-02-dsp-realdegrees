import os
from mido import MidiFile
from pyglet import window, clock, app
from src.config import Config
import click
from src.ui import UI
from src.common.song import Song
from src.common.voice import FrequencyCursor


from pyglet.window import key


class GameWindow(window.Window):
    def __init__(self, song: Song, cursor: FrequencyCursor, ui: UI):
        super().__init__(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.set_caption("Karaoke Game")
        self.set_visible(True)
        self.cursor = cursor
        self.cursor.init_cursor()
        self.cursor.start_audio_loop()
        self.song = song
        self.song.init_notes()
        self.ui = ui
        self.ui.init()

    def reset(self):
        """Reset the game state."""
        self.song.reset()

    def on_update(self, delta_time):
        self.cursor.update(delta_time)
        self.song.update(delta_time)
        self.ui.update()

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
    "--song",
    "-s",
    required=True,
    help="The name of the song you want to play",
    type=str,
)
@click.option(
    "--track",
    "-t",
    required=False,
    help="The index of the track that should be used for the voice match [default: 0]",
    type=int,
    default=0,
)
@click.option(
    "--verbose",
    "-v",
    required=False,
    help="Logs the captured frequency, resulting MIDI note and octave [default: False]",
    is_flag=True,
    default=False,
)
@click.option(
    "--octave-offset",
    "-o",
    required=False,
    help="Offsets the octave of audio input by this amount (Set positive for deep voices and negative for high voices) [default: 0]",
    type=float,
    default=0,
)
@click.option(
    "--time-scale",
    "-ts",
    required=False,
    help="Sets the time scale for the audio input [default: 1]",
    type=float,
    default=1,
)
@click.option(
    "--assist",
    "-a",
    required=False,
    help="Sets the assistance level of the game, the higher the assistance level the earlier the frequency cursor will snap to the nearest note [default: 3]",
    type=int,
    default=3,
)
def run(
    song: str,
    track: int,
    verbose: bool,
    octave_offset: float,
    assist: int,
    time_scale: float,
):
    try:
        midi = MidiFile(Config.SONG_DIRECTORY + song + ".mid")
    except Exception:
        print("Unable to find the requested song.")
        available_songs = [
            f"- {file.split('.')[0]}"
            for file in os.listdir(Config.SONG_DIRECTORY)
            if file.endswith(".mid")
        ]
        print(f"Available songs:\n{chr(10).join(available_songs)}")
        return

    song = Song(midi, track, time_scale)
    voice = FrequencyCursor(song, assist, octave_offset)
    ui = UI(song)

    win = GameWindow(song, voice, ui)
    keys = key.KeyStateHandler()
    win.push_handlers(keys)

    def update(dt):
        win.on_update(dt)
        if keys[key.R]:
            win.reset()

        if verbose:
            frequency = voice.frequency if voice.frequency is not None else -1
            midi_note = voice.midi_note if voice.midi_note is not None else -1

            pitch = midi_note % 12
            octave = midi_note // 12 - 1

            if frequency != -1:
                print(
                    f"Frequency: {frequency:.2f} Hz, MIDI Note: {midi_note}, Pitch: {pitch}, Octave: {octave}"
                )

    clock.schedule_interval(update, 1 / 60.0)
    app.run()


if __name__ == "__main__":
    run()
