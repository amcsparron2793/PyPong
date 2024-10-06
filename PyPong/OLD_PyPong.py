import pygame
from pygame.locals import *
#import sys

# GLOBALS

# FPS - change this to speed up or slow down the game
# default is 200
FPS = 200

WINDOWWIDTH = 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def drawArena():
    DISPLAYSURF.fill((0, 0, 0))
    # Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS)

    # draw the center line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2), 0), ((WINDOWWIDTH/2), WINDOWHEIGHT), 2)


def drawPaddle(paddle):
    # stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS

    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS

    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)


def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)


def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball


def checkEdgeCollision(ball, ballDirX, ballDirY):
    """ If the ball hits any of the edges of the window
    (ball.top, ball.bottom, ball.left, ball.right)
    then flip the balls direction."""
    if ball.top == LINETHICKNESS or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == LINETHICKNESS or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY


def checkHitBall(ball, paddle1, paddle2, ballDirX):
    """Checks if the ball has hit a paddle, and 'bounces' the ball off of it. """
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1


def checkPointScored(paddle1, ball, score, ballDirX):
    """Checks to see if a point has been scored, and returns the new score. """
    # reset points if the left wall is hit
    if ball.left == LINETHICKNESS:
        return 0
    # gain 1 point for hitting the ball
    elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        return score

    # gain 5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score

    # if no points were scored, then just return the score unchanged
    else:
        return score


def artificialIntelligence(ball, ballDirX, paddle2):
    """ not true AI, just a set of if then's."""
    # if the ball is moving away from the paddle, then center the paddle
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= 1
    # if the ball is moving towards the paddle, then track the balls movement
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2


def displayScore(score):
    resultSurf = BASICFONT.render(f'Score = {score}', True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)


def main():
    pygame.init()
    global DISPLAYSURF
    # Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('PyPong - AJM')

    # paddle and ball starting positions and inits
    ballX = WINDOWWIDTH / 2 - LINETHICKNESS / 2
    ballY = WINDOWHEIGHT / 2 - LINETHICKNESS / 2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    score = 0

    # Keeps track of ball direction
    ballDirX = -1  # -1 = left 1 = right
    ballDirY = -1  # -1 = up 1 = down

    # creates the rectangles that represent the ball and paddles
    # The X co-ordinate for paddle 2 needs to be the width of the window,
    # (WINDOWWIDTH) minus the paddle offset (PADDLEOFFSET).
    # However this would take us to the right hand side of the paddle,
    # so we also need to minus off the thickness of the paddle (LINETHICKNESS).
    # Therefore the X co-ordinate of paddle 2 would be WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    # Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    # make the mouse cursor invisible
    pygame.mouse.set_visible(False)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(paddle1, ball, score, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = artificialIntelligence(ball, ballDirX, paddle2)

        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()

