class Maze():

    def __init__(self):
        #Maze stored as a 2D array, where 0 = empty box, 1 = start, 2 = finish, 8 = blank space
        layout = [[0,1,0,8,0,0],
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