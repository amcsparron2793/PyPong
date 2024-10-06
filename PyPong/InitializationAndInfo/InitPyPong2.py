from pygame import display, time, mouse, init as pg_init
from .Sound import Sound
from pygame import K_q as Q_key, K_ESCAPE as ESC_key

class _HIDEventHandler:
    def _check_keydown_events(self, event):
        if event.key == Q_key or event.key == ESC_key:
            # self.sb.write_highscore()
            # if q or esc is pressed pause the game
            self.game_active = False
            self.running = False
            if event.key == Q_key and not self.game_active:
                self.running = False
                self.show_leaderboard = False

class InitPyPong2(_HIDEventHandler):
    DEFAULT_LINE_THICKNESS = 10
    DEFAULT_SPEED = 5
    DEFAULT_FPS = 40
    DEFAULT_PADDLE_HEIGHT = 50
    DEFAULT_PADDLE_WIDTH = DEFAULT_LINE_THICKNESS

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    WINDOW_WIDTH = 800  # original 400
    WINDOW_HEIGHT = 700  # original 300

    DISPLAY_SURF = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    FPS_CLOCK = time.Clock()
    FPS = 40  # frames per second - default is 40

    def __init__(self):
        pg_init()
        display.set_caption("PyPong 2.0")
        mouse.set_visible(False)  # make mouse invisible
        self.sound: Sound = Sound()