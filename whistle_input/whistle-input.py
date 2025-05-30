from pyglet import window, clock, app
from src.config import Config
import click
from src.common.voice import Voice


from pyglet.window import key

from src.ui import UI
from src.virtual_input import VirtualInput


class GameWindow(window.Window):
    def __init__(self, voice: Voice, virtual_input: VirtualInput, demo: bool):
        super().__init__(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.set_caption("Karaoke Game")
        self.set_visible(demo)
        self.voice = voice
        self.virtual_input = virtual_input
        self.voice.start_audio_loop()
        self.ui = UI()

    def on_update(self, delta_time):
        self.virtual_input.update(delta_time)
        self.ui.update()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.ui.increment_index()
        elif symbol == key.DOWN:   
            self.ui.decrement_index()
        return super().on_key_press(symbol, modifiers)

    def on_draw(self):
        self.clear()
        Config.BATCH.draw()

    def on_resize(self, width, height):
        Config.WINDOW_WIDTH = width
        Config.WINDOW_HEIGHT = height
        return super().on_resize(width, height)

    def on_close(self):
        clock.unschedule(self.on_update)
        super().on_close()
        app.exit()


@click.command()
@click.option(
    "--verbose",
    "-v",
    required=False,
    help="Logs the captured frequency, resulting MIDI note and octave [default: False]",
    is_flag=True,
    default=False,
)
@click.option(
    "--demo",
    "-d",
    required=False,
    help="Runs the demo mode [default: False]",
    is_flag=True,
    default=False,
)
@click.option(
    "--sensitivity",
    "-s",
    required=False,
    help="Sets the sensitivity (0-10) [default: 10]",
    type=int,
    default=6,
)
def run(
    verbose: bool,
    demo: bool,
    sensitivity: int,
):
    voice = Voice()
    virtual_input = VirtualInput(voice, sensitivity, verbose)
    win = GameWindow(voice, virtual_input, demo)
    keys = key.KeyStateHandler()
    win.push_handlers(keys)

    def update(dt):
        win.on_update(dt)

        if verbose:
            frequency = f"{voice.frequency:.2f}" if voice.frequency is not None else "None"
            slope = f"{virtual_input.slope:.2f}" if virtual_input.slope is not None else "None"
            if frequency != -1:
                print(
                    f"Frequency: {frequency} Hz, Slope: {slope}"
                )

    clock.schedule_interval(update, 1 / 60.0)
    app.run()


if __name__ == "__main__":
    run()
