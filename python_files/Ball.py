from pygame import Rect, draw, sprite

class Ball:
    def __init__(self, pong_game, x, y, w, h, speed):
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.speed: int = speed
        self.game = pong_game
        self.dir_x = -1  # -1 = left 1 = right
        self.dir_y = -1  # -1 = up 1 = down

        self.rect = Rect(self.x, self.y, self.w, self.h)

    def draw(self) -> None:
        draw.rect(self.game.DISPLAY_SURF, self.game.WHITE, self.rect)

    def move(self) -> None:
        self.rect.x += (self.dir_x * self.speed)
        self.rect.y += (self.dir_y * self.speed)

        # Checks for a collision with a wall, and 'bounces' ball off it.
        if self.hit_ceiling() or self.hit_floor():
            self.bounce('y')
        if self.hit_wall():
            self.bounce('x')

    def bounce(self, axis) -> None:
        if axis == 'x':
            self.dir_x *= -1
        elif axis == 'y':
            self.dir_y *= -1

    def hit_ceiling(self) -> bool:
        if self.dir_y == -1 and self.rect.top <= self.w:
            return True
        else:
            return False

    def hit_floor(self) -> bool:
        if self.dir_y == 1 and self.rect.bottom >= self.game.WINDOW_HEIGHT - self.w:
            return True
        else:
            return False

    def hit_wall(self) -> bool:
        if ((self.dir_x == -1 and self.rect.left <= self.w) or
                (self.dir_x == 1 and self.rect.right >= self.game.WINDOW_WIDTH - self.w)):
            return True
        else:
            return False

    def hit_paddle(self, paddle) -> bool:
        if sprite.collide_rect(self, paddle):
            return True
        else:
            return False

    def pass_player(self) -> bool:
        if self.rect.left <= self.w:
            return True
        else:
            return False

    def pass_computer(self) -> bool:
        if self.rect.right >= self.game.WINDOW_WIDTH - self.w:
            return True
        else:
            return False
