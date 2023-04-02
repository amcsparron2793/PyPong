"""
based around https://www.youtube.com/watch?v=3FoUs-mRnvE
and http://trevorappleton.blogspot.com/2015/04/refactoring-pong-using-object-oriented.html
"""

import pygame
import sys
from pygame.locals import *

# set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

window_width = 800  # original 400
window_height = 700  # original 300

display_surf = pygame.display.set_mode((window_width, window_height))

fps_clock = pygame.time.Clock()
fps = 40  # frames per second - default is 40


class Game:
    def __init__(self, line_thickness=10, speed=5):
        self.line_thickness: int = line_thickness
        self.speed: int = speed
        self.score: int = 0

        ball_x = int(window_width / 2 - self.line_thickness / 2)
        ball_y = int(window_height / 2 - self.line_thickness / 2)
        self.ball: Ball = Ball(ball_x, ball_y, self.line_thickness,
                               self.line_thickness, self.speed)
        self.paddles: dict = {}
        paddle_height = 50
        paddle_width = self.line_thickness
        user_paddle_x = 20
        computer_paddle_x = window_width - paddle_width - 20
        self.paddles['user'] = Paddle(user_paddle_x,
                                      paddle_width, paddle_height)
        self.paddles['computer'] = AutoPaddle(computer_paddle_x,
                                              paddle_width, paddle_height,
                                              self.ball, self.speed)
        self.scoreboard: Scoreboard = Scoreboard(0)

    def draw_arena(self) -> None:
        display_surf.fill((0, 0, 0))
        # Draw outline of arena
        pygame.draw.rect(display_surf, WHITE,
                         ((0, 0), (window_width, window_height)),
                         self.line_thickness)
        # Draw centre line
        pygame.draw.line(display_surf, WHITE,
                         (int(window_width / 2), 0),
                         (int(window_width / 2), window_height),
                         int(self.line_thickness / 4))

    def update(self) -> None:
        self.ball.move()
        self.paddles['computer'].move()

        if self.ball.hit_paddle(self.paddles['computer']):
            self.ball.bounce('x')
        elif self.ball.hit_paddle(self.paddles['user']):
            self.ball.bounce('x')
            self.score += 1
        elif self.ball.pass_computer():
            self.score += 5
        elif self.ball.pass_player():
            self.score = 0

        self.draw_arena()
        self.ball.draw()
        self.paddles['user'].draw()
        self.paddles['computer'].draw()
        self.scoreboard.display(self.score)


class Paddle:
    def __init__(self, x, w, h):
        self.x: int = x
        self.w: int = w
        self.h: int = h
        self.y: int = int(window_height / 2 - self.h / 2)
        # creates rectangle for paddle
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self) -> None:
        #Stops paddle moving too low
        if self.rect.bottom > window_height - self.w:
            self.rect.bottom = window_height - self.w
        #Stops paddle moving too high
        elif self.rect.top < self.w:
            self.rect.top = self.w
        #Draws paddle
        pygame.draw.rect(display_surf, WHITE, self.rect)

    def move(self, pos) -> None:
        self.rect.y = pos[1]
        self.draw()


class AutoPaddle(Paddle):
    def __init__(self, x, w, h, ball, speed):
        super().__init__(x, w, h)
        self.ball: Ball = ball
        self.speed: int = speed

    def move(self) -> None:
        # If ball is moving away from paddle, center bat
        if self.ball.dir_x == -1:
            if self.rect.centery < int(window_height / 2):
                self.rect.y += self.speed
            elif self.rect.centery > int(window_height / 2):
                self.rect.y -= self.speed
        # if ball moving towards bat, track its movement.
        elif self.ball.dir_x == 1:
            if self.rect.centery < self.ball.rect.centery:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed


class Ball:
    def __init__(self, x, y, w, h, speed):
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.speed: int = speed
        self.dir_x = -1  # -1 = left 1 = right
        self.dir_y = -1  # -1 = up 1 = down

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self) -> None:
        pygame.draw.rect(display_surf, WHITE, self.rect)

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
        if self.dir_y == 1 and self.rect.bottom >= window_height - self.w:
            return True
        else:
            return False

    def hit_wall(self) -> bool:
        if ((self.dir_x == -1 and self.rect.left <= self.w) or
                (self.dir_x == 1 and self.rect.right >= window_width - self.w)):
            return True
        else:
            return False

    def hit_paddle(self, paddle) -> bool:
        if pygame.sprite.collide_rect(self, paddle):
            return True
        else:
            return False

    def pass_player(self) -> bool:
        if self.rect.left <= self.w:
            return True
        else:
            return False

    def pass_computer(self) -> bool:
        if self.rect.right >= window_width - self.w:
            return True
        else:
            return False


class Scoreboard:
    def __init__(self, score=0, x=window_width-150, y=25, font_size=20):
        self.x: int = x
        self.y: int = y
        self.font: pygame.font.Font = pygame.font.Font('freesansbold.ttf', font_size)
        self.score: int = score

    def display(self, score) -> None:
        self.score = score
        result_surf = self.font.render(f'Score = {self.score}', True, WHITE)
        rect = result_surf.get_rect()
        rect.topleft = (self.x, self.y)
        display_surf.blit(result_surf, rect)


def main():
    pygame.init()
    pygame.display.set_caption("PyPong 2.0")
    pygame.mouse.set_visible(False)  # make mouse invisible

    game = Game()
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            # checks for mouse movement and moves the user paddle accordingly
            elif event.type == MOUSEMOTION:
                game.paddles['user'].move(event.pos)

        game.update()
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
