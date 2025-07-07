import heapq

class Maze():

    def __init__(self):
        # Maze stored as a 2D array, where 0 = empty box, 1 = start, 2 = finish, 8 = blank space
        self.layout = [[0,1,0,0,0,0],
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
    
    def __str__(self):
        stringToReturn = ""
        for x in range(len(self.layout)):
            for y in range(len(self.layout[x])):
                # Add spaces for between boxes, except on column 0
                if y != 0:
                    stringToReturn += "  "
                match self.layout[x][y]:
                    case 0:
                        stringToReturn += "[]"
                    case 1:
                        stringToReturn += "SS"
                    case 2:
                        stringToReturn += "GG"
                    case 8:
                        stringToReturn += "XX"
            stringToReturn += "\n"
        return stringToReturn
                

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
        if row > self.numOfRows-1 or col > self.numOfColumns-1:
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
        self.type = self.maze.getBoxType(self.row, self.column)
        self.manhattanDistance = self.maze.getManhattanDistance(self.row, self.column)
        self.totalCost = self.movementCost + self.manhattanDistance

    def __lt__(self, other):
        if self.totalCost == other.totalCost:
            return self.num < other.num
        return self.totalCost < other.totalCost
    
    def __eq__(self, other):
        if self.row == other.row and self.column == other.column:
            return True
        else:
            return False
    
    def __str__(self):
        return f"Node #{self.num} - Loc: {self.row},{self.column} - {self.movementCost} + {self.manhattanDistance} = {self.totalCost}"

# Checks to see if the current box that may be added is already explored
def notAlreadyExplored(explored, heap, box):
    # First check if it's already in the explored list
    for node in explored:
        if box == node:
            return False
    # Check if it's waiting already in the Heap
    for node in heap:
        if box == node:
            return False
    return True
        
# Checks a given box's 4 surrounding boxes and adds them to the heap if applicable
def resolveBox(maze, heap, explored, exp, box):
    result = "Not Found"
    # Check West first
    if maze.boxExists(box.row, box.column-1):
        exp += 1
        newNodeWest = boxNode(maze, exp, maze.getMovementCost(0), box.row, box.column-1)
        if notAlreadyExplored(explored, heap, newNodeWest):
            heapq.heappush(heap, newNodeWest)
        if newNodeWest.type == "Finish":
            result = "Found"
    # Check North
    if maze.boxExists(box.row-1, box.column):
        exp += 1
        newNodeNorth = boxNode(maze, exp, maze.getMovementCost(1), box.row-1, box.column)
        if notAlreadyExplored(explored, heap, newNodeNorth):
            heapq.heappush(heap, newNodeNorth)
        if newNodeNorth.type == "Finish":
            result = "Found"
    # Check East
    if maze.boxExists(box.row, box.column+1):
        exp += 1
        newNodeEast = boxNode(maze, exp, maze.getMovementCost(2), box.row, box.column+1)
        if notAlreadyExplored(explored, heap, newNodeEast):
            heapq.heappush(heap, newNodeEast)
        if newNodeEast.type == "Finish":
            result = "Found"
    # Check South
    if maze.boxExists(box.row+1, box.column):
        exp += 1
        newNodeSouth = boxNode(maze, exp, maze.getMovementCost(3), box.row+1, box.column)
        if notAlreadyExplored(explored, heap, newNodeSouth):
            heapq.heappush(heap, newNodeSouth)
        if newNodeSouth.type == "Finish":
            result = "Found"

    return result

m = Maze()
heapFrontier = []
explored = []
exploredCount = 0
print(m)
nodeStart = boxNode(m, 0, 0, m.getStartBoxRow(), m.getStartBoxColumn())

heapq.heappush(heapFrontier, nodeStart)

while (len(heapFrontier) != 0):
    currentBox = heapq.heappop(heapFrontier)
    explored.append(currentBox)
    result = resolveBox(m, heapFrontier, explored,  exploredCount, currentBox)
    exploredCount += 1

    if result == "Found":
        break
    
print(heapFrontier)
print(explored)