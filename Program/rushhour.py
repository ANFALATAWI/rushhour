import sys
from collections import deque
from vehicle import Vehicle
from Queue import PriorityQueue
import webbrowser, os

GOAL_VEHICLE = Vehicle('X', 4, 2, 'H')

class RushHour(object):
    """A configuration of a single Rush Hour board."""

    def __init__(self, vehicles):
        """Create a new Rush Hour board.
        
        Arguments:
            vehicles: a set of Vehicle objects.
        """
        self.vehicles = vehicles

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.vehicles == other.vehicles

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        s = '-' * 8 + '\n'
        for line in self.get_board():
            s += '|{0}|\n'.format(''.join(line))
        s += '-' * 8 + '\n'
        return s

    def get_board(self):
        """Representation of the Rush Hour board as a 2D list of strings"""
        board = [[' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ']]
        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            if vehicle.orientation == 'H':
                for i in range(vehicle.length):
                    board[y][x+i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    board[y+i][x] = vehicle.id
        return board

    def solved(self):
        """Returns true if the board is in a solved state."""
        return GOAL_VEHICLE in self.vehicles

    def moves(self):
        """Return iterator of next possible moves."""
        board = self.get_board()
        for v in self.vehicles:
            if v.orientation == 'H':
                if v.x - 1 >= 0 and board[v.y][v.x - 1] == ' ':
                    new_v = Vehicle(v.id, v.x - 1, v.y, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles)
                if v.x + v.length <= 5 and board[v.y][v.x + v.length] == ' ':
                    new_v = Vehicle(v.id, v.x + 1, v.y, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles)
            else:
                if v.y - 1 >= 0 and board[v.y - 1][v.x] == ' ':
                    new_v = Vehicle(v.id, v.x, v.y - 1, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles)
                if v.y + v.length <= 5 and board[v.y + v.length][v.x] == ' ':
                    new_v = Vehicle(v.id, v.x, v.y + 1, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles)

def load_file(rushhour_file):
    vehicles = []
    for line in rushhour_file:
        line = line[:-1] if line.endswith('\n') else line
        id, x, y, orientation = line
        vehicles.append(Vehicle(id, int(x), int(y), orientation))
    return RushHour(set(vehicles))

def breadth_first_search(r, firstSolution, max_depth=25):
    """
    Find solutions to given RushHour board using breadth first search.
    Returns a dictionary with named fields:
        visited: the number of configurations visited in the search
        solutions: paths to the goal state
        depth_states: the number of states visited at each depth
    Arguments:
        r: A RushHour board.
        firstSolution: Boolean if true stops execution after finding the first solution.
    Keyword Arguments:
        max_depth: Maximum depth to traverse in search (default=25)
    """
    print 'State of the board:\n{0}'.format(r)
    visited = set()
    solutions = list()
    depth_states = dict()
    queue = deque()
    queue.appendleft((r, tuple()))
    while len(queue) != 0:
        board, path = queue.pop()
        new_path = path + tuple([board])

        depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1

        if len(new_path) >= max_depth:
            break

        if board in visited:
            continue
        else:
            visited.add(board)

        if board.solved():
            solutions.append(new_path)
            if firstSolution:
                return {'visited': visited,
                        'solutions': solutions,
                        'depth_states': depth_states}
        else:
            queue.extendleft((move, new_path) for move in board.moves())

    return {'visited': visited,
            'solutions': solutions,
            'depth_states': depth_states}

def A_star_search_H1(r, firstSolution, max_depth=25):
    """
    Find solutions to given RushHour board using A* search by H1.
    Returns a dictionary with named fields:
        visited: the number of configurations visited in the search
        solutions: paths to the goal state
        depth_states: the number of states visited at each depth
    Arguments:
        r: A RushHour board.
        firstSolution: Boolean if true stops execution after finding the first solution.
    Keyword Arguments:
        max_depth: Maximum depth to traverse in search (default=25)
    """
    print 'State of the board:\n{0}'.format(r)
    visited = set()
    solutions = list()
    depth_states = dict()
    queue = PriorityQueue()
    queue.put((0,r,tuple()))
    while not queue.empty():
        x, board, path = queue.get()
        new_path = path + tuple([board]) # -- Add this board to the path
        depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1 # -- saving the depth
        if len(new_path) >= max_depth:
            break
        if board in visited:
            continue
        else:
            visited.add(board)
        if board.solved():
            solutions.append(new_path)
            if firstSolution:
                return {'visited': visited,
                        'solutions': solutions,
                        'depth_states': depth_states}
        else:
            for move in board.moves():
                priority = H1(move.get_board())
                queue.put((priority, move, new_path))

    return {'visited': visited,
            'solutions': solutions,
            'depth_states': depth_states}

def A_star_search_H2(r, firstSolution, max_depth=25):
    """
    Find solutions to given RushHour board using A* search by H2.
    Returns a dictionary with named fields:
        visited: the number of configurations visited in the search
        solutions: paths to the goal state
        depth_states: the number of states visited at each depth
    Arguments:
        r: A RushHour board.
        firstSolution: Boolean if true stops execution after finding the first solution.
    Keyword Arguments:
        max_depth: Maximum depth to traverse in search (default=25)
    """
    print 'State of the board:\n{0}'.format(r)
    visited = set()
    solutions = list()
    depth_states = dict()
    queue = PriorityQueue()
    queue.put((0,r,tuple())) # -- he sent R and an empty tuple
    while not queue.empty():

        x, board, path = queue.get() # -- Load this state, x is to handle priority.
        new_path = path + tuple([board]) # -- Add this board to the path
        depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1 # -- saving the depth
        if len(new_path) >= max_depth:
            break
        if board in visited:
            continue
        else:
            visited.add(board)
        if board.solved():
            solutions.append(new_path)
            if firstSolution:
                return {'visited': visited,
                        'solutions': solutions,
                        'depth_states': depth_states}
        else:
            for move in board.moves():
                # Calc heuristic
                # priority = 0             # -- Breadth with no heuristic at all, H0
                priority = H2(move.get_board())
                queue.put((priority, move, new_path))
            

    return {'visited': visited,
            'solutions': solutions,
            'depth_states': depth_states}

def A_star_search_H3(r, firstSolution, max_depth=25):
    """
    Find solutions to given RushHour board using A* search by H3.
    Returns a dictionary with named fields:
        visited: the number of configurations visited in the search
        solutions: paths to the goal state
        depth_states: the number of states visited at each depth
    Arguments:
        r: A RushHour board.
        firstSolution: Boolean if true stops execution after finding the first solution.
    Keyword Arguments:
        max_depth: Maximum depth to traverse in search (default=25)
    """
    print 'State of the board:\n{0}'.format(r)
    visited = set()
    solutions = list()
    depth_states = dict()
    queue = PriorityQueue()
    queue.put((0,r,tuple()))
    while not queue.empty():
        x, board, path = queue.get()
        new_path = path + tuple([board])
        depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1
        if len(new_path) >= max_depth:
            break
        if board in visited:
            continue
        else:
            visited.add(board)
        if board.solved():
            solutions.append(new_path)
            if firstSolution:
                return {'visited': visited,
                        'solutions': solutions,
                        'depth_states': depth_states}
        else:
            for move in board.moves():
                m = move.get_board()
                priority = H3(m)
                queue.put((priority, move, new_path))

    return {'visited': visited,
            'solutions': solutions,
            'depth_states': depth_states}

def H1(state):
    '''
    Calculates Heuristic #1
    The distance from the car to the exit (goal state).

    Returns:
        Integer: the heuristic score of that board.
    Arguments:
        state: the state of the board.
    '''
    for index, x in enumerate(state):
        for index,y in enumerate(x):
            if y == 'X':
                return 6 - (index+2)

def H2(state):
    '''
    Calculates Heuristic #2
    The number of cars blocking the main car + 1,
    or 0 if it was at goal.

    Returns:
        Integer: the heuristic score of that board.
    Arguments:
        state: the state of the board.
    '''
    if state[2][5] == 'X':
        return 0
    else:
        return findBlockers(state[2], 'X') + 1

def H3(state):
    '''
    Calculates Heuristic #3
    The number of cars blocking the car to the exit
    + the min number of cars blocking the first car from moving.

    Returns:
        Integer: the heuristic score of that board.
    Arguments:
        state: the state of the board.
    '''
    if H2(state) == 0:
        return 0
    elif H2(state) == 1:
        return 1
    blockingList = list()
    for index, x in enumerate(state):
        if index == 2:
            strRow = ''.join(x)
            frontOfCar = strRow.rindex('X')
            counter = frontOfCar + 1
            while counter < 6:
                if x[counter] in blockingList:
                    counter = counter + 1
                    continue
                else:
                    if x[counter] != ' ':
                        blockingList.append(x[counter])
                        break
                counter = counter + 1 
    
    blockingcar = blockingList[0]
    ypos = counter
    column = [row[ypos] for row in state]
    return findBlockers(state[2], 'X') + min(findBlockers(column, blockingcar, onlyImmediate = True), findBlockers(column[::-1], blockingcar, onlyImmediate = True)) + 1


def findBlockers(row,char, onlyImmediate = False):
    '''
    Calculates the cars blocking any given car.

    Returns:
        Integer: the number of cars blocking car char
    Arguments:
        char: character, the name of the car to inspect its blockers.
        row: character array, the row the car char is in.
        onlyImmediate: boolean, if true the function only checks adjacent cars.
    '''
    blockingList = list()
    strRow = ''.join(row)
    frontOfCar = strRow.rindex(char)

    if not onlyImmediate:
        if frontOfCar == 5:
            return 0
    else:
        if frontOfCar == 5:
            return 10
        if row[frontOfCar + 1] == ' ':
            return 0
    counter = frontOfCar + 1
    while counter < 6:
        if row[counter] in blockingList:
            counter = counter + 1
            continue
        else:
            if row[counter] != ' ':
                blockingList.append(row[counter])
            counter = counter + 1
    return len(blockingList)

def solution_steps(solution):
    """Generate list of steps from a solution path."""
    steps = []
    for i in range(len(solution) - 1):
        r1, r2 = solution[i], solution[i+1]
        v1 = list(r1.vehicles - r2.vehicles)[0]
        v2 = list(r2.vehicles - r1.vehicles)[0]
        if v1.x < v2.x:
            steps.append('{0}R'.format(v1.id))
        elif v1.x > v2.x:
            steps.append('{0}L'.format(v1.id))
        elif v1.y < v2.y:
            steps.append('{0}D'.format(v1.id))
        elif v1.y > v2.y:
            steps.append('{0}U'.format(v1.id))
    return steps

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as rushhour_file:
        rushhour = load_file(rushhour_file)


    print '\n             *** RUSH HOUR HEURISTIC SOLVER ***'

    # BFS SEARCH: -----------------------------------------------------------------------------------

    # results = breadth_first_search(rushhour, max_depth=100, firstSolution = True)
    # print 'Solving using BFS'
    # for solution in results['solutions']:
    #     print 'Solution: {0}'.format(', '.join(solution_steps(solution)))

    # print 'Nodes visited: {0}'.format(len(results['visited']))
    # print 'Depth: {0}'.format(len(results['depth_states']))

    # A* SEARCH: H1: Distance Heuristic ----------------------------------------------------------------

    # results = A_star_search_H1(rushhour, max_depth=1000, firstSolution = True)
    # print 'Solving using A* H1: Distance Heuristic'
    # for solution in results['solutions']:
    #     print 'Solution: {0}'.format(', '.join(solution_steps(solution)))
    #     print 'Number of moves: {0}'.format(len(solution) - 1)
    # print 'Depth: {0}'.format(len(results['depth_states']))
    # print 'Nodes visited: {0} '.format(len(results['visited']))


    # A* SEARCH: H2: Blocking cars Heuristic -----------------------------------------------------------

    # results = A_star_search_H2(rushhour, max_depth=1000, firstSolution = True)
    # print 'Solving using A* H2: Blocking cars Heuristic'
    # for solution in results['solutions']:
    #     print 'Solution: {0}'.format(', '.join(solution_steps(solution)))
    #     print 'Number of moves: {0}'.format(len(solution) - 1)
    # print 'Depth: {0}'.format(len(results['depth_states']))
    # print 'Nodes visited:{}'.format(len(results['visited']))

    
    
    # A* SEARCH: H3: Double Blocking heuristic ----------------------------------------------------------

    results = A_star_search_H3(rushhour, max_depth=1000, firstSolution = True)

    print 'A* H3: Double Blocking Heuristic'
    print 'Depth: {0}'.format(len(results['depth_states']))
    print 'Nodes visited:{0}'.format(len(results['visited']))

    for solution in results['solutions']:
        print 'Solution: {0}'.format(', '.join(solution_steps(solution)))
        print 'Number of moves: {0}'.format(len(solution) - 1)

    # Calling interface:
    # Change path as appropriate: /Users/anfalalatawi/Downloads/RushHour/index.html
    filename = '/Users/anfalalatawi/Downloads/RushHour/index.html'
    webbrowser.open('file://' + os.path.realpath(filename))
    
