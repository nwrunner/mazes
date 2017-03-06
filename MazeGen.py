from PIL import Image
import os, random, sys

class MazeGen:

    def __init__(self, (x,y), genType, asPerfect):
        """ Generate a maze of size (x,y)

        generator type 1 = Prims, 2 = recursion
        a "perfect" maze has no loops and only one solutions
        """
        if x < 3 or y < 3:
            raise ValueError("Maze is too small, 3 x 3 maze is minimum", x, y)
            return

        x=MazeGen.makeOdd(x)
        y=MazeGen.makeOdd(y)
        self.perfect = asPerfect
            
        self.dimensions = (x,y)
        self.setFilePath()

        im = Image.new("RGB", self.dimensions)
        self.pixMap =  im.load()
        self.mazeBits = {}  # coordinate key, values 0-wall, 1-path, 2-queuedWall, 3-checkedWall (final for prims), -1 out of range

        if genType == 1:
            self.generate_prims()
        elif genType == 2:
            self.init_recurse()

        im.save(self.file, "BMP")

    def makePath(self, (x,y)):
        return

    def getMazeBit(self, (x,y)):
        # a wall is valid to be turned into a path if it is a wall
        if (x < 0 or  x >= self.dimensions[0]):
            return -1 # out of range
        
        if (y < 0 or  y >= self.dimensions[1]):
            return -1 # out of range

        return self.mazeBits((x,y))

    def generate_prims(self):
        """ prims algorithm for maze generation
        start with all walls and a starting point, somewhere at the top.  Add all neighboring walls to a list
        while list not empty:
            get a random item from the list.  
            If the wall has 3 wall neighbors, make it a path. 
                Add all unvisited walls to the list
        to make non-perfect, randomly change non-corners walls to paths
        """
        self.init_prims()
        randomX = random.randint(1, self.dimensions[0]-2) # choose a random "x" position at the top row
        self.makePath((randomX, 0))
        self.mazeBits((randomX,0)) = 1

        l = []
        if self.getMazeBit(randomX-1, 0) == 0:
            l.append((randomX-1, 0))
        if self.getMazeBit(randomX+1, 0) == 0:
            l.append((randomX+1, 0))
        
        while l:
            


        


    def init_prims(self):
        # Create an all wall maze, no need to set anything to white.
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.mazeBits[x,y] = 0

    def init_recurse(self):
        # Create an empty maze with walled off border
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if x == 0 or y == 0 or x == self.dimensions[0]-1 or y == self.dimensions[1]-1:
                    self.mazeBits[x,y] = 0
                else:
                    self.mazeBits[x,y] = 1
                    self.pixMap[x,y] = (255,255,255)



    def generate_recurse(self):
        self.init_recurse()
        return

    
    def setFilePath(self):
        mazeNum = 0
        while mazeNum==0 or os.path.exists(filePath):
            mazeNum+=1
            mazeName = (("0" * 5) + str(mazeNum))[-5:]
            newFileName = "m" + str(self.dimensions[0]) + "." + mazeName + ".png"
            filePath = ".\\puzzles\\" + newFileName

        self.file = filePath

        
    @staticmethod
    def makeOdd(i):
        if i % 2 == 1:
            return i
        else:
            return i+1    

    def populateBits(self):
        # -1=Wall, 0=Unvisited Path, 1=visited path
        # Assumptions, the first non-wall at the top is the start
        # the first non-wall at the bottom is the end
        pygame.init()
        self.screen = pygame.display.set_mode(self.dimensions)
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                self.screen.set_at((i,j), self.pixMap[i,j])
                if (self.pixMap[i,j] == (255,255,255)):
                    self.mazeBits[i,j] = 0
                    self.nodeCount+=1
                    if j == 0: 
                        self.pixMap[i,j] = (0,255,0)     
                        self.start = (i,j) 
                    elif j == self.dimensions[0] -1:
                        self.pixMap[i,j] = (255,0,0)     
                        self.end = (i,j)
                else:
                    self.mazeBits[i,j] = -1
        pygame.display.update()

        

    def updateImage(self, pos, rgb, ticks):
        self.pixMap[pos] = rgb
        self.screen.set_at(pos, rgb)
        if ticks != 0:
            # don't bother updating if ticks == 0
            pygame.display.update()
            time.sleep(Decimal(ticks)/1000)


    def writeFile(self, solver):
        dotIdx = self.fName.index('.') 
        newFileName = self.fName[0:dotIdx] + "." + self.startTime + "." + solver + ".png"
        self.im.save(".\\solutions\\" + newFileName, "PNG")

    # print maze walls in Console, note that we print one LINE at a time (in the "Y" direction)
    # so note the flip that we "y" is the outer loop.
    def printMe(self):
        for y in range(self.dimensions[1]):
            line = ""
            for x in range(self.dimensions[0]):
                if (self.mazeBits[x,y] != -1):
                    line += " "
                else:
                    line += "X"
            print(line)

        """
        for i in range(self.dimensions[0]):
            line = ""
            for j in range(self.dimensions[1]):
                if (self.pixMap[j,i] == (255,255,255)):
                    line += " "
                else:
                    line += "X"
            print(line)
        """
        

    # end print method    


# print the maze as "X" for walls, blank space for paths
myMaze = MazeGen((50,50), 2, True)
#myMaze.writeFile()
#myMaze.solveMazeBfs()
#myMaze.printMe()
