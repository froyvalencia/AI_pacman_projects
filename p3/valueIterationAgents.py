# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0
    """Description:
    Idea:
    call on -> v_i+1(s) <- max_a Sigma_s' T(s,a,s') * [ R(s,a,s') + Gama * V_i(s') ]
    Thow out old Vi values
    This is called a value update or Bellman update
    Repeat until convergence
    Basic idea: approximations get refined towards optimal values
    """
    for _ in range(self.iters):
      vals = util.Counter()
      for s in self.mdp.getStates():
        max_val = float('-inf')
        for a in mdp.getPossibleActions(s):
          max_val = max(max_val, self.getQValue(s,a))
          vals[s] = max_val
      self.values = vals

  def getValue(self, state):
    """
    Return the value of the state (computed in __init__).
    """    
    return self.values[state]

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
      
      Description:
      we are give state and action that is being taken
      we must calculate a Q value based on each possible outcome 
      from taking an action.
      T(s,a,s') = P(s'|s,a) i.e. probability that taking action a from s leads to s'
      Q(s,a) = Sigma_s' T(s,a,s') * [ R + gama * V*(s') ] 
    """
    return sum(T*(self.mdp.getReward(state,action,S)+self.discountRate*self.values[S]) for S,T in self.mdp.getTransitionStatesAndProbs(state,action))
    '''
    #non pythonic version
    Q = 0
    for S, T in self.mdp.getTransitionStatesAndProbs(state, action):#print('S',S)# print('T', T)                
    R = self.mdp.getReward(state, action, S) 
    R(s,a,s')#print('R',R)#print('V*(S)',self.values[S])
    Q += T * (R + self.discountRate * self.values[S]) #print('Q',Q)
    return Q
    '''
  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    
      Description:
      We want to get the optimal choice here
      for each action get the q-value so that we can decide
      which choice is the best then call argMax on 
    """
    return util.Counter({a:self.getQValue(state,a) for a in self.mdp.getPossibleActions(state)}).argMax()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
