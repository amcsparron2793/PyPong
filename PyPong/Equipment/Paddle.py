from pygame import Rect, draw
class Paddle:
    def __init__(self, pong_game, x, w, h):
        self.game = pong_game
        self.x: int = x
        self.w: int = w
        self.h: int = h
        self.y: int = int(self.game.WINDOW_HEIGHT / 2 - self.h / 2)
        # creates rectangle for paddle
        self.rect = Rect(self.x, self.y, self.w, self.h)

    def draw(self) -> None:
        #Stops paddle moving too low
        if self.rect.bottom > self.game.WINDOW_HEIGHT - self.w:
            self.rect.bottom = self.game.WINDOW_HEIGHT - self.w
        #Stops paddle moving too high
        elif self.rect.top < self.w:
            self.rect.top = self.w
        #Draws paddle
        draw.rect(self.game.DISPLAY_SURF, self.game.WHITE, self.rect)

    def move(self, pos) -> None:
        self.rect.y = pos[1]
        self.draw()


class AutoPaddle(Paddle):
    def __init__(self, pong_game, x, w, h, ball, speed):
        self. game = pong_game
        super().__init__(self.game, x, w, h)
        self.ball: Ball = ball
        self.speed: int = speed

    def move(self) -> None:
        # If ball is moving away from paddle, center bat
        if self.ball.dir_x == -1:
            if self.rect.centery < int(self.game.WINDOW_HEIGHT / 2):
                self.rect.y += self.speed
            elif self.rect.centery > int(self.game.WINDOW_HEIGHT / 2):
                self.rect.y -= self.speed
        # if ball moving towards bat, track its movement.
        elif self.ball.dir_x == 1:
            if self.rect.centery < self.ball.rect.centery:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed