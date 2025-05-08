import sys
from pyglet import window, clock, app
from config import Config

# TODO: add "click" for setting the song via the cli, then create a new song instance in the window class

class GameWindow(window.Window):
    def __init__(self):
        super().__init__(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.set_caption("Karaoke Game")
        self.set_visible(True)

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        self.clear()
        # TODO: draw batch

    def on_close(self):
        super().on_close()
        clock.unschedule(self.on_update)
        app.exit()
        sys.exit()


if __name__ == "__main__":
    win = GameWindow()
    clock.schedule_interval(win.on_update, 1 / 60.0)
    app.run()
