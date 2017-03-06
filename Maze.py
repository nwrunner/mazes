from PIL import Image
from decimal import Decimal
import time, os, pygame, sys

class Maze:
    def __init__(self, fileName):
        self.fName = fileName
        self.im = Image.open(".\\puzzles\\" + fileName)
        self.dimensions = self.im.size
        self.pixMap =  self.im.load()
        self.nodeCount = 0
        self.visitCount = 0

        self.mazeBits = {}
        self.populateBits()

        print "Maze size: " + str(self.dimensions[0]) + " x " + str(self.dimensions[1])
        print "Node Count: " + str(self.nodeCount)

        self.startTime = time.strftime("%m%d.%H%M")
        #self.folder = ".\\solutions\\" + self.startTime

        # no longer need to create the folder ahead of time 
        # os.makedirs(self.folder)

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

    def visitNode(self, pos, ticks):
        # for all non-start nodes, mark as visited involves coloring white -> gray
        self.mazeBits[pos] = 1 
        self.updateImage(pos, (128,128,128), ticks)
        self.visitCount += 1

        # write out to file (too slow, thousands of useless files)
        #paddedNum = (("0" * 12) + str(self.visitCount))[-12:]
        #newFileName = "iter" + paddedNum + ".png"
        #self.im.save(self.folder + "\\" + newFileName, "PNG")
    # end visitNode

    def reset(self):
        # reset colors, "unsolve" the maze by scrubbing the path
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                if (self.pixMap[i,j] != (0,0,0)):
                    # anything not a wall
                    self.updateImage((i,j), (255,255,255), 0)
                    self.mazeBits[i,j] = 0
        # set the start and end nodes            
        self.updateImage(self.start, (0,255,0),0)
        self.updateImage(self.end, (255,0,0),1) #force screen refresh
        
        self.visitCount = 0
        
    def checkLastNode(self, node, solver):
        # performs "end game" actions if the node matches "end"
        print ""            
        if (node.position != self.end):
            print "No solution found using " + solver            
            self.writeFile(solver) 
            return

        print "Solved using " + solver
        print "Nodes visited: " + str(self.visitCount)
        print "Path Length: " + str(node.depth)

        arr = [0]*(node.depth+1)
        pathLength = node.depth
        arr[node.depth] = node.position
        while (node.parent):
            node = node.parent
            arr[node.depth] = node.position
            self.colorPath(node, pathLength)
        
        # because we "visited" the start and end, re-color
        self.updateImage(self.start, (0,255,0),0)
        self.updateImage(self.end, (255,0,0),1)

        self.writeFile(solver)
        pygame.display.update()
        time.sleep(1)
        self.reset()

    def colorPath(self, node, pathLength):
        # transition from Green to blue from start to middle
        # transition from blue to red from middle to end
        
        halfway = pathLength / 2
        if node.depth >= halfway:
            # transition from red to blue
            r = (255 * (node.depth - halfway)) / halfway
            b = 255 - r
            self.updateImage(node.position, (r,0,b),0)
        else:
            # transition 
            b = (255 * node.depth) / halfway
            g = 255 - b
            #self.pixMap[node.position[0], node.position[1]] = (0, g, b)     
            self.updateImage(node.position, (0,g,b),0)
    # end colorPath

    def updateImage(self, pos, rgb, ticks):
        self.pixMap[pos] = rgb
        self.screen.set_at(pos, rgb)
        if ticks != 0:
            # don't bother updating if ticks == 0
            pygame.display.update()
            time.sleep(Decimal(ticks)/1000)

    def isValidPath(self, (x,y)):
        if (x<0 or x > self.dimensions[0]):
            return False 
        if (y<0 or y > self.dimensions[1]):
            return False
        if (self.mazeBits[(x,y)] == 0): # valid path!
            return True
        else:         # other conditions, -1 (wall), 1 (visited node)
            return False


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
#myMaze = Maze("maze101.bmp")
#myMaze.writeFile()
#myMaze.solveMazeBfs()
#myMaze.printMe()
