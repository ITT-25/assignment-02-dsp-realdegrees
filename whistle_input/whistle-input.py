from pyglet import window, clock, app
from src.config import Config
import click
from src.common.voice import Voice


from pyglet.window import key


class GameWindow(window.Window):
    def __init__(self, voice: Voice):
        super().__init__(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.set_caption("Karaoke Game")
        self.set_visible(True)
        self.voice = voice
        self.voice.start_audio_loop()

    def on_update(self, delta_time):
        self.voice.update(delta_time)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            print("UP key pressed")
        elif symbol == key.DOWN:   
            print("DOWN key pressed")
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
def run(
    verbose: bool,
):
    voice = Voice()

    win = GameWindow(voice)
    keys = key.KeyStateHandler()
    win.push_handlers(keys)

    def update(dt):
        win.on_update(dt)

        if verbose:
            frequency = voice.frequency if voice.frequency is not None else -1
            if frequency != -1:
                print(
                    f"Frequency: {frequency:.2f} Hz"
                )
            else:
                print("No frequency detected.")

    clock.schedule_interval(update, 1 / 60.0)
    app.run()


if __name__ == "__main__":
    run()
