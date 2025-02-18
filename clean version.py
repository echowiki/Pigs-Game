# |------------------------------------| Initialisation |------------------------------------|
import random
import pygame

pygame.init()

RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)

d1 = pygame.image.load('d1.png')                            # this section initializes all the variables
d2 = pygame.image.load('d2.png')                            # and saves some data that will be needed later
d3 = pygame.image.load('d3.png')
d4 = pygame.image.load('d4.png')
d5 = pygame.image.load('d5.png')
d6 = pygame.image.load('d6.png')

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

roll1 = 0
roll2 = 0
roll3 = 0

bot = 1


# |------------------------------------| Button Setup |------------------------------------|


class Button:

    def __init__(self):
        self.textBoxes = {}

    # ----Clicked In----
    @staticmethod
    def clickedIn(x, y, width, height):                                     # this method checks if the button
        global mouse_state, mouse_x, mouse_y                                # is being clicked
        if mouse_state == 1 and x <= mouse_x <= (x + width) \
                and y <= mouse_y <= (y + height):
            return True

    # ----Clicked Out----
    @staticmethod
    def clickedOut(x, y, width, height):                                    # this method checks if the button
        global mouse_state, mouse_x, mouse_y                                # isn't being clicked
        if mouse_state == 1 and (mouse_x < x or mouse_x > (x + width)) \
                or mouse_state == 1 and (mouse_y < y or mouse_y > (y + height)):
            return True

    # ----Hovering----
    @staticmethod
    def hovering(x, y, width, height):                                      # this method checks if the button
        global mouse_state, mouse_x, mouse_y                                # is being hovered over
        if mouse_state == 0 and x <= mouse_x <= (x + width) \
                and y <= mouse_y <= (y + height):
            return True

    # ----Click Button----
    def clickButton(self, x, y, width, height, normalColour, hoverColour, textFont, text, textColour,
                    stateHolding=False,
                    stateVariable=0, state=1):
        if not self.clickedIn(x, y, width, height) and not self.hovering(x, y, width, height):
            pygame.draw.rect(screen, normalColour, (x, y, width, height))
        elif self.hovering(x, y, width, height):                            # this method uses the previous methods
            pygame.draw.rect(screen, hoverColour, (x, y, width, height))    # to check the state of the button and
        if stateHolding and stateVariable == state:                         # designates its look respectively and
            pygame.draw.rect(screen, hoverColour, (x, y, width, height))    # also gives an output when clicked
        buttonText = textFont.render(text, True, textColour)
        buttonText_x = buttonText.get_rect().width
        buttonText_y = buttonText.get_rect().height
        screen.blit(buttonText, (((x + (width / 2)) - (buttonText_x / 2)), ((y + (height / 2)) - (buttonText_y / 2))))
        if self.clickedIn(x, y, width, height):
            return True


# |------------------------------------| Info Bar Code |------------------------------------|


def infoBar():
    global gameState
    global turn
    pygame.draw.rect(screen, GREY, (0, 0, 500, 115))
    pygame.draw.line(screen, BLACK, (0, 115), (500, 115), 4)

    if gameState == 0 or gameState == -3 or gameState == -5:
        text = font.render("GOAL: " + str(game.goal), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((250 - (text_x / 2)), (35 - (text_y / 2))))
        if gameState == 0 or gameState == -3:
            text = font.render("Player1's score: " + str(game.score1), True, BLACK)
        else:
            text = font.render("Bot1's score: " + str(game.score1), True, BLACK)    # this section dictates the way
        text_x = text.get_rect().width                                              # the game screen looks and
        text_y = text.get_rect().height                                             # which text appears based on
        screen.blit(text, ((150 - (text_x / 2)), (80 - (text_y / 2))))              # who is playing what
        if gameState == 0:
            text = font.render("Player2's score: " + str(game.score2), True, BLACK)
        elif gameState == -3:
            text = font.render("The Bot's score: " + str(game.score2), True, BLACK)
        else:
            text = font.render("Bot2's score: " + str(game.score2), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((350 - (text_x / 2)), (80 - (text_y / 2))))
        if turn == 1:
            if gameState == 0 or gameState == -3:
                text = font.render("Player 1's Turn", True, BLACK)
            else:
                text = font.render("Bot1's Turn", True, BLACK)                      # and this decides based on
            text_x = text.get_rect().width                                          # whose turn it is
            text_y = text.get_rect().height
            screen.blit(text, ((250 - (text_x / 2)), (150 - (text_y / 2))))
        else:
            if gameState == 0:
                text = font.render("Player 2's Turn", True, BLACK)
            elif gameState == -3:
                text = font.render("The Bot's Turn", True, BLACK)
            else:
                text = font.render("Bot2's Turn", True, BLACK)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            screen.blit(text, ((250 - (text_x / 2)), (150 - (text_y / 2))))

        text = font.render("This round's total: " + str(game.roundT), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((250 - (text_x / 2)), (200 - (text_y / 2))))

        if game.dice != 2:                                              # ------------------------------
            if roll1 == 1:
                screen.blit(d1, (150, 220))
            elif roll1 == 2:
                screen.blit(d2, (150, 220))                     # this section is the code that displays
            elif roll1 == 3:                                    # the dice. it decides the number of dice to
                screen.blit(d3, (150, 220))                     # be shown and shows the correct face for what
            elif roll1 == 4:                                    # was rolled
                screen.blit(d4, (150, 220))
            elif roll1 == 5:
                screen.blit(d5, (150, 220))
            else:
                screen.blit(d6, (150, 220))
            if game.dice == 3:                                          # ------------------------------
                if roll2 == 1:
                    screen.blit(d1, (0, 220))
                elif roll2 == 2:
                    screen.blit(d2, (0, 220))
                elif roll2 == 3:
                    screen.blit(d3, (0, 220))
                elif roll2 == 4:
                    screen.blit(d4, (0, 220))
                elif roll2 == 5:
                    screen.blit(d5, (0, 220))
                else:                                                   # this bit adds the second and
                    screen.blit(d6, (0, 220))                           # third dice if there are
                if roll3 == 1:                                          # meant to be three of them
                    screen.blit(d1, (300, 220))
                elif roll3 == 2:
                    screen.blit(d2, (300, 220))
                elif roll3 == 3:
                    screen.blit(d3, (300, 220))
                elif roll3 == 4:
                    screen.blit(d4, (300, 220))
                elif roll3 == 5:
                    screen.blit(d5, (300, 220))
                else:
                    screen.blit(d6, (300, 220))
        else:                                                           # ------------------------------
            if roll1 == 1:
                screen.blit(d1, (75, 220))
            elif roll1 == 2:
                screen.blit(d2, (75, 220))
            elif roll1 == 3:
                screen.blit(d3, (75, 220))
            elif roll1 == 4:
                screen.blit(d4, (75, 220))
            elif roll1 == 5:
                screen.blit(d5, (75, 220))
            else:                                                           # and this bit shows two dice
                screen.blit(d6, (75, 220))                                  # for the two dice option
            if roll2 == 1:                                                  # i've had to do it like this
                screen.blit(d1, (225, 220))                                 # due to positioning issues
            elif roll2 == 2:                                                # so if the number of dice is
                screen.blit(d2, (225, 220))                                 # two it needs this entirely
            elif roll2 == 3:                                                # separate set of coordinates
                screen.blit(d3, (225, 220))
            elif roll2 == 4:
                screen.blit(d4, (225, 220))
            elif roll2 == 5:
                screen.blit(d5, (225, 220))
            else:
                screen.blit(d6, (225, 220))

    elif gameState == 1:  # p1                                              # ------------------------------
        text = font.render("PLAYER 1 WINS", True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height                                     # this section shows the win screens
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))      # it was easier to do them as separate
    elif gameState == 2:  # p2                                              # sections of the main game display
        text = font.render("PLAYER 2 WINS", True, BLACK)                    # rather than making an entirely new
        text_x = text.get_rect().width                                      # def statement for them because they
        text_y = text.get_rect().height                                     # are so simple
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))
    if gameState == 1 or gameState == 2:
        if button.clickButton(325, 25, 150, 50, RED, ORANGE, font, "RESET", BLACK):
            gameState = -1
            game.reset(0, 0)

    if gameState == 0:                                                      # ------------------------------
        if button.clickButton(160, 480, 80, 30, RED, ORANGE, font, "MENU", BLACK):
            gameState = -1
        if button.clickButton(260, 480, 80, 30, RED, ORANGE, font, "QUIT", BLACK):
            pygame.quit()
        if button.clickButton(160, 440, 80, 30, RED, ORANGE, font, "ROLL", BLACK):
            game.roll()
        if button.clickButton(260, 440, 80, 30, RED, ORANGE, font, "BANK", BLACK):
            if turn == 1:
                game.score1 += game.roundT
                if game.score1 >= game.goal:                            # this section is the code for what is
                    gameState = 1                                       # displayed when it is a player vs player match
                else:                                                   # and the bank score function
                    turn = 2
            else:
                game.score2 += game.roundT
                if game.score2 >= game.goal:
                    gameState = 2
                else:
                    turn = 1
            game.roundT = 0
    if gameState == -3:                                                     # ------------------------------
        if button.clickButton(160, 480, 80, 30, RED, ORANGE, font, "MENU", BLACK):
            gameState = -1
        if button.clickButton(260, 480, 80, 30, RED, ORANGE, font, "QUIT", BLACK):
            pygame.quit()
        if turn == 2:
            text = font.render("The AI is currently taking it's turn", True, BLACK)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            screen.blit(text, ((250 - (text_x / 2)), (440 - (text_y / 2))))
            if bot == 1:
                game.Bot1()                                                 # this is the code for when a player
            elif bot == 2:                                                  # faces off against a bot
                game.Bot2()
        elif turn == 1:
            if button.clickButton(160, 440, 80, 30, RED, ORANGE, font, "ROLL", BLACK):
                game.roll()
            if button.clickButton(260, 440, 80, 30, RED, ORANGE, font, "BANK", BLACK):
                if turn == 1:
                    game.score1 += game.roundT
                    if game.score1 >= game.goal:
                        gameState = 1
                    else:
                        turn = 2
                game.roundT = 0
    if gameState == -5:                                                     # ------------------------------
        if button.clickButton(160, 480, 80, 30, RED, ORANGE, font, "MENU", BLACK):
            gameState = -1
        if button.clickButton(260, 480, 80, 30, RED, ORANGE, font, "QUIT", BLACK):
            pygame.quit()
        text = font.render("the AI is currently taking it's turn", True, BLACK)
        text_x = text.get_rect().width                                              # this is the code for when
        text_y = text.get_rect().height                                             # the AIs do battle
        screen.blit(text, ((250 - (text_x / 2)), (440 - (text_y / 2))))
        if turn == 1:
            game.Bot1()
        elif turn == 2:
            game.Bot2()


# |------------------------------------| Menu Code |------------------------------------|


def menu():
    global gameState
    screen.fill(GREY)
    text = font.render("PIGS   GAME", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((250 - (text_x / 2)), (100 - (text_y / 2))))
    text = font.render("MENU", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((250 - (text_x / 2)), (150 - (text_y / 2))))         # this section of code is for which
    text = font.render("Normal Games", True, BLACK)                         # buttons are displayed on the main menu
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((150 - (text_x / 2)), (240 - (text_y / 2))))
    text = font.render("Fancy Games", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((350 - (text_x / 2)), (240 - (text_y / 2))))
    if button.clickButton(100, 260, 100, 50, RED, ORANGE, font, "SMALL", BLACK):
        game.reset(100, 1)
        gameState = 0
    if button.clickButton(100, 370, 100, 50, RED, ORANGE, font, "MEDIUM", BLACK):
        game.reset(250, 1)
        gameState = 0
    if button.clickButton(100, 480, 100, 50, RED, ORANGE, font, "LARGE", BLACK):
        game.reset(500, 2)
        gameState = 0
    if button.clickButton(300, 260, 100, 50, RED, ORANGE, font, "CUSTOM", BLACK):
        gameState = -2
    if button.clickButton(300, 370, 100, 50, RED, ORANGE, font, "AI", BLACK):
        gameState = -4
    if button.clickButton(300, 480, 100, 50, RED, ORANGE, font, "QUIT", BLACK):
        pygame.quit()


# |------------------------------------| Custom Menu Code |------------------------------------|


def custom():
    global maxScore, noDice, gameState
    screen.fill(GREY)
    text = font.render("CUSTOM MENU", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((250 - (text_x / 2)), (100 - (text_y / 2))))
    text = font.render("GOAL: " + str(maxScore), True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((225 - (text_x / 2)), (180 - (text_y / 2))))
    if button.clickButton(300, 160, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if maxScore < 1000:
            maxScore += 50
    if button.clickButton(300, 180, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if maxScore > 50:
            maxScore -= 50                                                      # this section of code is for the
    text = font.render("DICE: " + str(noDice), True, BLACK)                     # customisation options page and
    text_x = text.get_rect().width                                              # all included buttons
    text_y = text.get_rect().height
    screen.blit(text, ((230 - (text_x / 2)), (260 - (text_y / 2))))
    if button.clickButton(300, 240, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if noDice < 3:
            noDice += 1
    if button.clickButton(300, 260, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if noDice > 1:
            noDice -= 1
    if button.clickButton(200, 390, 100, 60, RED, ORANGE, font, "START", BLACK):
        game.reset(maxScore, noDice)
        gameState = 0
    if button.clickButton(210, 480, 80, 30, RED, ORANGE, font, "MENU", BLACK):
        gameState = -1
    if button.clickButton(210, 530, 80, 30, RED, ORANGE, font, "QUIT", BLACK):
        pygame.quit()


# |------------------------------------| AI Menu Code |------------------------------------|


def AI():
    global maxScore, gameState, bot
    screen.fill(GREY)
    text = font.render("AI MENU", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((250 - (text_x / 2)), (100 - (text_y / 2))))
    if button.clickButton(100, 200, 100, 50, RED, ORANGE, font, "EASY", BLACK):
        game.reset(100, 1)
        gameState = -3
        bot = 1                                                                   # this section of code is for all
    text = font.render("An easy bot to warm up on", True, BLACK)                  # options regarding AIs such as
    text_x = text.get_rect().width                                                # which one you want to fight or if
    text_y = text.get_rect().height                                               # you want to watch them battle
    screen.blit(text, ((330 - (text_x / 2)), (225 - (text_y / 2))))               # each other
    if button.clickButton(100, 300, 100, 50, RED, ORANGE, font, "HARD", BLACK):
        game.reset(100, 1)
        gameState = -3
        bot = 2
    text = font.render("Something to annoy you", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((330 - (text_x / 2)), (325 - (text_y / 2))))
    if button.clickButton(100, 400, 100, 50, RED, ORANGE, font, "AI BATTLE", BLACK):
        game.reset(100, 1)
        gameState = -5
    text = font.render("Let them fight each other", True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((330 - (text_x / 2)), (425 - (text_y / 2))))
    if button.clickButton(100, 500, 100, 50, RED, ORANGE, font, "MAIN MENU", BLACK):
        gameState = -1
    if button.clickButton(300, 500, 100, 50, RED, ORANGE, font, "QUIT", BLACK):
        pygame.quit()


# |------------------------------------| Game Logic Code + Bots |------------------------------------|


class Game:
    def __init__(self, goal, dice):
        self.goal = goal                                        # this initialises all necessary variables
        self.dice = dice                                        # for the class 'Game'
        self.score1 = 0
        self.score2 = 0
        self.roundT = 0
        self.cool_down = 500
        self.last = 0

    def roll(self):                                             # ------------------------------
        global turn, roll1, roll2, roll3
        now = pygame.time.get_ticks()
        if now - self.last >= self.cool_down:
            self.last = now
            roll1 = random.randint(1, 6)
            roll2 = random.randint(1, 6)
            roll3 = random.randint(1, 6)
            if game.dice == 1:
                num = roll1
            elif game.dice == 2:                                # this is the roll function and is
                num = roll1 + roll2                             # adaptable depending on the number
            else:                                               # of dice rolled
                num = roll1 + roll2 + roll3
            if num == game.dice:
                game.roundT = 0
                if turn == 1:
                    turn = 2
                else:
                    turn = 1
            else:
                game.roundT += num
            return game.roundT

    def Bot1(self):                                             # ------------------------------
        global gameState, turn
        x = turn
        if game.roundT >= 10 and turn == x:
            if turn == 2:
                pygame.time.delay(1000)
                game.score2 += game.roundT
                if game.score2 >= game.goal:
                    gameState = 2
                else:                                       # this is the easy bot code and is very
                    turn = 1                                # simple only holding until it has over 10
            else:                                           # score before banking. it is a decent
                pygame.time.delay(1000)                     # initial strategy but is in no way the best
                game.score1 += game.roundT
                if game.score1 >= game.goal:
                    gameState = 1
                else:
                    turn = 2
            game.roundT = 0
        elif game.roundT < 10 and turn == x:
            pygame.time.delay(1000)
            self.roll()

    def Bot2(self):                                             # ------------------------------
        global gameState, turn
        x = turn

        if game.score2 == 0 and game.roundT < 21 and turn == x:
            pygame.time.delay(1000)
            self.roll()
        elif 21 < game.score2 <= 27 and game.roundT < 20 and turn == x:
            pygame.time.delay(1000)
            self.roll()
        elif 41 <= game.score2 <= 46 and game.roundT < 19 and turn == x:
            pygame.time.delay(1000)
            self.roll()
        elif 47 <= game.score2 <= 52 and game.roundT < 17 and turn == x:
            pygame.time.delay(1000)
            self.roll()
        elif 61 <= game.score2 <= 66 and game.roundT <= 15 and turn == x:
            pygame.time.delay(1000)
            self.roll()
        elif 67 <= game.score1 <= 74 and game.roundT <= 11 and turn == x:
            pygame.time.delay(1000)
            self.roll()
        elif game.score2 >= 75 and (game.roundT + game.score2) < 100 and turn == x:
            pygame.time.delay(1000)
            self.roll()
        elif game.score1 >= 80 and game.roundT < (game.goal - game.score2) and turn == x:
            pygame.time.delay(1000)
            self.roll()

        elif turn == 2:
            pygame.time.delay(1000)                     # this is the hard bot and its strategy is to hold to
            game.score2 += game.roundT                  # varying amounts depending on how much score it has
            if game.score2 >= game.goal:                # and how much score the opponent has making it more
                gameState = 2                           # comprehensive and tougher to beat
            else:
                turn = 1
            game.roundT = 0
        elif turn == 1:
            pygame.time.delay(1000)
            game.score1 += game.roundT
            if game.score1 >= game.goal:
                gameState = 1
            else:
                turn = 2
            game.roundT = 0

    def reset(self, goal, dice):                               # ------------------------------
        global turn
        self.goal = goal
        self.dice = dice                                       # this resets the game to a fresh state so
        self.score1 = 0                                        # that when its played again there are no
        self.score2 = 0                                        # accidental left over variables from
        self.roundT = 0                                        # the previous game
        turn = 1


# |------------------------------------| Main Loop |------------------------------------|

button = Button()
game = Game(0, 0)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_state = event.button
            pygame.mouse.set_pos(mouse_x, mouse_y)
        else:
            mouse_state = 0                                     # this is the main loop of the program and
#                                                               # is what drives the display and the checking
    mouse_x = pygame.mouse.get_pos()[0]                         # of weather the buttons have been pressed
    mouse_y = pygame.mouse.get_pos()[1]                         # it sets the frame rate to 60 times a second
#                                                               # and depending on the global variable gameState
    screen.fill(WHITE)                                          # it will display a different page to the user
#                                                               # then the def statement for that page will
    if gameState == -1:                                         # set the looks of the gui and which buttons
        menu()                                                  # are available to press

    elif gameState == -2:
        custom()

    elif 0 <= gameState <= 2 or gameState == -3 or gameState == -5:
        infoBar()

    elif gameState == -4:
        AI()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
