import random
import pygame

pygame.init()

RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (145, 140, 140)
BLACK = (0, 0, 0)

size = (500, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pigs Game")

done = False

clock = pygame.time.Clock()

font = pygame.font.Font("ArialCEMTBlack.ttf", 20)

mouse_state = 0
mouse_x = 0
mouse_y = 0

gameState = -1


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
    def clickButton(self, x, y, width, height, normalColor, hoverColor, textFont, text, textColor, stateHolding=False,
                    stateVariable=0, state=1):
        if not self.clickedIn(x, y, width, height) and not self.hovering(x, y, width, height):
            pygame.draw.rect(screen, normalColor, (x, y, width, height))
        elif self.hovering(x, y, width, height):
            pygame.draw.rect(screen, hoverColor, (x, y, width, height))
        if stateHolding and stateVariable == state:
            pygame.draw.rect(screen, hoverColor, (x, y, width, height))
        buttonText = textFont.render(text, True, textColor)
        buttonText_x = buttonText.get_rect().width
        buttonText_y = buttonText.get_rect().height
        screen.blit(buttonText, (((x + (width / 2)) - (buttonText_x / 2)), ((y + (height / 2)) - (buttonText_y / 2))))
        if self.clickedIn(x, y, width, height):
            return True


button = Button()


def infoBar():
    global gameState
    pygame.draw.rect(screen, GREY, (0, 0, 500, 100))
    pygame.draw.line(screen, BLACK, (0, 100), (500, 100), 4)

    if gameState == 0:
        text = font.render("MINES: " + str(game.totalScore), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))
        text = font.render("FLAGS: " + str(game.totalScore), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((350 - (text_x / 2)), (50 - (text_y / 2))))
    elif gameState == 1:  # win
        text = font.render("YOU  WIN", True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))
    elif gameState == 2:  # loose
        text = font.render("YOU  LOOSE", True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))

    if gameState == 1 or gameState == 2:
        if button.clickButton(325, 25, 150, 50, RED, ORANGE, font, "RESET", BLACK):
            gameState = -1
            PigsGame(100)

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
    if button.clickButton(200, 250, 100, 50, RED, ORANGE, font, "EASY", BLACK):
        PigsGame(100)
        gameState = 0
    if button.clickButton(200, 310, 100, 50, RED, ORANGE, font, "MEDIUM", BLACK):
        PigsGame(200)
        gameState = 0
    if button.clickButton(200, 370, 100, 50, RED, ORANGE, font, "HARD", BLACK):
        PigsGame(300)
        gameState = 0
    if button.clickButton(200, 430, 100, 50, RED, ORANGE, font, "CUSTOM", BLACK):
        gameState = -2

'''
class PigsGUI(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.my_game = PigsGame()
    
        master.title("Pigs Game")
        master.resizable(0, 0)
        
        self.main_label = tk.Label(master, text="Pigs Game", borderwidth=2, relief="groove")
        self.main_label.grid(row=0, column=0, columnspan=3, sticky="NEWS")
        self.score_label = tk.Label(master, text="Score").grid(row=1, column=0)
        self.time_label = tk.Label(master, text="Time").grid(row=1, column=1)
        self.cur_word_label = tk.Label(master, text="Current Word").grid(row=1, column=2)
        self.show_score_label = tk.Label(master, text="0").grid(row=2, column=0)
        self.show_time_label = tk.Label(master, text="120").grid(row=2, column=1)
        self.show_word_edit = tk.Text(master).grid(row=2, column=2)
'''

maxScore = 0
noDice = 0


def custom():
    global maxScore, noDice, gameState
    text = font.render("COLUMNS: " + str(maxScore), True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((225 - (text_x / 2)), (180 - (text_y / 2))))
    if button.clickButton(300, 160, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if maxScore < 20:
            maxScore += 1
    if button.clickButton(300, 180, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if maxScore > 0:
            maxScore -= 1
    text = font.render("ROWS: " + str(noDice), True, BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((230 - (text_x / 2)), (260 - (text_y / 2))))
    if button.clickButton(300, 240, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if noDice < 20:
            noDice += 1
    if button.clickButton(300, 260, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if noDice > 0:
            noDice -= 1
    if button.clickButton(200, 390, 100, 60, RED, ORANGE, font, "START", BLACK):
        game.reset(maxScore, noDice)
        gameState = 0


class PigsGame:

    def __init__(self, totalScore):
        self.totalScore = totalScore
        self.play()

    @staticmethod
    def roll():
        num = random.randint(1, 6)
        print("you rolled a ", num)
        return num

    def turn(self, player, ptotal, win):
        turn = 0
        cont = True
        print("player", player, "is rolling")
        while cont:
            num = self.roll()
            if num == 1:
                cont = False
                print("bad dice")
                return ptotal, win
            else:
                turn += num
                print("your total for this turn is currently", turn)
                pro = input("would you like to continue rolling y/n")
                if pro == 'n':
                    ptotal += turn
                    print("player", player," currently has a total score of", ptotal)
                    if ptotal >= self.totalScore:
                        cont = False
                        print("player", player, "has won the game")
                        win = True
                    return ptotal, win

    def play(self):
        win = False
        tot1 = 0
        tot2 = 0
        print("roll to see who plays first")
        first = self.roll()
        if first <= 3:
            print("as it was lower than 4 player one begins")
            while not win:
                tot1, win = self.turn("one", tot1, win)
                tot2, win = self.turn("two", tot2, win)
        else:
            print("as it was higher than 3 player one begins")
            while not win:
                tot2, win = self.turn("two", tot2, win)
                tot1, win = self.turn("one", tot1, win)


game = PigsGame(100)

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
        menu()

    elif gameState >= 0 and gameState <= 2:
        infoBar()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
