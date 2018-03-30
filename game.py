import logic
import copy


class Game:

    def __init__(self):
        self.score = 0
        self.matrix = logic.new_game(4)
        logic.add_two(self.matrix)
        logic.add_two(self.matrix)

    def up(self):
        self.matrix, done, bonus_score = logic.up(self.matrix)
        if done:
            logic.add_two(self.matrix)
        self.score += bonus_score
        return bonus_score

    def down(self):
        self.matrix, done, bonus_score = logic.down(self.matrix)
        if done:
            logic.add_two(self.matrix)
        self.score += bonus_score
        return bonus_score

    def right(self):
        self.matrix, done, bonus_score = logic.right(self.matrix)
        if done:
            logic.add_two(self.matrix)
        self.score += bonus_score
        return bonus_score

    def left(self):
        self.matrix, done, bonus_score = logic.left(self.matrix)
        if done:
            logic.add_two(self.matrix)
        self.score += bonus_score
        return bonus_score

    def clone(self):
        return copy.deepcopy(self)

    def dump(self):
        print("score: ", self.score)
        for i in range(4):
            for j in range(4):
                print(self.matrix[i][j], "\t", end="")
            print("")
