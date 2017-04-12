  '''
  
  def minmax(self, state):
    #returns an action
    v = float('-inf')
    print("self.treeDepth",self.treeDepth)
    return max(action for action in state.getLegalActions(0),
               lambda key= self.minvalue(state.generateSuccessor(0, action),self.treeDepth,1))

  #max will get pacmans max score possible
  def maxvalue(self, state, depth, agent):
    if(state.isWin()):
      return self.evaluationFunction(state)
    v = float('-inf')
    #for action in state.getLegalActions(agent): v = max(v,minvalue(self.minvalue(state.generateSuccessor(agent, action), depth, agent + 1))
    return max(self.minvalue(action for action in state.getLegalActions(agent), lambda key= self.minvalue(state.generateSuccessor(agent, action), depth, agent + 1))

  #min will get min possible score that ghost action could lead to
  def minvalue(self, state, depth, agent):
      if(state.isLose()): return self.evaluationFunction(state)
      if agent < state.getNumAgents(): #is ghost
        return min(self.maxvalue(state.generateSuccessor(agent, action),depth, agent + 1) for action in state.getLegalActions(agent) )
      #call om pacman
      return min(self.maxvalue(state.generateSuccessor(agent, action),depth+1, 0) for action in state.getLegalActions(agent))

  def player(self,state,agent):
    if agent == state.getNumAgents() -1: return 0
    return agent + 1
  '''
