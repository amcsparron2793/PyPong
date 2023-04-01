"""
based around https://www.youtube.com/watch?v=3FoUs-mRnvE
and http://trevorappleton.blogspot.com/2015/04/refactoring-pong-using-object-oriented.html
"""

import pygame
from pygame.locals import *


class Paddle:
    def __init__(self, x, w, h):
        self.x: int = x
        self.y: int
        self.w: int = w
        self.h: int = h

    def draw(self) -> None:
        ...

    def move(self, pos) -> None:
        ...


class AutoPaddle(Paddle):
    def __init__(self, x, w, h, ball, speed):
        super().__init__(x, w, h)
        self.ball: Ball = ball
        self.speed: int = speed

    def move(self) -> None:
        ...


class Ball:
    def __init__(self, x, y, w, h, speed):
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.speed: int = speed
        self.dir_x = -1  # -1 = left 1 = right
        self.dir_y = -1  # -1 = up 1 = down



