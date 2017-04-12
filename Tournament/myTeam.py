# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint
import distanceCalculator
from distanceCalculator import Distancer

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed, first = 'OffensiveReflexAgent',second ='OffensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
class firstAgent(CaptureAgent):  
  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team we're on).
    A distanceCalculator instance caches the maze distances 
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)
    IMPORTANT: This method may run for at most 15 seconds.
    """
    CaptureAgent.registerInitialState(self,gameState)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else: return successor
  
  def chooseAction(self, gameState):
    #Picks among the actions with the highest Q(S,A.
    actions = gameState.getLegalActions(self.index)
    d = {self.evaluate(gameState, a):a for a in actions if a != Directions.STOP}
    return d[max(d.keys())]
  
  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    w = self.getWeights(gameState, action) 
    f = self.getFeatures(gameState, action)
    return f * w

class OffensiveReflexAgent(firstAgent):
  
  def getDefensiveFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()
    
    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
      
    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction\
]
    if action == rev: features['reverse'] = 1
    return features


  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    
    features['successorScore'] = self.getScore(successor)
    #Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      
      #my positoon
      myPos = successor.getAgentState(self.index).getPosition()
      #print('myPos', myPos)

      foodDefending = self.getFoodYouAreDefending(successor).asList()
      features['distanceToMyFood'] = min([self.getMazeDistance(myPos, foodPos) for foodPos in foodDefending])
    
      features['distanceToFood'] = min([self.getMazeDistance(myPos, foodPos) for foodPos in foodList])
      #print('features[\'distanceToFood\']', features['distanceToFood'])
      #get capsules
      capsules = gameState.getCapsules()
      features['capsules'] = 0
      if myPos in capsules and successor.getAgentState(self.index).isPacman: features['capsules'] = 1
      #get enemies
      enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]      
      #get enemy positions
      enemyPos = [e.getPosition() for e in enemies]
      
      #print pos
      #print('agentPos',successor.getAgentPosition(self.index))
      agentPos = successor.getAgentPosition(self.index)
      
      #print('enemyPos', enemyPos)
      #distance to each enemy
      eDis = [self.getMazeDistance(myPos,ePos) for ePos in enemyPos if ePos!= None]
      features['enemydistance'] = 0 if len(eDis) == 0 else  min(eDis)
      scared = [ self.getMazeDistance(myPos, e.getPosition()) for e in enemies if e.getPosition() != None and  e.scaredTimer > 2] #self.getMazeDistance(myPos,e.getPosition())]

      
      if successor.getAgentState(self.index).isPacman:
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        ghosts  = [a for a in enemies if not a.isPacman and a.getPosition() != None]
        if len(ghosts) > 0:
          #for a in ghosts:
          s = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts if a.scaredTimer >0]
          features['scaredGhost'] = min([ d for d in s]) if len(s) > 0 else 0 
          reg = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts if a.scaredTimer == 0]
          features['ghostDistance'] = min([d for d in reg]) if len(reg) > 0 else 0
      #check weather to do defense or offense
      #features['onDefense'] = 0
      #get Invaders
      #check if scared ghost is around if it is set scared value so we know to go eat it.
        #if enemy is scared
      if len(scared) > 0: features['scaredDistance'] = min(scared)
      else: features['scared'] = 0
        
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      features['numInvaders'] = len(invaders)
      #print('invaders count', len(invaders))
      #features['onDefense'] = 0
      if len(invaders) > 0:
        #return self.getDefensiveFeatures(gameState,action)
        features['onDefense'] = 1
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
        features['invaderDistance'] = min(dists)
          
    return features


  def getWeights(self, gameState, action):
    if(self.getFeatures(gameState,action)['onDefense'] == 1):
      return {'numInvaders': -1000,
              'onDefense': 100,
              'invaderDistance': -10,
              'stop': -100,
              'reverse': -2,
              #'ghostDistance': -1,
              #'scaredGhost': 2,
              #'successorScore': 100
              }
    
    return {'successorScore': 100,
            'distanceToFood': -3, 
            'capsules':100,
            'invaderDistance': .5,
            'ghostDistance': -1,
            'scaredGhost': 2
            }


#################3
#cide below here not used, used for different combination

  '''
  def getWeights(self, gameState, action):
    ##defensive weights
    if(self.getFeatures(gameState,action)['onDefense'] == 1):
      return {'numInvaders': -1000,
              'onDefense': 100,
              'invaderDistance': -500, #-300 18/20
              'stop': -100,
              'reverse': -2,
              'scared' : 10,
              'successorScore': 100
              }#10
    #offensive weights
    return  {'successorScore': 100,
             'distanceToFood': -1, 
             'scared': 1,
             #'enemydistance': 1 if gameState.getAgentState(self.index).scaredTimer ==0 else -1
            }#10
  '''




##

###############################
################################
'''CODE BELOW NOT USED ALTERNATE AGENT ON PREVIOUS APPROACH'''



##############################
class allOffensiveReflexAgent(firstAgent):
  
  def getDefensiveFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()
    
    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
      
    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1
    return features


  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    
    features['successorScore'] = self.getScore(successor)
    #Compute distance to the nearest food

    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      
      #print('getPosition()',successor.getAgentState(self.index).getPosition())
      #my positoon
      myPos = successor.getAgentState(self.index).getPosition()
      #print('myPos', myPos)
      
      features['distanceToFood'] = min([self.getMazeDistance(myPos, foodPos) for foodPos in foodList])
      #print('features[\'distanceToFood\']', features['distanceToFood'])
      
      #get enemies
      enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
      #print('enemies',enemies)
      
      #get enemy positions
      enemyPos = [e.getPosition() for e in enemies]
      
      #print pos
      #print('mypos',myPos)
      #print('agentPos',successor.getAgentPosition(self.index))
      

      agentPos = successor.getAgentPosition(self.index)
      
      #print('enemyPos', enemyPos)
      #distance to each enemy
      eDis = [self.getMazeDistance(myPos,ePos) for ePos in enemyPos if ePos!= None]
      features['enemydistance'] = 0 if len(eDis) == 0 else  min(eDis)
      scared = [ self.getMazeDistance(myPos, e.getPosition()) for e in enemies if e.getPosition() != None and  e.scaredTimer > 2] #self.getMazeDistance(myPos,e.getPosition())]
      
      
      if successor.getAgentState(self.index).isPacman:
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        ghosts  = [a for a in enemies if not a.isPacman and a.getPosition() != None]
        if len(ghosts) > 0:
          for a in ghosts:
            dists = [self.getMazeDistance(myPos, a.getPosition())]
            if a.scaredTimer > 1: #self.getMazeDistance(myPos, ):
              features['scaredGhost'] = min(dists)
            else:
              features['ghostDistance'] = min(dists)
      #return features
      
      #check weather to do defense or offense
      #features['onDefense'] = 0
        
      #get Invaders
        #check if scared ghost is around if it is set scared value so we know to go eat it.
        #if enemy is scared
      if len(scared) > 0: features['scaredDistance'] = min(scared)
      else: features['scared'] = 0
        
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      features['numInvaders'] = len(invaders)
        #print('invaders count', len(invaders))
      #features['onDefense'] = 0
      if len(invaders) > 0:
        #features['onDefense'] = 1
        #return self.getDefensiveFeatures(gameState,action)
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
        features['invaderDistance'] = min(dists)
          
    return features

  
  def getWeights(self, gameState, action):
    
    return { 'successorScore': 200,
             'distanceToFood': -1, 
             'enemyDistance': -1,
             'scared': 1,
             }
