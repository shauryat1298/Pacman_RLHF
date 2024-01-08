# qlearningAgents.py
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
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math,sys
from query import *

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

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
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        action = self.computeActionFromQValues(state)
        if action!= None:
          return self.getQValue(state,action)

        return 0.0
        

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legalActions = self.getLegalActions(state)
        max_action = None
        max_value = -sys.maxint-1
        for a in legalActions:
          cur_val = self.getQValue(state, a)
          if max_value <= cur_val:
            max_value = cur_val
            max_action = a

        return max_action


        

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terpython pacman.py -p ApproximateQAgent -x 2000 -n 2010 -l smallGrid 
minal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        if len(legalActions)>0:
          explore = util.flipCoin(self.epsilon)
          if explore == True:
            action = random.choice(legalActions)
          else:
            action = self.getPolicy(state)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


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
        self.weights = util.Counter()
      

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """

        q_val = 0
        features = self.featExtractor.getFeatures(state, action)
        
        for f in features:
          q_val+=self.weights[f]*features[f]


        return q_val


    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        diff = (reward + self.discount*self.getValue(nextState)) - self.getQValue(state, action)

        features = self.featExtractor.getFeatures(state, action) 
        for f in features:
          self.weights[f] += self.alpha*diff*features[f]


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        # print "\nFeature weights: "
        # print self.weights
        # print "\n"
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            pass




class ApproximateQAgentFeedback(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()
        self.query_budget = 3
        self.use_queries = None
        self.explore = None
        self.write_to_file = None
        self.read_from_file = None

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """

        q_val = 0
        features = self.featExtractor.getFeatures(state, action)
        
        for f in features:
          q_val+=self.weights[f]*features[f]

        if self.read_from_file == None:
          print self.weights
          print "Enter t to read from file, f otherwise"
          option = raw_input()
          if option == "t":
            self.read_from_file = True
          else:
            self.read_from_file = False

        if self.read_from_file == True:
          dict = read_from_file()
          weights = util.Counter()
          for f in dict:
            weights[f] = dict[f]
          self.weights = weights
          self.read_from_file = False


        return q_val


    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        diff = (reward + self.discount*self.getValue(nextState)) - self.getQValue(state, action)

        features = self.featExtractor.getFeatures(state, action) 
        for f in features:
          self.weights[f] += self.alpha*diff*features[f]


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        print "\nFeature weights: "
        print self.weights
        print "\n"
        PacmanQAgent.final(self, state)



        if self.write_to_file == None:
          print "Enter t to write to file, f otherwise"
          option = raw_input()
          if option == "t":
            self.write_to_file = True
          else:
            self.write_to_file = False

        if self.explore == None:
          print "Enter t to explore, f otherwise"
          option = raw_input()
          if option == "t":
            self.explore = True
          else:
            self.explore = False
            self.epsilon = 0

        if self.use_queries == None:
          print "Enter t to use queries, f otherwise"
          option = raw_input()
          if option == "t":
            self.use_queries = True
          else:
            self.use_queries = False

        if self.query_budget == 0:
          self.epsilon = 0

        if self.use_queries == True:
          if self.query_budget>0:
            self.query_budget-=1

            feature_names = self.featExtractor.getFeatureNames()
            query_list = queryUser(self.featExtractor.getFeatureDescriptions())


            for i in range(len(query_list)):
              weight_update = self.queryWeightIncrement(self.weights[feature_names[i]], query_list[i])
              if weight_update != None:
                self.weights[feature_names[i]]+= weight_update

            print "\nFeature weights after update: "
            print self.weights
            print "\n"


        if self.write_to_file:
          write_to_file(self.weights)


        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            pass
    def queryWeightIncrement(self, weight, sign):

        if weight == 0.0:
          weight = 2.0

        weight_mod = abs(weight)
        weight_increment = weight_mod/2

        if weight>0 and weight<2 and sign == "-":
          weight_incremet = -2*weight

        if weight < 0 and weight > -2 and sign == "+":
          weight_increment = -2*weight

        if sign == "+":
          return weight_increment
        elif sign == '-':
          return -weight_increment

