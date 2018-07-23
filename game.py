import logic
import copy


class Game:

    def __init__(self):
        self.score = 0
        self.true_score = 0
        self.matrix = logic.new_game(4)
        self.invalid_moves = 0
        self.total_moves = 0
        logic.add_two(self.matrix)
        logic.add_two(self.matrix)

    def up(self):
        self.matrix, done, bonus_score = logic.up(self.matrix)
        self.total_moves += 1
        if done:
            logic.add_two(self.matrix)
            self.score += bonus_score
            self.true_score += bonus_score
        else:
            self.invalid_moves += 1
            self.score -=1
            bonus_score = -1
        return bonus_score

    def down(self):
        self.matrix, done, bonus_score = logic.down(self.matrix)
        self.total_moves += 1
        if done:
            logic.add_two(self.matrix)
            self.score += bonus_score
            self.true_score += bonus_score
        else:
            self.invalid_moves += 1
            self.score -=1
            bonus_score = -1
        return bonus_score

    def right(self):
        self.matrix, done, bonus_score = logic.right(self.matrix)
        self.total_moves += 1
        if done:
            logic.add_two(self.matrix)
            self.score += bonus_score
            self.true_score += bonus_score
        else:
            self.invalid_moves += 1
            self.score -= 1
            bonus_score = -1
        return bonus_score

    def left(self):
        self.matrix, done, bonus_score = logic.left(self.matrix)
        self.total_moves += 1
        if done:
            logic.add_two(self.matrix)
            self.score += bonus_score
            self.true_score += bonus_score
        else:
            self.invalid_moves += 1
            self.score -=1
            bonus_score = -1
        return bonus_score

    def clone(self):
        return copy.deepcopy(self)

    def is_over(self):
        return logic.game_state(self.matrix) == "lose"

    def move(self, move):
        if move == 0:
            return self.up()
        elif move == 1:
            return self.down()
        elif move == 2:
            return self.left()
        elif move == 3:
            return self.right()
        return -1

    def illegal_move_ratio(self):
        return float(self.invalid_moves) / float(self.total_moves)

    def largest_number(self):
        largest = 0
        for row in self.matrix:
            for element in row:
                if element > largest:
                    largest = element
        return largest

    def multi_move(self, moves):
        result = -1
        for i in range(len(moves)):
            move = moves[i]
            result = self.move(move)
            if result > 0:
                return result
        return result

    def dump(self):
        print("score: ", self.score)
        for i in range(4):
            for j in range(4):
                print(self.matrix[i][j], "\t", end="")
            print("")
