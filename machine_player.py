from puzzle import *
from threading import Thread
import time
import random
import numpy as np


# -------------------------------  Machine Players -------------------------------
class VisualMachinePlayer(Thread):
    def __init__(self, samples_directory_name, play_algorithm, play_interval=0.5):
        super().__init__()
        self.samples_directory_name = samples_directory_name
        self.play_function = play_algorithm
        self.play_interval = play_interval
        self.visual_game = None

    def run(self):
        print("Player thread started")
        while self.visual_game is None:
            time.sleep(1)
        while not self.visual_game.game.is_over():
            move = self.play_function(self.visual_game.game.matrix)
            self.visual_game.move(move)
            time.sleep(self.play_interval)

    def start_playing(self):
        GameGrid(self)


class BackgroundMachinePlayer(Thread):
    def __init__(self, samples_directory_name, play_algorithm):
        super().__init__()
        self.samples_directory_name = samples_directory_name
        self.play_function = play_algorithm
        self.game = Game()
        self.history = GameHistory()

    def run(self):
        while not self.game.is_over():
            matrix = self.game.matrix
            move = self.play_function(self.game.matrix)
            bonus_score = self.game.move(move)
            if bonus_score != -1:
                self.history.add_step(matrix, move, bonus_score, self.game.true_score)
        print("Game finished with {} moves and score {}".format(self.game.total_moves, self.game.true_score))
        self.history.dump_to_file("{}/{}.hxp".format(self.samples_directory_name, int(time.time())))

    def start_playing(self):
        self.start()


# ------------------------------- Machine Playing Algorithm -------------------------------
class UniformRandomAlgorithm:
    def __call__(self, *args, **kwargs):
        return random.randint(0, 3)


class DownLeftRightUpAlgorithm:
    def __init__(self):
        self.last_state = None
        self.last_decision = -1

    def next_decision(self):
        if self.last_decision == -1:
            return 1
        elif self.last_decision == 1:
            return 2
        elif self.last_decision == 2:
            return 3
        elif self.last_decision == 3:
            return 0
        return -1

    def __call__(self, matrix, *args, **kwargs):
        current_state = np.array(matrix)
        if (current_state == self.last_state).all():
            self.last_decision = self.next_decision()
        else:
            self.last_decision = 1
        self.last_state = current_state
        return self.last_decision


if __name__ == "__main__":
    # unirand = UniformRandomAlgorithm()
    dlru = DownLeftRightUpAlgorithm()
    # player = BackgroundMachinePlayer("dlru_played_samples", dlru)
    player = VisualMachinePlayer("dlru_played_samples", dlru)
    player.start_playing()
