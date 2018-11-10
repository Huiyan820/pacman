# qlearningGhostAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningGhostAgents import ReinforcementGhostAgent
from ghostfeatureExtractors import *
import sys
import random,util,math
import pickle
class QLearningGhostAgent(ReinforcementGhostAgent):
    """
      Q-Learning Ghost Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self,epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0,agentIndex=1, extractor='GhostIdentityExtractor', **args):
        "You can initialize Q-values here..."
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        args['agentIndex'] = agentIndex
        self.index = agentIndex 
        self.q_values = util.Counter()
        
        self.featExtractor = util.lookup(extractor, globals())()
        self.weights = util.Counter()
        ReinforcementGhostAgent.__init__(self, **args)
        

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        qValue= 0.0
        features = self.featExtractor.getFeatures(state, action)
        for key in features.keys():
           	qValue += (self.weights[key] * features[key])
        
        return qValue

    def computeValueFromQValues(self, state):
        possibleActions = self.getLegalActions(state)
        if possibleActions:
            maxv = float("-inf")
            for action in possibleActions:
                q = self.getQValue(state, action)
                if q >= maxv:
                    maxv = q
            return maxv
        return 0.0
        
    def computeActionFromQValues(self, state):
        possibleActions = self.getLegalActions(state)
        if possibleActions:
            maxv = float("-inf")
            bestAction = None
            for action in possibleActions:
                q = self.getQValue(state, action)
                if q >= maxv:
                    maxv = q
                    bestAction = action
            return bestAction
        return None
        
    def getWeights(self):
        return self.weights


    def update(self, state, action, nextState, reward): 
        features = self.featExtractor.getFeatures(state, action)  
        print(features)
        for key in features.keys():
            self.weights[key] +=  self.alpha * ((reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action))*features[key]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        ReinforcementGhostAgent.final(self, state) 
        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            print(self.agentIndex,"  :", self.weights)
            #sys.exit(1)
            pass

    def getAction(self, state):
        #Uncomment the following if you want one of your agent to be a random agent.
        action = None
        #if self.agentIndex == 1:
            #action = random.choice(self.getLegalActions(state))
        #else: 
        if random.uniform(0,1) < self.epsilon:
            action = random.choice(self.getLegalActions(state))
        else:
            action = self.computeActionFromQValues(state)

        self.doAction(state, action)
        return action
  

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


    