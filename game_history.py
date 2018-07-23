import json
import time


class GameHistory:
    def __init__(self):
        self.game_steps = []
        self.total_score = 0
        self.invalid_moves = 0
        self.total_moves = 0

    def add_step(self, matrix, move, move_score, total_score):
        self.game_steps.append(
            {
                "game_state": matrix,
                "move": move,
                "move_score": move_score,
                "total_score_after_move": total_score
            })

    def dump_to_file(self, path):
        with open(path, "w") as file:
            file.write(json.dumps(self.__dict__))
