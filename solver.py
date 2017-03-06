from Maze import *
from heapq import *
import Queue
from MazeNodes import *

class Solver:
    # Generic maze node with position, visited flag and parent
    def __init__(self, maze):
        self.maze = maze
        self.nodeMap = {} # store nodes we have added to the queue, but haven't visited

    def DFS(self, msTicks):
        stk = []
        maze = self.maze
        self.nodeMap = {}
        node = MazeNode(maze.start, 0)
        stk.append(node)

        while stk:
            node = stk.pop()
            maze.visitNode(node.position,msTicks)
            if (node.position == maze.end):
                break

            x = node.position[0]
            y = node.position[1]
            self.addPathDfs((x, y-1), node, stk)
            self.addPathDfs((x, y+1), node, stk)
            self.addPathDfs((x-1, y), node, stk)
            self.addPathDfs((x+1, y), node, stk)
        maze.checkLastNode(node, "DFS")

    def addPathDfs(self, (x,y), node, stk):
        if not self.maze.isValidPath((x,y)):
            return

        if (x,y) in self.nodeMap.keys():
            return

        newNode = MazeNode((x,y), node.depth+1)
        newNode.parent = node
        stk.append(newNode)
        self.nodeMap[(x,y)] = 1

    def AStar(self, msTicks):
        maze = self.maze
        self.nodeMap = {}
        h = []

        node = MazeNode(maze.start, 0)
        heappush(h,node)
        heapify(h)
        while h:
            node = heappop(h)
            maze.visitNode(node.position,msTicks)
            if (node.position == maze.end):
                break

            x = node.position[0]
            y = node.position[1]
            self.addPathAst((x, y-1), node, h)
            self.addPathAst((x, y+1), node, h)
            self.addPathAst((x-1, y), node, h)
            self.addPathAst((x+1, y), node, h)
        # finished the maze, or traversed all accessible nodes

        maze.checkLastNode(node, "A_Star")

    def addPathAst(self, (x,y), parentNode, h):
        if not self.maze.isValidPath((x,y)):
            return

        newDepth = parentNode.depth+1
        if (x,y) in self.nodeMap.keys():
            node = self.nodeMap[(x,y)]
            if node.depth > newDepth:
                # new shorter path to "node"
                node.parent = parentNode
                node.depth = newDepth
                heapify(h)
        else:
            node = AstNode((x,y), newDepth, self.maze.end)
            node.parent = parentNode
            heappush(h,node)
            self.nodeMap[(x,y)] = node

    
    def BFS(self, msTicks):
        maze = self.maze
        self.nodeMap = {}
        q = Queue.Queue()
        node = MazeNode(maze.start, 0)
        q.put(node)

        while not q.empty():
            node = q.get()
            maze.visitNode(node.position,msTicks)
            if (node.position == maze.end):
                break

            x = node.position[0]
            y = node.position[1]
            self.addPathBfs((x, y-1), node, q)
            self.addPathBfs((x, y+1), node, q)
            self.addPathBfs((x-1, y), node, q)
            self.addPathBfs((x+1, y), node, q)
        # finished the maze, or traversed all accessible nodes

        maze.checkLastNode(node, "BFS")

    def addPathBfs(self, (x,y), node, q):
        if not self.maze.isValidPath((x,y)):
            return

        if (x,y) in self.nodeMap.keys():
            return

        newNode = MazeNode((x,y), node.depth+1)
        newNode.parent = node
        q.put(newNode)
        self.nodeMap[(x,y)] = 1
    # end BFS solver

myMaze = Maze("m51t.bmp")
solver = Solver(myMaze)
#solver.DFS(5)
#solver.BFS(2)
solver.AStar(2)
