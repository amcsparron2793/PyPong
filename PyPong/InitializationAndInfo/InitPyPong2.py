from pygame import display, time, mouse, init as pg_init


class InitPyPong2:
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