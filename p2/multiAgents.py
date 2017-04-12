# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """

  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()
    #print(legalMoves)

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    #print("scores", scores)
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]

    #print("best indices,", bestIndices)
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    "Add more of your code here if you want to"
    return legalMoves[chosenIndex]# if legalMoves[chosenIndex] != "Stop" else legalMoves[chosenIndex -1 if chosenIndex > 1 else chosenIndex + 1]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodPositions = oldFood.asList()
    "*** YOUR CODE HERE ***"
    #print("foodPositions",foodPositions)
    #print("oldFood",oldFood)
    #print("successorGameState",successorGameState)
    #print("newPosition",newPosition)
    #print("newGhostStates",newGhostStates)
    #for x in newGhostStates:
     #print(x)
    #print("newScaredTimes",newScaredTimes)
    #get position of food that is min distance from newPosition
    nextFood = min((pos for pos in foodPositions), key=lambda pos: util.manhattanDistance(newPosition,pos))

    
    #shortest distance to food position
    d = util.manhattanDistance(nextFood,newPosition)
    oldD = util.manhattanDistance(nextFood,currentGameState.getPacmanPosition())
    #shortest distance to a ghost
    d_g = min(util.manhattanDistance(g.getPosition(),newPosition) for g in newGhostStates)

    #win loss cases
    if successorGameState.isWin(): return float('inf')
    if successorGameState.isLose(): return float('-inf')
    if d < oldD: #make sure we are getting closer to target return value with a bonus for getting closer to target
      return successorGameState.getScore() + 100
    #if moving makes score worse find formula to see if based on number of food we are satisfied
    if successorGameState.getScore() < currentGameState.getScore(): # if worse find our how much worse depending on number of food
      return (successorGameState.getScore() + 1/(d)) * 1/(len(foodPositions)) #if d > 0 else successorGameState.getScore()
    #default return distance to nearest food if other cases are not satisfied
    return d
  '''
    FAILED ATTEMPT
    #Using both active and inactive ghost
    #avg = sum(util.manhattanDistance(newPosition,pos) for pos in foodPositions)
    scared = []
    regular = []
    for g in ghostStates:
      if g.scaredTimer > 0: scared.append(g)
      else: regular.append(g)
    minG2 = min(util.manhattanDistance(newPosition,g.getPosition()) for g in regular) if len(regular) > 0 else 1
    minG = min(util.manhattanDistance(newPosition,g.getPosition()) for g in scared) if len(scared) > 0 else 1
    capsules = len(successorGameState.getCapsules())
    diff = successorGameState.getScore() - currentGameState.getScore() + score
    return score + successorGameState.getScore() - currentGameState.getScore()
  '''



def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.treeDepth = int(depth)

#q2
class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
           The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    pacman_actions = gameState.getLegalActions(0)
    if "Stop" in pacman_actions: pacman_actions.remove("Stop")
    '''
    Reccurence from stanford ai cs slides
    V(opt,d)  which is the minimax value with search stopping at depth dmax. 
    You should express your answer in terms of the following functions: 
    IsEnd(s), which tells you if s is an end state; 
    Utility(s), the utility of a state; 
    Eval(s), an evaluation function for the state s; 
    Player(s), which returns the player whose turn it is; 
    Actions(s), which returns the possible actions; 
    and Succ(s,a), which returns the successor state resulting from taking an action at a certain state. 
    You may use any relevant notation introduced in lecture.
    '''
    #gets action that will lead to max score
    return max((action for action in gameState.getLegalActions(0)),key=lambda action: self.minValue(gameState.generateSuccessor(0,action),0,1))

  def maxValue(self,state, depth, agent):
    if self.isTerminalState(state,depth): return self.evaluationFunction(state)
    return max( self.minValue(state.generateSuccessor(agent, action), depth, agent+1) for action in state.getLegalActions(agent))

  def minValue(self, state, depth, agent):
    if self.isTerminalState(state,depth): return self.evaluationFunction(state)
    if self.isPlayer(state,agent):
      return min(self.maxValue(state.generateSuccessor(agent, action),depth+1, 0) for action in state.getLegalActions(agent))
    return min(self.minValue(state.generateSuccessor(agent, action),depth, agent+1) for action in state.getLegalActions(agent))

  def isPlayer(self,state,agent):
    return True if agent == state.getNumAgents() - 1 else False

  def isTerminalState(self,state,depth):
    return True if depth == self.treeDepth or state.isWin() or state.isLose() else False
#q3
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    a = float('-inf')
    b = float('inf')
    return max((action for action in gameState.getLegalActions(0)),key=lambda action: self.minValue(gameState.generateSuccessor(0,action),0,1,a,b))

  def maxValue(self,state, depth, agent,a,b):
    if self.isTerminalState(state,depth): return self.evaluationFunction(state)
    v = max( self.minValue(state.generateSuccessor(agent, action), depth, agent+1,a,b) for action in state.getLegalActions(agent))
    if v >= b: return v
    a = max(a,v)
    return v

  def minValue(self, state, depth, agent,a, b):
    if self.isTerminalState(state,depth): return self.evaluationFunction(state)
    if self.isPlayer(state,agent):
      v = min(self.maxValue(state.generateSuccessor(agent, action),depth+1,0,a,b) for action in state.getLegalActions(agent))
      if v <= a: return b
      b = min(v,b)
      return v
    v = min(self.minValue(state.generateSuccessor(agent, action),depth, agent+1,a,b) for action in state.getLegalActions(agent))
    if v <= a: return b
    b = min(v,b)
    return v

  def isPlayer(self,state,agent):
    return True if agent == state.getNumAgents() - 1 else False

  def isTerminalState(self,state,depth):
    return True if depth == self.treeDepth or state.isWin() or state.isLose() else False
#q4
class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    return max((action for action in gameState.getLegalActions(0)),key=lambda action: self.minValue(gameState.generateSuccessor(0,action),0,1))

  def maxValue(self,state, depth, agent):
    if self.isTerminalState(state,depth): return self.evaluationFunction(state)
    return max( self.minValue(state.generateSuccessor(agent, action), depth, agent+1) for action in state.getLegalActions(agent))

  def minValue(self, state, depth, agent):
    if self.isTerminalState(state,depth): return self.evaluationFunction(state)
    if self.isPlayer(state,agent):
      return min(self.maxValue(state.generateSuccessor(agent, action),depth+1, 0) for action in state.getLegalActions(agent))
    return sum(self.minValue(state.generateSuccessor(agent, action),depth, agent+1) for action in state.getLegalActions(agent))/len(state.getLegalActions(agent))

  def isPlayer(self,state,agent):
    return True if agent == state.getNumAgents() - 1 else False

  def isTerminalState(self,state,depth):
    return True if depth == self.treeDepth or state.isWin() or state.isLose() else False

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    Goal here is to stay away from ghost while getting closer to food pellets
    I tried a lot of constants but it worked better only using closest ghost distance and distance to furthest pellet
    subtract the far pellet since we want to be going towards it
    subtract ghost because the closer ghost is the closer we are to possible death
  """
  "*** YOUR CODE HERE ***"
  #print('current legal actions',currentGameState.getLegalActions(0))
  oldFood = currentGameState.getFood()
  foodPositions = oldFood.asList()
  # if win do
  newGhostStates = currentGameState.getGhostStates()
  g_d = min(util.manhattanDistance(currentGameState.getPacmanPosition(),g.getPosition()) for g in newGhostStates)
  if currentGameState.isWin(): return float('inf')
  # if lose dont do
  if  currentGameState.isLose(): return float('-inf')
  nextFood = max((pos for pos in foodPositions), key=lambda pos: util.manhattanDistance(currentGameState.getPacmanPosition(),pos))
  d = util.manhattanDistance(nextFood,currentGameState.getPacmanPosition())
  if g_d < 2: return float('-inf')
  return currentGameState.getScore() - d - g_d #subtract d to make score worse for further choices boonus for staying away



  '''
  FAILED ATTEMPT
  #if currentGameState.isLose(): return float('-inf')
  #if currentGameState.isWin(): return float('inf')
  # .getGhostPositions
  v = 0
  foodPositions = currentGameState.getFood().asList()
  #print(foodPositions)
  pacPos = currentGameState.getPacmanPosition()
  ghostStates = currentGameState.getGhostStates()
  for g in ghostStates:
    if g.scaredTimer > 0:
      dis = util.manhattanDistance(g.getPosition(),pacPos)
      if dis < g.scaredTimer:
        v += 500
      else:
        v -= 200
  #GameState.
  nextFood = min( (pos for pos in foodPositions), key=lambda pos: util.manhattanDistance(pacPos,pos))
  d = util.manhattanDistance(pacPos,nextFood)
  return 1 / d * len(foodPositions) + currentGameState.getScore() + v
'''


  #Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
