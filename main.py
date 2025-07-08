import heapq

class Maze():

    def __init__(self):
        # Maze stored as a 2D array, where 0 = empty box, -1 = start, -2 = finish, -8 = blank space
        # Positive ints represent an explored box (and the number in which they were discovered)
        #self.layout = [[00,-1,00,00,00,00],
        #               [00,-8,-8,-8,-8,00],
        #               [00,-8,00,-2,-8,00],
        #               [00,-8,00,00,00,00],
        #               [00,00,00,00,00,00]
        #            ]
        
        self.layout = [[00,-1,00,00,00,00],
                       [-8,-8,-8,-8,-8,00],
                       [-2,-8,-8,00,00,00],
                       [00,-8,-8,-8,-8,00],
                       [00,00,00,-8,00,00],
                       [00,00,00,00,00,00]
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

        # Discovery Globals
        self.nodesDiscovered = 0             # total number of nodes that have been found (added to frontier heap or expanded)

    
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
                    case -1:
                        stringToReturn += "SS"
                    case -2:
                        stringToReturn += "FF"
                    case -5:
                        stringToReturn += "**"
                    case -8:
                        stringToReturn += "XX"
                    case _:
                        # Deal with numbers 0-9 by adding a leading zero to string
                        if len(str(self.layout[x][y])) == 1:
                            stringToReturn += "0"
                        stringToReturn += str(self.layout[x][y])

            stringToReturn += "\n"
        return stringToReturn

    # Updates map with a number            
    def updateBox(self, row, col, num):
        self.layout[row][col] = num

    # Updates map with next discovery num          
    def discoverBox(self, row, col):
        self.nodesDiscovered += 1
        self.layout[row][col] = self.nodesDiscovered

    def getNumNodesDiscovered(self):
        return self.nodesDiscovered

    def getBoxType(self, row, col):
        boxNum = self.layout[row][col]
        match boxNum:
            case 0:
                return "Empty Box"
            case -1:
                return "Start"
            case -2:
                return "Finish"
            case -8:
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
        if box == "Empty Box" or box == "Finish":
            return True
        else:
            return False
        
    # Called when solution is found to revert maze array back to original, then fill in the solution
    def updateWithSolution(self, solution):
        for x in range(len(self.layout)):
            for y in range(len(self.layout[x])):
                if self.layout[x][y] not in solution and self.layout[x][y] > 0:
                    self.layout[x][y] = 00
                elif self.layout[x][y] in solution:
                    self.layout[x][y] = -5    

        
# One individual node that holds a box's info when it is discovered, then added to the queue
class boxNode():
    
    def __init__(self, maze, movementCost, row, col):
        self.num = maze.getNumNodesDiscovered() + 1 # discovery number
        self.movementCost = movementCost            # total movement cost of this box along with every square to date
        self.maze = maze
        self.row = row
        self.column = col
        self.type = self.maze.getBoxType(self.row, self.column)
        if self.type == "Start":
            self.num = 0
        self.manhattanDistance = self.maze.getManhattanDistance(self.row, self.column)
        self.totalCost = self.movementCost + self.manhattanDistance

    def __lt__(self, other):
        if self.totalCost == other.totalCost:
            return self.num < other.num
        return self.totalCost < other.totalCost
    
    def __eq__(self, other):
        if isinstance(other, int): 
            if other == self.num:
                return True
            else:
                return False
        if self.row == other.row and self.column == other.column:
            return True
        else:
            return False
    
    def __str__(self):
        return f"Node #{self.num} - Loc: {self.row},{self.column} - {self.movementCost} + {self.manhattanDistance} = {self.totalCost}"
    
    # Determines if this node is neighbors with another node
    def isNeighbors(self, otherNode):
        # Check if East or West neighbors
        if (self.row == otherNode.row and self.column == otherNode.column - 1) or (self.row == otherNode.row and self.column == otherNode.column + 1):
            return True
        # Check if North or South neigbors
        if (self.row == otherNode.row  - 1 and self.column == otherNode.column) or (self.row == otherNode.row + 1 and self.column == otherNode.column):
            return True
        return False
    
    # Ensures this node is a part of the solution by making sure that this node is connected to two other nodes in the solution
    def isNotPartOfSolution(self, node1, node2):
        if self.isNeighbors(node1) and self.isNeighbors(node2):
            return False
        return True

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
def resolveBox(maze, heap, explored, box):
    result = "Not Found"
    # Check West first
    if maze.boxExists(box.row, box.column-1):
        newNodeWest = boxNode(maze, maze.getMovementCost(0), box.row, box.column-1)
        if notAlreadyExplored(explored, heap, newNodeWest):
            heapq.heappush(heap, newNodeWest)
            maze.discoverBox(box.row, box.column-1)
            if newNodeWest.type == "Finish":
                result = "Found"
    # Check North
    if maze.boxExists(box.row-1, box.column):
        newNodeNorth = boxNode(maze, maze.getMovementCost(1), box.row-1, box.column)
        if notAlreadyExplored(explored, heap, newNodeNorth):
            heapq.heappush(heap, newNodeNorth)
            maze.discoverBox(box.row-1, box.column)
            if newNodeNorth.type == "Finish":
                result = "Found"
    # Check East
    if maze.boxExists(box.row, box.column+1):
        newNodeEast = boxNode(maze, maze.getMovementCost(2), box.row, box.column+1)
        if notAlreadyExplored(explored, heap, newNodeEast):
            maze.discoverBox(box.row, box.column+1)
            heapq.heappush(heap, newNodeEast)
            if newNodeEast.type == "Finish":
                result = "Found"
    # Check South
    if maze.boxExists(box.row+1, box.column):
        newNodeSouth = boxNode(maze, maze.getMovementCost(3), box.row+1, box.column)
        if notAlreadyExplored(explored, heap, newNodeSouth):
            maze.discoverBox(box.row+1, box.column)
            heapq.heappush(heap, newNodeSouth)
            if newNodeSouth.type == "Finish":
                result = "Found"

    return result

# Goes back through explored list and gets the final solution to the maze
# Returns list of nodes in order from start to final node before finish
def backtrackForSolution(explored):
    solution = []
    # Add last explored node (the node that discovered the finish)
    previousNode = explored[len(explored) - 1]
    solution.append(previousNode)
    #Go through explored nodes backwards finding neighbors of all those that were connected to the node that discovered the finish
    for node in reversed(explored):
        if node.isNeighbors(previousNode):
            solution.insert(0, node)
            previousNode = node

    # runs through loop at least once (but possible multiple times) looking for nodes that only have 1 neighbor within the list
    # if found, removes it and reruns the loop again
    # not the greatest practice but python lacks a do, while loop so this is a workaround I guess
    # ------- NOT NEEDED, previous for loop removes dead ends
    #notVerified = True
    #while notVerified:
    #    notVerified = False
    #    for x in range(len(solution)):
    #    #skip first and last node
    #        if x == 0 or x == len(solution) - 1:
    #            continue
    #        if solution[x].isNotPartOfSolution(solution[x-1], solution[x+1]):
    #            solution.pop(x)
    #            notVerified = True
    return solution


m = Maze()
heapFrontier = []
explored = []
stepNum = 0                 # Current Step of expansion (loop)
nodeStart = boxNode(m, 0, m.getStartBoxRow(), m.getStartBoxColumn())

heapq.heappush(heapFrontier, nodeStart)

while (len(heapFrontier) != 0):
    currentBox = heapq.heappop(heapFrontier)
    print("Step #" + str(stepNum) + ":  Exploring " + str(currentBox.num))
    print(m)
    explored.append(currentBox)
    result = resolveBox(m, heapFrontier, explored, currentBox)
    stepNum += 1

    if result == "Found":
        break
    
solution = backtrackForSolution(explored)
m.updateWithSolution(solution)
print("Final Solution:")
print(m)