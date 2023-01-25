GOAL = "G"
GAP = "0"
TILE = "1"
SWITCH = "S"
SPECIAL_SWITCH = "X"
TELEPORT_SWITCH = "T"
FALL = "F"

class Block():
    objectives = {}
    bridges = {}

    def __init__(self, start, map, type=None, end=None):
        self.current = Move(start, "", None)
        self.map = map
        self.type = type
        self.end = end
        self.projection = self.get_projection()

    def available_moves(self):
        moves = []
        for (dir, space) in self.projection.items():
            if self.is_valid(space):
                moves.append(Move(tuple(space), dir, self.current))
        return moves

    def is_valid(self, space):
        for (i, j) in space:
            if i not in range(len(self.map)) or j not in range(len(self.map[i])) or self.map[i][j] == GAP: 
                return False
        if len(space) == 1:
            ((i, j),) = space
            if self.map[i][j] == FALL:
                return False
        return True

    def is_done(self):
        return self.end in self.current.space and (len(self.current.space) == 1 or self.type[0] == SWITCH)

    def move(self, move):
        self.current = move
        self.projection = self.get_projection()

    def update(self):
        if self.type[0] == SWITCH or self.type[0] == SPECIAL_SWITCH:
            for (i, j) in Block.bridges[self.type]:
                flip = {"0": "0", "1": "1", "s": str(int(not int(self.map[i][j])))}
                self.map[i][j] = flip[self.type[1]]

        self.current.previous = None
        del Block.objectives[self.type]
        Block.objectives[self.type] = self.end

    def get_projection(self):
        spaces = {"D": [], "U": [], "R": [], "L": []}
        dirs = list(spaces)

        if len(self.current.space) == 1:
            ((i, j),) = self.current.space
            for idx, (x, y) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
                d = dirs[idx]
                spaces[d].append((i + x, j + y))
                spaces[d].append((i + 2*x, j + 2*y))
        else:
            ((i1, j1), (i2, j2)) = self.current.space
            for idx, (c, f) in enumerate(((1, max), (-1, min))):
                d1 = dirs[idx]
                d2 = dirs[idx + 2]
                if i1 == i2:
                    spaces[d1].append((i1 + c, j1))
                    spaces[d1].append((i2 + c, j2))
                    spaces[d2].append((i1, f(j1, j2) + c))
                else:
                    spaces[d2].append((i1, j1 + c))
                    spaces[d2].append((i2, j2 + c))
                    spaces[d1].append((f(i1, i2) + c, j1))
        return spaces
    
    def get_path(self):
        out = ""
        move = self.current
        while move.previous is not None:
            out += move.direction
            move = move.previous
        return out[::-1]


class Move():
    def __init__(self, space, direction, previous, block=None):
        self.space = space
        self.direction = direction
        self.previous = previous
        self.block = block

    def __eq__(self, other):
        return self.space == other.space and self.direction == other.direction
    
    def __hash__(self):
        return hash((self.space, self.direction))

class Queue():
    def __init__(self):
        self.items = []
        self.seen = set()
    
    def next(self):
        tmp = self.items[0]
        self.seen.add(tmp)
        del self.items[0]
        return tmp
    
    def add(self, new):
        for move in new:
            if move not in self.seen:
                self.items.append(move)

def solve(level):
    Block.bridges = level["bridges"]
    Block.objectives = level["objectives"]
    block = Block((level["start"],), level["map"])
    return solve_helper(block)

def solve_helper(block):
    start = block.current
    for (type, end) in Block.objectives.items():
        block.move(start)
        block.type = type
        block.end = end
        queue = Queue()
        queue.add(block.available_moves())
        while len(queue.items) > 0:
            next = queue.next()
            block.move(next)
            path = block.get_path()
            if block.is_done():
                if type == GOAL:
                    return path
                block.update()
                new_path = solve_helper(block)
                if new_path is not None:
                    return path + new_path
            queue.add(block.available_moves())

