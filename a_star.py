import math
import random
import heapq


def create_square_puzzle(rows, cols):
    board = [[None] * cols for _ in range(rows)]
    i = 1
    for r in range(rows):
        for c in range(cols):
            board[r][c] = i
            i += 1
    board[rows-1][cols-1] = 0
    return SquarePuzzle(board)


class SquarePuzzle(object):

    # Required
    def __init__(self, board):
        self._board = [row[:] for row in board]
        self._row = len(board)
        self._col = len(board[0])

    def get_board(self):
        return [row[:] for row in self._board]

    def perform_move(self, direction):
        er, ec = None, None
        for r in range(self._row):
            for c in range(self._col):
                if self._board[r][c] == 0:
                    er, ec = r, c
        directions = ({"up": (-1, 0), "down": (1, 0),
                       "right": (0, 1), "left": (0, -1)})
        nr = er + directions[direction][0]
        nc = ec + directions[direction][1]
        if nr > self._row-1 or nc > self._col-1 or nr < 0 or nc < 0:
            return False
        self._board[er][ec] = self._board[nr][nc]
        self._board[nr][nc] = 0
        return True

    def scramble(self, num_moves):
        moves = ["up", "down", "right", "left"]
        for i in range(num_moves):
            move = random.choice(moves)
            while not self.perform_move(move):
                move = random.choice(moves)

    def is_solved(self):
        return (self._board ==
                create_square_puzzle(self._row, self._col).get_board())

    def copy(self):
        return SquarePuzzle([row[:] for row in self._board])

    def successors(self):
        moves = ["up", "down", "right", "left"]
        res = []
        for move in moves:
            puzzle = self.copy()
            if puzzle.perform_move(move):
                res.append((move, puzzle.get_board()))
        return res

    # Required
    def iddfs_helper(self, limit, moves, visited):
        if self.is_solved():
            yield moves
            return
        if len(moves) >= limit:
            return
        cur_state = tuple(tuple(row) for row in self._board)
        visited.add(cur_state)
        for move, board in self.successors():
            next_state = tuple(tuple(row) for row in board)
            if next_state not in visited:
                yield from (SquarePuzzle(board).
                            iddfs_helper(limit, moves+[move], visited))

    def find_solutions_iddfs(self):
        limit = 0
        while True:
            solutions = list(self.iddfs_helper(limit, [], set()))
            if solutions:
                return iter(solutions)
            limit += 1

    # Required
    def h(self):
        distance = 0
        for r in range(self._row):
            for c in range(self._col):
                value = self._board[r][c]
                if value == 0:
                    continue
                goal_r, goal_c = divmod(value-1, self._col)
                distance += abs(r - goal_r) + abs(c - goal_c)
        return distance

    def find_solution_a_star(self):
        pq = [(self.h(), 0, [], self.copy())]
        visited = set()
        while pq:
            fn, gn, moves, puzzle = heapq.heappop(pq)
            if puzzle.is_solved():
                return moves
            visited.add(tuple(tuple(row) for row in puzzle.get_board()))
            for move, board in puzzle.successors():
                tuple_board = tuple(tuple(row) for row in board)
                if tuple_board not in visited:
                    new_puzzle = SquarePuzzle(board)
                    new_f = new_puzzle.h() + gn + 1
                    heapq.heappush(pq, (new_f, gn+1, moves+[move], new_puzzle))
        return None


############################################################
# Section 2: Grid Navigation
############################################################


def grid_successor(curr, scene):
    row = len(scene)
    col = len(scene[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    r, c = curr
    res = []
    for dr, dc in directions:
        nr, nc = dr + r, dc + c
        if nr < 0 or nc < 0 or nr > row - 1 or nc > col -1 or scene[nr][nc]:
            continue
        next = (nr,nc)
        res.append(next)
    return res

def find_path(start, goal, scene):
    def het(r, c):
        return ((r-goal[0]) ** 2 + (c-goal[1]) ** 2) ** 0.5
    visited = set()
    visited.add(start)
    pq = [(het(start[0], start[1]), 0, start, [start])]
    while pq:
        fn, gn, curr, path = heapq.heappop(pq)
        if curr == goal:
            return path
        for next in grid_successor(curr, scene):
            if next not in visited:
                visited.add(next)
                cost = ((curr[0]-next[0]) ** 2 + (curr[1]-next[1]) ** 2) ** 0.5
                new_f = het(next[0], next[1]) + gn + cost
                heapq.heappush(pq,(new_f, gn + cost, next, path+[next]))
    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


def successor_move_distinct(curr_state, length):
    moves = []
    for i in range(length):
        if curr_state[i] == -1:
            continue

        if i + 1 < length and curr_state[i + 1] == -1:
            moves.append((i, i + 1))
        if (i + 2 < length
                and curr_state[i + 1] != -1
                and curr_state[i + 2] == -1):
            moves.append((i, i + 2))
        # go left
        if i - 1 >= 0 and curr_state[i - 1] == -1:
            moves.append((i, i - 1))
        if i - 2 >= 0 and curr_state[i - 1] != -1 and curr_state[i - 2] == -1:
            moves.append((i, i - 2))
    return moves

def h(state, n, length):
    distance = 0
    goal_state = [-1] * (length - n) + list(range(n - 1, -1, -1))
    for disk in range(n):
        now_pos = state.index(disk)
        goal_pos = goal_state.index(disk)
        distance += abs(goal_pos - now_pos)
    return distance

def solve_distinct_disks(length, n):
    init_state = list(range(n)) + [-1] * (length - n)
    goal_state = [-1] * (length - n) + list(range(n - 1, -1, -1))
    pq = [((length-n)*n, 0, [], init_state)]
    visited = set()
    visited.add(tuple(init_state))
    while pq:
        fn, gn, curr_move, curr_state = heapq.heappop(pq)

        if curr_state == goal_state:
            return curr_move

        for from_i, to_i in successor_move_distinct(curr_state, length):
            copy_state = curr_state[:]
            copy_state[to_i] = copy_state[from_i]
            copy_state[from_i] = -1

            tuple_state = tuple(copy_state)
            if tuple_state in visited:
                continue
            visited.add(tuple_state)

            new_h = h(copy_state, n, length)
            new_g = gn + abs(from_i - to_i)
            new_f = new_h + new_g

            copy_move = curr_move[:]
            copy_move.append((from_i, to_i))
            heapq.heappush(pq, (new_f, new_g, copy_move, copy_state))
    return None