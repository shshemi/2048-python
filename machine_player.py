from puzzle import *
from threading import Thread
from multiprocessing import Process
import time
import random
import numpy as np
import math


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
            if self.play_interval > 0:
                time.sleep(self.play_interval)

    def start_playing(self):
        GameGrid(self)


class BackgroundMachinePlayer:

    def __init__(self, samples_directory_name, play_algorithm, finish_callback=None, game_id = -1):
        super().__init__()
        self.samples_directory_name = samples_directory_name
        self.play_function = play_algorithm
        self.game = Game()
        self.history = GameHistory()
        self.finish_callback = finish_callback
        self.game_id = game_id
        self.play_time = 0
        if game_id != -1:
            print("Game", game_id, "created and ready to be played")

    def run(self):
        start_time = time.time()
        if self.game_id != -1:
            print("Game", self.game_id, "started")
        while not self.game.is_over():
            matrix = self.game.matrix
            move = self.play_function(self.game.matrix)
            bonus_score = self.game.move(move)
            if bonus_score != -1:
                self.history.add_step(matrix, move, bonus_score, self.game.true_score)
        self.play_time = time.time() - start_time
        if self.game_id != -1:
            print("Game {} finished with {} moves and score {} and play time {}".format(self.game_id, self.game.total_moves, self.game.true_score, self.play_time))
        else:
            print("Game finished with {} moves and score {} and play time {}".format(self.game.total_moves, self.game.true_score, self.play_time))
        self.history.dump_to_file("{}/{}.hxp".format(self.samples_directory_name, int(time.time())))
        if self.finish_callback is not None:
            self.finish_callback()

    def start_playing_as_thread(self):
        t = Thread(target=self.run)
        t.start()
        return t

    def start_playing_as_process(self):
        p = Process(target=self.run)
        p.start()
        return p


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


# ------------------------------- A Start Playing Algorithm -------------------------------
class AStartAlgorithm:

    def __init__(self):
        self.call_count = 0

    def __call__(self, matrix, *args, **kwargs):
        self.call_count += 1
        best_move = -1
        best_score = -1
        for move in range(4):
            g = Game(matrix).clone()
            bonus = g.move(move)
            if bonus == -1:
                continue
            predicted = self.predict_score(g.matrix, 3 + int(math.log10(self.call_count)))
            if bonus + predicted > best_score:
                best_score = bonus + predicted
                best_move = move
        return best_move

    def predict_score(self, matrix, steps_to_go):
        if Game(matrix).is_over():
            return 0
        scores = []
        for move in range(4):
            g = Game(matrix).clone()
            bonus = g.move(move)
            if bonus == -1:
                continue
            if g.is_over() or steps_to_go == 0:
                scores.append(g.move(move))
            else:
                scores.append(bonus + self.predict_score(g.matrix, steps_to_go-1))
        return max(scores) if len(scores) > 0 else 0

