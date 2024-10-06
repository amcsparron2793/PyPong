"""
based around https://www.youtube.com/watch?v=3FoUs-mRnvE
and http://trevorappleton.blogspot.com/2015/04/refactoring-pong-using-object-oriented.html
"""

import pygame
from pygame.locals import *
from InitializationAndInfo.InitPyPong2 import InitPyPong2
from InitializationAndInfo.Scoreboard import Scoreboard
from InitializationAndInfo.Sound import Sound

from Equipment.Paddle import Paddle, AutoPaddle
from Equipment.Ball import Ball


class Game(InitPyPong2):
    def __init__(self, line_thickness=None, speed=None):
        super().__init__()
        self.line_thickness: int = line_thickness or self.DEFAULT_LINE_THICKNESS
        self.speed: int = speed or self.DEFAULT_SPEED
        self.score: int = 0
        self.sound: Sound = Sound()

        ball_x = int(self.WINDOW_WIDTH / 2 - self.line_thickness / 2)
        ball_y = int(self.WINDOW_HEIGHT / 2 - self.line_thickness / 2)
        self.ball: Ball = Ball(self, ball_x, ball_y, self.line_thickness,
                               self.line_thickness, self.speed)

        self.paddles: dict = {}
        self.paddle_width = self.DEFAULT_PADDLE_WIDTH
        self.paddle_height = self.DEFAULT_PADDLE_HEIGHT

        user_paddle_x = 20
        computer_paddle_x = self.WINDOW_WIDTH - self.paddle_width - 20

        self.paddles['user'] = Paddle(self, x=user_paddle_x,
                                      w=self.paddle_width, h=self.paddle_height)
        self.paddles['computer'] = AutoPaddle(self, x=computer_paddle_x,
                                              w=self.paddle_width, h=self.paddle_height,
                                              ball=self.ball, speed=self.speed)
        self.scoreboard: Scoreboard = Scoreboard(self, 0)

    def draw_arena(self) -> None:
        self.DISPLAY_SURF.fill(self.BLACK)
        # Draw outline of arena
        pygame.draw.rect(self.DISPLAY_SURF, self.WHITE,
                        rect=((0, 0), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)),
                         width=self.line_thickness)
        # Draw centre line
        pygame.draw.line(self.DISPLAY_SURF, self.WHITE,
                         (int(self.WINDOW_WIDTH / 2), 0),
                         (int(self.WINDOW_WIDTH / 2), self.WINDOW_HEIGHT),
                         int(self.line_thickness / 4))

    def update(self) -> None:
        self.ball.move()
        self.paddles['computer'].move()

        if self.ball.hit_paddle(self.paddles['computer']):
            self.sound.low_beep.play()
            self.ball.bounce('x')
        elif self.ball.hit_paddle(self.paddles['user']):
            self.sound.high_beep.play()
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

    def GameLoop(self):
        while True:  # main game loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                # checks for mouse movement and moves the user paddle accordingly
                elif event.type == MOUSEMOTION:
                    self.paddles['user'].move(event.pos)

            self.update()
            pygame.display.update()
            self.FPS_CLOCK.tick(self.FPS)


if __name__ == '__main__':
    pypong = Game()
    pypong.GameLoop()
