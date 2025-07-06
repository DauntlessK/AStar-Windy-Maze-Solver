class Maze():

    def __init__(self):
        #Maze stored as a 2D array, where 0 = empty box, 1 = start, 2 = finish, 8 = blank space
        self.layout = [[0,1,0,8,0,0],
                       [0,8,8,8,8,0],
                       [0,8,0,2,8,0],
                       [0,8,0,0,0,0],
                       [0,0,0,0,0,0]
                    ]
        
        #Wind Parameters
        windDirection = 0               # 0 = West, 1 = North, 2 = East, 3 = South
        MOVEMENT_COST_WITH_WIND = 1     # cost in spaces to move in the direction of the wind
        MOVEMENT_COST_PERP_WIND = 2     # cost in spaces to move perpendicular to the wind
        MOVEMENT_COST_AGAINST_WIND = 3  # cost in spaces to move against the direction of the wind

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
    def getEndBox(self):
        return self.finishBox
            
class Queue():

    def __init__(self):
        pass

m = Maze()
print(m.getBoxType(0,2))
print(m.finishBox["Row"])