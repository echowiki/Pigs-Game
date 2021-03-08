import random
import pygame

pygame.init()

RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)

size = (500, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pigs Game")

done = False

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 20)

mouse_state = 0
mouse_x = 0
mouse_y = 0

maxScore = 50
noDice = 1

gameState = -1

turn = 1

class Button():
    def __init__(self):
        self.textBoxes = {}

    # ----Clicked In----
    def clickedIn(self, x, y, width, height):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 1 and mouse_x >= x and mouse_x <= (x + width) and mouse_y >= y and mouse_y <= (y + height):
            return True

    # ----Clicked Out----
    def clickedOut(self, x, y, width, height):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 1 and mouse_x < x or mouse_state == 1 and mouse_x > (
                x + width) or mouse_state == 1 and mouse_y < y or mouse_state == 1 and mouse_y > (y + height):
            return True

    # ----Hovering----
    def hovering(self, x, y, width, height):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 0 and mouse_x >= x and mouse_x <= (x + width) and mouse_y >= y and mouse_y <= (y + height):
            return True

    # ----Click Button----
    def clickButton(self, x, y, width, height, normalColour, hoverColour, textFont, text, textColour, stateHolding=False,
                    stateVariable=0, state=1):
        if not self.clickedIn(x, y, width, height) and not self.hovering(x, y, width, height):
            pygame.draw.rect(screen, normalColour, (x, y, width, height))
        elif self.hovering(x, y, width, height):
            pygame.draw.rect(screen, hoverColour, (x, y, width, height))
        if stateHolding == True and stateVariable == state:
            pygame.draw.rect(screen, hoverColour, (x, y, width, height))
        buttonText = textFont.render(text, True, textColour)
        buttonText_x = buttonText.get_rect().width
        buttonText_y = buttonText.get_rect().height
        screen.blit(buttonText, (((x + (width / 2)) - (buttonText_x / 2)), ((y + (height / 2)) - (buttonText_y / 2))))
        if self.clickedIn(x, y, width, height):
            return True


button = Button()


def infoBar():
    global gameState
    global turn
    pygame.draw.rect(screen, GREY, (0, 0, 500, 115))
    pygame.draw.line(screen, BLACK, (0, 115), (500, 115), 4)


    if gameState == 0 or gameState == -3:
        text = font.render("GOAL: " + str(game.goal), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((250 - (text_x / 2)), (35 - (text_y / 2))))
        text = font.render("Player1 score: " + str(game.score1), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (80 - (text_y / 2))))
        text = font.render("Player2 score: " + str(game.score2), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((350 - (text_x / 2)), (80 - (text_y / 2))))
        if turn == 1:
            text = font.render("Player 1's Turn", True, BLACK)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            screen.blit(text, ((250 - (text_x / 2)), (150 - (text_y / 2))))
        else:
            text = font.render("Player 2's Turn", True, BLACK)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            screen.blit(text, ((250 - (text_x / 2)), (150 - (text_y / 2))))

        text = font.render("This round's total: " + str(game.roundT), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((250 - (text_x / 2)), (200 - (text_y / 2))))
        text = font.render(str(game.throw), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((300 - (text_x / 2)), (250 - (text_y / 2))))
    elif gameState == 1:  # p1
        text = font.render("PLAYER 1 WINS", True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))
    elif gameState == 2:  # p2
        text = font.render("PLAYER 2 WINS", True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))

    if gameState == 1 or gameState == 2:
        if button.clickButton(325, 25, 150, 50, RED, ORANGE, font, "RESET", BLACK):
            gameState = -1
            game.reset(0, 0)
    if gameState == 0:
        print("yes: ", game.roundT)
        if button.clickButton(200, 233, 80, 30, RED, ORANGE, font, "ROLL", BLACK):
            game.roll()
        if button.clickButton(210, 270, 80, 30, RED, ORANGE, font, "BANK", BLACK):
            if turn == 1:
                game.score1 += game.roundT
                if game.score1 >= game.goal:
                    gameState = 1
                else:
                    turn = 2
            else:
                game.score2 += game.roundT
                if game.score2 >= game.goal:
                    gameState = 2
                else:
                    turn = 1
            game.roundT = 0
    if gameState == -3:
        if turn == 2:
            Bot1.play()
        print("yes: ", game.roundT)
        if button.clickButton(200, 233, 80, 30, RED, ORANGE, font, "ROLL", BLACK):
            game.roll()
        elif button.clickButton(210, 270, 80, 30, RED, ORANGE, font, "BANK", BLACK):
            if turn == 1:
                game.score1 += game.roundT
                if game.score1 >= game.goal:
                    gameState = 1
                else:
                    turn = 2
            game.roundT = 0



def menu():
    global gameState
    screen.fill(GREY)
    text = font.render("PIGS", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((250 - (text_x / 2)), (100 - (text_y / 2))))
    text = font.render("GAME", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((250 - (text_x / 2)), (150 - (text_y / 2))))
    if button.clickButton(200, 250, 100, 50, RED, ORANGE, font, "SMALL", BLACK):
        game.reset(100, 1)
        gameState = 0
    if button.clickButton(200, 310, 100, 50, RED, ORANGE, font, "MEDIUM", BLACK):
        game.reset(250, 1)
        gameState = 0
    if button.clickButton(200, 370, 100, 50, RED, ORANGE, font, "LARGE", BLACK):
        game.reset(500, 2)
        gameState = 0
    if button.clickButton(200, 430, 100, 50, RED, ORANGE, font, "CUSTOM", BLACK):
        gameState = -2
    if button.clickButton(200, 490, 100, 50, RED, ORANGE, font, "AI - SIMPLE", BLACK):
        game.reset(100, 1)
        gameState = -3


def custom():
    global maxScore, noDice, gameState
    text = font.render("GOAL: " + str(maxScore), True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((225 - (text_x / 2)), (180 - (text_y / 2))))
    if button.clickButton(300, 160, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if maxScore < 1000:
            maxScore += 50
    if button.clickButton(300, 180, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if maxScore > 50:
            maxScore -= 50
    text = font.render("DICE: " + str(noDice), True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((230 - (text_x / 2)), (260 - (text_y / 2))))
    if button.clickButton(300, 240, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if noDice < 20:
            noDice += 1
    if button.clickButton(300, 260, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if noDice > 1:
            noDice -= 1
    if button.clickButton(200, 390, 100, 60, RED, ORANGE, font, "START", BLACK):
        game.reset(maxScore, noDice)
        gameState = 0


class Game:
    def __init__(self, goal, dice):
        self.goal = goal
        self.dice = dice
        self.score1 = 0
        self.score2 = 0
        self.roundT = 0
        self.throw = 0

    def roll(self):
        global turn
        num = 0
        print("hi")
        print(turn)
        for i in range(self.dice):
            num += random.randint(1, 6)
        self.throw = num
        print("roll: ", num)
        if num == game.dice:
            self.roundT = 0
            if turn == 1:
                turn = 2
            else:
                turn = 1
        else:
            self.roundT += num
            print("round T:", self.roundT)
        return self.roundT

    def turn(self, ptotal, win):
        global noDice, maxScore, turn
        self.roundT = 0
        cont = True
        while cont:
            num = self.roll()
            if num == self.dice:
                self.roundT = 0
                cont = False
            else:
                self.roundT += num
                # roll pressed
                pro = input("would you like to continue rolling y/n")
                # bank pressed
                if pro == 'n':
                    if ptotal >= maxScore:
                        cont = False
                        win = True
                    else:
                        cont = False
        ptotal += self.roundT
        return ptotal, win

    def play(self):
        global noDice, maxScore, turn, gameState
        win = False
        while not win:
            self.roundT = 0
            if turn == 1:
                if button.clickButton(325, 25, 150, 50, RED, ORANGE, font, "ROLL", BLACK):
                    pass
                if button.clickButton(325, 25, 150, 50, RED, ORANGE, font, "BANK", BLACK):
                    gameState = -1
                    game.reset(0, 0)
            self.score1, win = self.turn(self.score1, win)
            self.score2, win = self.turn(self.score2, win)

    def reset(self, goal, dice):
        global turn
        self.goal = goal
        self.dice = dice
        self.score1 = 0
        self.score2 = 0
        self.roundT = 0
        self.throw = 0
        turn = 1


class BOT1:
    global gameState, turn

    def __init__(self):
        self.hello = "hi"

    def play(self):
        global gameState, turn
        while game.roundT < 10 and turn == 2:
            game.roll()
        if turn == 2:
            game.score2 += game.roundT
            if game.score2 >= game.goal:
                gameState = 2
            else:
                turn = 1
            game.roundT = 0


Bot1 = BOT1()
game = Game(0, 0)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_state = event.button
            pygame.mouse.set_pos(mouse_x, mouse_y + 1)
        else:
            mouse_state = 0

    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    screen.fill(WHITE)

    if gameState == -1:
        menu()

    elif gameState == -2:
        custom()

    elif gameState >= 0 and gameState <= 2 or gameState == -3:
        infoBar()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
