import sys

# Instances of the Node class is used to represent coordinates of the maze
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# Uses a single path until it hits a dead end or finds the solution
class DepthFirstSearch():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        """ Add a node to the frontier """

        self.frontier.append(node)

    def contains_state(self, state):
        """ Checks to see if a state is in the frontier """

        return any(node.state == state for node in self.frontier)

    def empty(self):
        """ Makes sure the frontier is not empty """

        return len(self.frontier) == 0

    def remove(self):
        """ Picks a node from the frontier one at a time if the frontier is not empty """

        if not self.empty(): 
            return self.frontier.pop(-1)
        
        raise Exception("empty frontier")
            

# Explore all the paths it meets it that path hits a dead end or reaches the goal
class BreathFirstSearch(DepthFirstSearch):
    def remove(self):
        if not self.empty(): 
            return self.frontier.pop(0)
        
        raise Exception("empty frontier")
            

# Explores path that are closer to the goal anytime it has to choose coordinates to explore next
class GreedyBestFirstSearch(DepthFirstSearch):
    def __init__(self, goal):
        self.goal = goal
        self.frontier = {}
        self.currentMinTuple = (0, 0)

    def estimate_from_goal(self):
        """ Gives the estimated distance of the current state from the goal """

        currentMinValue = float('inf')

        # Finds the distance of every coordinate away from the goal
        for key in self.frontier:
            goalRow, goalCol = self.goal
            stateRow, stateCol = key

            currentValue = abs(goalRow - stateRow) + abs(goalCol - stateCol)

            if currentValue < currentMinValue:
                currentMinValue = currentValue
                self.currentMinTuple = key
        
        return self.currentMinTuple

    def add(self, node):
        self.frontier[node.state] = node

    
    def contains_state(self, state):
        return any(node == state for node in self.frontier)


    def remove(self):
        if not self.empty():
            return self.frontier.pop(self.estimate_from_goal())

        raise Exception("empty frontier")
        

# Explores paths that have took fewer number of moves to reach and at the same time closer to the goal
class AStarSearch(DepthFirstSearch):
    def __init__(self, goal):
        self.goal = goal
        self.frontier = {}
        self.currentMinTuple = (0, 0)

    def moves_from_start(self, node):
        """ Backtracks it back to the starting position in order to know how many steps where taken to get to
            the current position """

        moves = 0

        while node.parent is not None:
            node = node.parent
            moves += 1

        return moves

    def estimate_from_goal(self):
        currentMinValue = float('inf')
        goalRow, goalCol = self.goal

        for key in self.frontier:
            stateRow, stateCol = key

            currentValue = abs(goalRow - stateRow) + abs(goalCol - stateCol) + self.moves_from_start(self.frontier[key])

            if currentValue < currentMinValue:
                currentMinValue = currentValue
                self.currentMinTuple = key
        
        return self.currentMinTuple


    def add(self, node):
        self.frontier[node.state] = node

    
    def contains_state(self, state):
        return any(node == state for node in self.frontier)


    def remove(self):
        if not self.empty():
            return self.frontier.pop(self.estimate_from_goal())

        raise Exception("empty frontier")


# Creates a simulation of a maze with walls, starting point, goal etc
class Maze():
    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        """ Prints the maze before and after finding a solution """

        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        """ Identify all  possible moves from the current position """

        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []

        # Actually seperates the possible moves from the candidates
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = DepthFirstSearch()
        # frontier = BreathFirstSearch()
        # frontier = GreedyBestFirstSearch(self.goal)
        # frontier = AStarSearch(self.goal)
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
                    print(action)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)