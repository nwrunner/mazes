import sys
import math

class MazeNode:
    # Generic maze node with position, visited flag and parent
    def __init__(self, (x,y), depth):
        self.position = (x,y) 
        #self.visited = False
        self.parent = None
        self.depth = depth
        # Fancy MazeNode keeping track of neighbors
        #self.neighbors = { Up:None, Down:None, Left:None, Right:None } 


class AstNode(MazeNode):
    def __init__(self, (i,j), depth, end):
        MazeNode.__init__(self,(i,j), depth)
        self.setHeuristic(end)

    def __cmp__(self, other):
        #return cmp(self.heur + self.depth, other.heur + other.depth)
        return cmp(self.heur, other.heur)

    def setHeuristic(self, (i,j)):
        # Distance as the crow flies
        # the lower the distance from the end, the higher the priority
        # used as he
        iDist = abs(i-self.position[0]) 
        jDist = abs(j-self.position[1])
        self.heur = math.sqrt((iDist*iDist) + (jDist*jDist)) // 1
