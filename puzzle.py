from tkinter import *
from game_history import *
from random import *
from game import *
import os

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", \
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", \
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2", \
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"


class GameGrid(Frame):
    def __init__(self, machine_player_object=None):
        Frame.__init__(self)

        self.grid()
        self.master.title("Paused" if machine_player_object is not None else "2048")
        self.master.bind("<Key>", self.key_down)
        # self.gamelogic = gamelogic
        self.commands = {KEY_UP: 0, KEY_DOWN: 1, KEY_LEFT: 2, KEY_RIGHT: 3,
                         KEY_UP_ALT: 0, KEY_DOWN_ALT: 1, KEY_LEFT_ALT: 2, KEY_RIGHT_ALT: 3}
        self.pause = True
        self.machine_player_object = machine_player_object
        if self.is_machine_playing():
            self.machine_player_object.start()
        self.grid_cells = []
        self.init_grid()
        self.game = Game()
        self.history = GameHistory()

        # self.init_matrix()
        self.update_grid_cells()

        if self.is_machine_playing():
            self.machine_player_object.visual_game = self
        self.mainloop()

    def is_machine_playing(self):
        return self.machine_player_object is not None

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.game.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[2048 if new_number > 2048 else new_number],
                                                    fg=CELL_COLOR_DICT[2048 if new_number > 2048 else new_number])
        self.update_idletasks()

    def key_down(self, event):
        if self.game.is_over():
            os._exit(0)
        key = repr(event.char)
        if self.is_machine_playing():
            if key == "' '":
                self.pause = not self.pause
                self.master.title("Paused" if self.pause else "Mohsen is playing")
            return
        if key in self.commands:
            cmd = self.commands[key]
            self.move(cmd)
        else:
            print("invalid key")

    def move(self, cmd):
        matrix = self.game.matrix
        bonus_score = self.game.move(cmd)
        if bonus_score != -1:
            print("bonus score: ", bonus_score)
            self.history.add_step(matrix, cmd, bonus_score, self.game.true_score)
            self.update_grid_cells()
            if self.game.is_over():
                self.master.title("You Lose! (Score: {})".format(self.game.true_score))
                self.history.total_score = self.game.true_score
                self.history.total_moves = self.game.total_moves
                self.history.invalid_moves = self.game.invalid_moves
                if self.is_machine_playing():
                    self.history.dump_to_file("{}/{}.hxp".format(self.machine_player_object.samples_directory_name, int(time.time())))
                else:
                    self.history.dump_to_file("human_played_samples/{}.hxp".format(int(time.time())))
                print("total score:", self.game.true_score)
        else:
            print("invalid move", cmd)
        return bonus_score

    # def generate_next(self):
    #     index = (self.gen(), self.gen())
    #     while self.matrix[index[0]][index[1]] != 0:
    #         index = (self.gen(), self.gen())
    #     self.matrix[index[0]][index[1]] = 2


if __name__ == "__main__":
    gamegrid = GameGrid()
