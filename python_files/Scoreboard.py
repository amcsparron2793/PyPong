from pygame import font


class Scoreboard:
    def __init__(self,pong_game, score=0, x=None, y=25, font_size=20):
        self.game = pong_game
        self.x: int = x
        if self.x is None:
            self.x = self.game.WINDOW_WIDTH - 150
        self.y: int = y
        self.font: font.Font = font.Font('freesansbold.ttf', font_size)
        self.score: int = score

    def display(self, score) -> None:
        self.score = score
        result_surf = self.font.render(f'Score = {self.score}', True, self.game.WHITE)
        rect = result_surf.get_rect()
        rect.topleft = (self.x, self.y)
        self.game.DISPLAY_SURF.blit(result_surf, rect)