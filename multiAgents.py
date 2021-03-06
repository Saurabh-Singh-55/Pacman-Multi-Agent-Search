# multiAgents.py
# --------------
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood=  currentGameState.getFood()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        for ghostState in newGhostStates:
          if util.manhattanDistance(ghostState.getPosition(),newPos)<2:
            return float("-inf")
        if oldFood[newPos[0]][newPos[1]]:
          return 100000
        i=random.choice([1,1,2])
        if i==1:
          return 0
        else:
          a=100000
          y=()
          x=list(newFood.asList())
          for food in x:
            if(a>util.manhattanDistance(food,newPos)):
              a=util.manhattanDistance(food,newPos)
              y=food
          return 100000-util.manhattanDistance( y,newPos)
        return successorGameState.getScore()

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
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        a = Directions.EAST
        legalMoves = gameState.getLegalActions(0)
        for action in legalMoves:
          x= self.value([gameState.generateSuccessor(0, action),0],1)
          if v < x:
            v = x
            a = action
        return a

    def value(self,state,agentIndex):
      if state[0].isWin() or state[0].isLose() or self.depth == state[1]:
        return self.evaluationFunction(state[0])
      if agentIndex == 0 :
        return self.maxValue(state)
      else :
        return self.minValue(state,agentIndex)

    def minValue(self,state,agentIndex):
      v = float("inf")
      for action in state[0].getLegalActions(agentIndex):
        if agentIndex == state[0].getNumAgents()-1:
          v = min( v, self.value( [state[0].generateSuccessor(agentIndex, action),state[1]+1] ,0) )
        else:
          v = min( v, self.value( [state[0].generateSuccessor(agentIndex, action),state[1]] ,agentIndex+1 ))
      return v

    def maxValue(self,state):
      v = float("-inf")
      for action in state[0].getLegalActions(0):
        v = max( v, self.value([state[0].generateSuccessor(0, action),state[1]] ,1))
      return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        a = Directions.EAST
        alpha=float("-inf")
        beta=float("inf")
        legalMoves = gameState.getLegalActions(0)
        for action in legalMoves:
          x= self.value([gameState.generateSuccessor(0, action),0],1,alpha,beta)
          if v < x:
            v = x
            a = action
          alpha = max(alpha, v)
        return a

    def value(self,state,agentIndex,alpha,beta):
      if state[0].isWin() or state[0].isLose() or self.depth == state[1]:
        return self.evaluationFunction(state[0])
      if agentIndex == 0 :
        return self.maxValue(state,alpha,beta)
      else :
        return self.minValue(state,agentIndex,alpha,beta)
    
    def maxValue(self,state,a,b):
      v = float("-inf")
      for action in state[0].getLegalActions(0):
        v = max( v, self.value([state[0].generateSuccessor(0, action),state[1]] ,1,a,b))
        if v>b  :
          return v
        a=max(a,v)
      return v     

    def minValue(self,state,agentIndex,a,b):
      v = float("inf")
      for action in state[0].getLegalActions(agentIndex):
        if agentIndex == state[0].getNumAgents()-1:
          v = min( v, self.value( [state[0].generateSuccessor(agentIndex, action),state[1]+1],0,a,b) )
        else:
          v = min( v, self.value( [state[0].generateSuccessor(agentIndex, action),state[1]],agentIndex+1,a,b) )
        if v<a:
          return v
        b=min(b,v)
      return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        a = Directions.EAST
        legalMoves = gameState.getLegalActions(0)
        for action in legalMoves:
          x= self.value([gameState.generateSuccessor(0, action),0],1)
          # print(action)
          # print(x)
          if v < x:
            v = x
            a = action
          elif v==x:
            if a == Directions.STOP:
              a = action
        # print("/////////////")
        # print(a)
        return a

    def value(self,state,agentIndex):
      if state[0].isWin() or state[0].isLose() or self.depth == state[1]:
        return self.evaluationFunction(state[0])
      if agentIndex == 0 :
        return self.maxValue(state)
      else :
        return self.expValue(state,agentIndex)

    def expValue(self,state,agentIndex):
      avg=0
      v = float("inf")
      l=state[0].getLegalActions(agentIndex)
      for action in state[0].getLegalActions(agentIndex):
        if agentIndex == state[0].getNumAgents()-1:
          avg = avg + min( v, self.value( [state[0].generateSuccessor(agentIndex, action),state[1]+1] ,0) )
        else:
          avg = avg + min( v, self.value( [state[0].generateSuccessor(agentIndex, action),state[1]] ,agentIndex+1 ))
      return avg

    def maxValue(self,state):
      v = float("-inf")
      for action in state[0].getLegalActions(0):
        v = max( v, self.value([state[0].generateSuccessor(0, action),state[1]] ,1))
      return v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    Food=  currentGameState.getFood()
    pallet = currentGameState.getCapsules()
    value=0
    g=0
    startPosition = currentGameState.getPacmanPosition()
    from util import Queue
    s=Queue()
    start=startPosition
    visited_state=[start]
    data=[[start],[],0]
    s.push(data)
    while not s.isEmpty():
        current=s.pop()
        current_node=current[0][-1]
        if current_node in pallet:
            value= current[2]
            break
        if Food[current_node[0]][current_node[1]]==True:
            value = current[2]
            break
        for ghostState in newGhostStates:
          if current_node==ghostState.getPosition():
              g =min(g,current[2])
              for ghost in newScaredTimes:
                if ghost>0:
                  return -(value + g*1000)+currentGameState.getScore()
        
        node=current_node
        w = currentGameState.getWalls()
        nodes=[]
        if w[node[0]][node[1]+1]==False:
            nodes.append( [ (node[0],node[1]+1),Directions.EAST,1 ] )
        if w[node[0]][node[1]-1]==False:
            nodes.append( [ (node[0],node[1]-1),Directions.EAST,1 ] )
        if w[node[0]+1][node[1]]==False:
            nodes.append( [ (node[0]+1,node[1]),Directions.EAST,1 ] )
        if w[node[0]-1][node[1]]==False:
            nodes.append( [ (node[0]-1,node[1]),Directions.EAST,1 ] )

        for leaf in nodes:
            next_state=leaf[0]
            next_direction=leaf[1]
            next_cost=leaf[2]
            if next_state not in visited_state:
                visited_state.append(next_state)
                next_states=current[0][:]
                next_states.append(next_state)
                next_directions=current[1][:]
                next_directions.append(next_direction)
                new_cost=current[2]+next_cost
                next_data=[next_states,next_directions,new_cost]
                s.push(next_data)
    # print(value,end=">>")
    # print(g,end="^^")
    # print(currentGameState.getScore())
    # c=0
    # for f in Food:
    #   if f==True:
    #     c=c+1
    # return currentGameState.getScore() - value
    scared =0
    for ghost in newScaredTimes:
      if ghost>0:
        scared=200

    return -(value + -1*g)*3+currentGameState.getScore() + scared

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
