# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0
  """Description:
  
  """
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = -2 
  """Description:
  make it expensive to keep living
  """
  return answerDiscount, answerNoise, answerLivingReward
# If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.5
  answerNoise = 0.4
  answerLivingReward = -1.5
  """Description:
  [Enter a description of what you did here.]
  
  """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = -.9
  """Description:
  [Enter a description of what you did here.]
  make it expensive to keep living
  """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  didnt change anything this was given path at start
  """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 10
  """Description:
  give large living reward and it will avoid both exits forever
  """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = None
  answerLearningRate = None
  """Description:
  [Enter a description of what you did here.]
  
  """
  return 'NOT POSSIBLE'
  #return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
