import tkinter as tk
from tkinter import *
import requests
from bs4 import BeautifulSoup

LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
MEDIUM_GRAY ="#808080"
GREEN = "#00CC66"
YELLOW = "#FFFF99"
RED = "#FF6666"
BLUE = "#66B2FF"
DARK_BLUE = "#000066"
PETROL_GREEN = "#66FFB2"

cells = {}

class Sudoku:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("450x752")
        self.window.resizable(0,0)
        self.window.title('S U D O K U')
        self.window.configure(background="gray")
        self.puzzle = self.get_and_populate_puzzle("1")
        self.number_buttons = self.create_number_buttons()
        self.level_nuttons = self.create_level_buttons()
        self.play_buttons = self.create_play_buttons () 
        self.grid = []
        self.board = []

    # Web scraping Sudoku board initializing numbers from https://nine.websudoku.com:
    def get_and_populate_puzzle(self, difficulty):
        # Difficulty passed in as string with one digit. 1-4
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(difficulty)).content
        soup = BeautifulSoup(html_doc, 'html.parser')
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f10', 'f11', 'f12', 'f13', 
        'f14', 'f15', 'f16', 'f17', 'f18', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 
        'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f40', 'f41', 'f42', 'f43', 'f44', 
        'f45', 'f46', 'f47', 'f48', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f60', 
        'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 
        'f76', 'f77', 'f78', 'f80', 'f81', 'f82', 'f83', 'f84', 'f85', 'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))
        #print(data)
        board = [[0 for x in range (9)] for x in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index//9][index%9] = int(cell['value'])
                #print(board[index//9][index%9]) # Numbers from dudoku starting game
            except:
                pass
        #print (board)
        # CREATE NESTED LIST (9 LISTS WITH 9 ELEMENTS):
        self.grid = board
        #print(board)

        # Draw grid 9x9 of 81 entry widgets:   
        for column in range (9):
            for row in range (9):
                color = LIGHT_BLUE
                def ValidateNumber(P):
                    out = (P.isdigit() or P == "") and len(P) < 2
                    return out
                reg = self.window.register(ValidateNumber)
                e = tk.IntVar()
                if board[row][column] == 0:
                    e.set("")
                else:
                    e.set(board[row][column])
                entry = Entry(self.window, textvariable=e, width = 3, bg=color, justify="center", font=('Arial', 20, 'bold'), validate="key", validatecommand=(reg, "%P")) # STATE = DISABLE (for restriction to change content)
                entry.grid(row=row+1, column=column+1, sticky=NSEW, padx=1, pady=1, ipady=5)
                 #if board[row][column] == 0:
                    #entry.config(state='normal')
                #else:
                    #entry.config(state='readonly')
                entry.config(state='normal' if board[row][column] == 0 else 'readonly') # Using ARGS to write it shorter
                entry.config(readonlybackground=LIGHT_GRAY, foreground=DARK_BLUE if board[row][column] != 0 else LIGHT_BLUE and 'black')
                cells[(row+1, column+1)] = e

    def create_number_buttons(self):
        for i in range (1,10,10):
            for j in range (1,10):
                btn = Button(self.window, width=2, height=3, text=j, highlightcolor=MEDIUM_GRAY, justify="center", font=('Arial', 15, 'bold'))
                btn.grid(row=10, column=j-1+1, sticky="nsew", padx=1, pady=1, ipadx=5)

    def create_level_buttons(self):
        level_easy = Button(self.window, width=6, height=3, text="EASY", highlightbackground=GREEN, justify="center", font=('Arial', 20, 'bold'))
        level_easy.grid(row=13, column=1, sticky="nsew", padx=1, pady=1, ipadx=5, columnspan=3)               
        level_medium = Button(self.window, width=6, height=3, text="MEDIUM", highlightbackground=YELLOW, justify="center", font=('Arial', 20, 'bold'))
        level_medium.grid(row=13, column=4, sticky="nsew", padx=1, pady=1, ipadx=5, columnspan=3) 
        level_hard = Button(self.window, width=6, height=3, text="HARD", highlightbackground=RED, justify="center", font=('Arial', 20, 'bold'))
        level_hard.grid(row=13, column=7, sticky="nsew", padx=1, pady=1, ipadx=5, columnspan=3) 

    def create_play_buttons (self):
        level_easy = Button(self.window, width=9, height=4, text="CHECK", highlightbackground=BLUE, justify="center", font=('Arial', 20, 'bold'))
        level_easy.grid(row=14, column=1, sticky="nsew", padx=1, pady=1, ipadx=5, columnspan=9)               
        level_medium = Button(self.window, width=9, height=4, text="SOLVE", highlightbackground=PETROL_GREEN, justify="center", font=('Arial', 20, 'bold'))
        level_medium.grid(row=15, column=1, sticky="nsew", padx=1, pady=1, ipadx=5, columnspan=9) 

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    sudoku = Sudoku()
    sudoku.run()