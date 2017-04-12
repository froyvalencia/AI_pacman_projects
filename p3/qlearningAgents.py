# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue /
      - getAction
      - getValue
      - getPolicy 
      - update /

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    self.qValues = util.Counter()
    

  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description
    
    """
    return self.qValues[(state,action)]

  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    """Description:
    """
    legalActions = self.getLegalActions(state)
    if not legalActions: return 0.0
    return max(self.getQValue(state, a) for a in legalActions)

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    """Description:
    we keep our temp max value while
    we encounter any that are equivalent we append
    if find a larger q value we reset the current action list 
    return a random choice from the current action list
    """
    legalActions = self.getLegalActions(state)
    if not legalActions: return None
    max = None
    curr = []
    for a in legalActions:
      q = self.getQValue(state, a)
      if max ==  None or q > max:
        max = q
        curr = [a]
      elif q == max: 
        curr.append(a)
    return random.choice(curr)

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    Description:
    returns none if no legalactions
    selects between random actionm or getPolicy  based on flipCoin 
    """
    legalActions = self.getLegalActions(state)
    if not legalActions: return None
    return random.choice(legalActions) if util.flipCoin(self.epsilon) else self.getPolicy(state)
  
  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    
    """Description:
    sets the value at a state action key pair
    """
    self.qValues[(state, action)] = reward + self.discountRate * self.getValue(nextState)

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)
    # You might want to initialize weights here.
    self.weights = util.Counter()

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
      """
    """Description:
    return the QValue for state action pair
    Q(s,a) = sigma i->n f_i (s,a)*w_i
    """
    return sum(self.weights[f] * v for f, v in self.featExtractor.getFeatures(state, action).items())
  
  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
    correction = [R(s,a) + gama * V(s') ] - Q(s,a)
    wi = w_i + alpha[correction]fi(s,a)
    """
    for f, v in self.featExtractor.getFeatures(state, action).items():
      self.weights[f] += self.alpha*(reward+self.discountRate*self.getValue(nextState)-self.getQValue(state, action))*v
      
  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)
    
    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      print('weights',self.weights)
