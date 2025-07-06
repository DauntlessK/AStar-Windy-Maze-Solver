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
        self.windDirection = 0               # 0 = West, 1 = North, 2 = East, 3 = South
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
            return False
        else:
            return True
        
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
        self.next = None

# Responsible for holding the frontier as a sorted list of box nodes
class Queue():

    def __init__(self):
        self.head = None

    # Inserts a new node into the linked list, keeping it sorted according to totalCost (tiebreak goes to num)
    def insert(newNode):
        pass

m = Maze()
print(m.getBoxType(0,2))
print(m.finishBox["Row"])
print(m.getMovementCost(2))