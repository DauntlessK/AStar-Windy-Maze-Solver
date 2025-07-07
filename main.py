import heapq

class Maze():

    def __init__(self):
        # Maze stored as a 2D array, where 0 = empty box, 1 = start, 2 = finish, 8 = blank space
        self.layout = [[0,1,0,8,0,0],
                       [0,8,8,8,8,0],
                       [0,8,0,2,8,0],
                       [0,8,0,0,0,0],
                       [0,0,0,0,0,0]
                    ]
        
        # Wind Parameters
        self.windDirection = 0               # Direction wind blows: 0 = West, 1 = North, 2 = East, 3 = South
        self.MOVEMENT_COST_WITH_WIND = 1     # cost in spaces to move in the direction of the wind
        self.MOVEMENT_COST_PERP_WIND = 2     # cost in spaces to move perpendicular to the wind
        self.MOVEMENT_COST_AGAINST_WIND = 3  # cost in spaces to move against the direction of the wind

        # Maze information
        self.numOfRows = len(self.layout)
        self.numOfColumns = len(self.layout[0])
        self.startBox = {}
        self.finishBox = {}
        self.setBoxes()

    def getBoxType(self, row, col):
        boxNum = self.layout[row][col]
        match boxNum:
            case 0:
                return "Empty Box"
            case 1:
                return "Start"
            case 2:
                return "Finish"
            case 8:
                return "Blank Space"

    # During init, called to establish the start and finish box coords
    # Also verifies only 1 start and only 1 finish        
    def setBoxes(self):
        numStarts = 0
        numFinishes = 0
        for row in range(len(self.layout)):
            for column in range(len(self.layout[row])):
                if self.getBoxType(row, column) == "Start":
                    self.startBox["Row"] = row
                    self.startBox["Column"] = column
                    numStarts += 1
                if self.getBoxType(row, column) == "Finish":
                    self.finishBox["Row"] = row
                    self.finishBox["Column"] = column
                    numFinishes += 1
        if numStarts != 1:
            raise ValueError("Not enough or too many start boxes in maze. Initialization failed.")
        if numFinishes != 1:
            raise ValueError("Not enough or too many finish boxes in maze. Initialization failed.")
            
    # Returns dictionary object containing row and column of box
    def getStartBox(self):
        return self.startBox
    
    def getStartBoxRow(self):
        return self.startBox["Row"]
    
    def getStartBoxColumn(self):
        return self.startBox["Column"]

    # Returns dictionary object containing row and column of box
    def getFinishBox(self):
        return self.finishBox

    # Returns wind direction in int format (0 is West)
    def getWindDirection(self):
        return self.windDirection
    
    # Figures out the cost of a movement in a given direction based on wind
    # Returns int of # of movement cost
    def getMovementCost(self, direction):
        if direction == self.windDirection:
            return self.MOVEMENT_COST_WITH_WIND
        elif (direction - 2 == self.windDirection) or (direction + 2 == self.windDirection):
            return self.MOVEMENT_COST_AGAINST_WIND
        else:
            return self.MOVEMENT_COST_PERP_WIND
        
    # Returns the manhattan distance of a given box at row, col to the maze finish box
    def getManhattanDistance(self, row, col):
        manDistRow = abs(row - self.finishBox["Row"])
        manDisCol = abs(col - self.finishBox["Column"])
        return manDistRow + manDisCol
        
    # Returns True if there's a box that can be explored, otherwise returns False
    def boxExists(self, row, col):
        if row > self.numOfRows or col > self.numOfColumns:
            return False
        elif row < 0 or col < 0:
            return False
        box = self.getBoxType(row, col)
        if box == "Empty Box":
            return True
        else:
            return False
        
# One individual node that holds a box's info when it is discovered, then added to the queue
class boxNode():
    
    def __init__(self, maze, num, movementCost, row, col):
        self.num = num                              # discovery number
        self.movementCost = movementCost            # total movement cost of this box along with every square to date
        self.maze = maze
        self.row = row
        self.column = col
        self.manhattanDistance = self.maze.getManhattanDistance(self.row, self.column)
        self.totalCost = self.movementCost + self.manhattanDistance

    def __lt__(self, other):
        if self.totalCost == other.totalCost:
            return self.num < other.num
        return self.totalCost < other.totalCost
    
    def __str__(self):
        return f"Node #{self.num} - Loc: {self.row},{self.column} - {self.movementCost} + {self.manhattanDistance} = {self.totalCost}"

def resolveBox(maze, heap, exp, box):
    # Check West first
    if maze.boxExists(box.row, box.column-1):
        exp += 1
        newNodeWest = boxNode(maze, exp, maze.getMovementCost(0), box.row, box.column-1)
        heapq.heappush(heap, newNodeWest)
    # Check North
    if maze.boxExists(box.row-1, box.column):
        exp += 1
        newNodeNorth = boxNode(maze, exp, maze.getMovementCost(1), box.row-1, box.column)
        heapq.heappush(heap, newNodeNorth)
    # Check East
    if maze.boxExists(box.row, box.column+1):
        exp += 1
        newNodeEast = boxNode(maze, exp, maze.getMovementCost(2), box.row, box.column+1)
        heapq.heappush(heap, newNodeEast)
    # Check South
    if maze.boxExists(box.row+1, box.column):
        exp += 1
        newNodeSouth = boxNode(maze, exp, maze.getMovementCost(3), box.row+1, box.column)
        heapq.heappush(heap, newNodeSouth)

    print(heap)

m = Maze()
heapFrontier = []
nodeStart = boxNode(m, 0, 0, m.getStartBoxRow(), m.getStartBoxColumn())
exploredCount = 1
resolveBox(m, heapFrontier, exploredCount, nodeStart)
print(heapq.heappop(heapFrontier))
print(heapq.heappop(heapFrontier))