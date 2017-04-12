# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def startingState(self):
    """
    Returns the start state for the search problem 
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()
           


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


class Node:
    """
    Node object used for search algorithms
    """
    def __init__(self, state, parent=None, direction=None, distance=0, depth=0):
        '''
        :param state: tuple (x,y) of current state
        :param parent: parent node
        :param direction: previous direction to arrive at current state
        :param distance: total cost of path to current state
        :param depth: number of directions taken to arrive
        '''
        self.state = state
        self.parent = parent
        self.direction = direction
        self.distance = distance
        self.depth = depth

def expand(node, problem):
    """
    :param node:
    :param problem:
    :return: list of state accesible from current node state
    """
    return [ (Node(successor, node, direction, node.distance + cost, node.depth + 1)) \
             for successor, direction, cost in problem.successorStates(node.state) ]

def getPath(node, problem):
    """
    :param node:
    :param problem:
    :return: path containg
    """
    path = []
    while problem.startingState() is not node.state:
        path.insert(0,node.direction)
        node = node.parent
    return path

def graphSearch(problem, frontier):
    """
    pseudocode from book
    returns a solution, or failure initialize the frontier using the initial state of problem
    initialize the explored set to be empty
    while true:
        if the frontier is empty:
            return failure
        choose a leaf node and remove it from the frontier
        if the node contains a goal state:
            return the corresponding solution
        add the node to the explored set
        expand the chosen node, adding the resulting nodes to the frontier
        only if not in the frontier or explored set:
    """
    explored = set()
    frontier.push(Node(problem.startingState()))
    while frontier.isEmpty() is False:
        leaf = frontier.pop()
        if problem.isGoal(leaf.state):
            return getPath(leaf, problem)
        if leaf.state not in explored:
            explored.add(leaf.state)
            for child in expand(leaf, problem):
                frontier.push(child)
    return None

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  # using stack LIFO runs graph search in depth first search order
  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())
  """
  return graphSearch(problem,util.Stack())

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  return graphSearch(problem,util.Queue())

def uniformCostSearch(problem):
  "Search the node of least total cost first."
  return graphSearch(problem,util.PriorityQueueWithFunction(lambda node: node.distance))

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  return graphSearch(problem,util.PriorityQueueWithFunction(
      lambda node: node.distance + heuristic(node.state,proble)))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

