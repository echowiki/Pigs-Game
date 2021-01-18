import tkinter as tk
from random import randint


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


class PigsGame:

    def __init__(self, totalscore):
        self.p1score = 0
        self.p2score = 0
        self.totalscore = totalscore
        self.play()

    @staticmethod
    def roll():
        num = randint(1, 6)
        print("you rolled a ", num)
        return num

    def first(self):
        num = self.roll()
        if num <= 3:
            return 1
        else:
            return 2

    def bank1(self, score):
        self.p1score += score
        print("player one currently has a total score of", self.p1score)

    def bank2(self, score):
        self.p2score += score
        print("player two currently has a total score of", self.p2score)

    def p1turn(self):
        score = 0
        cont = True
        print("player one is rolling")
        while cont:
            num = self.roll()
            if num == 1:
                print("bad dice")
                return False
            else:
                score += num
                print("your total for this turn is currently", score)
                pro = input("would you like to continue rolling y/n")
                if pro == 'n':
                    self.bank1(score)
                    if self.p1score >= self.totalscore:
                        print("player one has won the game")
                    return True

    def p2turn(self):
        score = 0
        cont = True
        print("player two is rolling")
        while cont:
            num = self.roll()
            if num == 1:
                print("bad dice")
                return False
            else:
                score += num
                print("your total for this turn is currently", score)
                pro = input("would you like to continue rolling y/n")
                if pro == 'n':
                    self.bank2(score)
                    if self.p2score >= self.totalscore:
                        print("player two has won the game")
                    return True

    def play(self):
        win = False
        print("roll to see who plays first")
        first = self.first()
        if first == 1:
            print("as it was lower than 4 player one begins")
            while not win:
                win = self.p1turn()
                if not win:
                    win = self.p2turn()
        else:
            print("as it was higher than 3 player two begins")
            while not win:
                win = self.p2turn()
                if not win:
                    win = self.p1turn()


game = PigsGame(100)
