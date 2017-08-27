# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# Helper functions for search algorithms
def make_initial_node(state):
    """Make the initial node of searching"""
    return {
        "state": state,
        "action": None,
        "cost": 0,
        "prev": None
    }

def make_succ_node(current_node, succ):
    """
    Make the successor node given the current node
    and succ as a dictionary obtained from problem.GetSuccessors
    """
    return {
        "state": succ[0],
        "action": succ[1],
        "cost": succ[2],
        "prev": current_node
    }

def getActionList(node):
    """
    Get the sequence of actions from the
    beginning of the problem to the current node
    """
    actions = []
    while node["prev"]:
        actions.append(node["action"])
        node = node["prev"]
    return actions[::-1]

def search(problem, init, expand):
    """
    Perform a search algorithm with shared logic,
    it calls init function to initialise data structure for open list,
    and calls expand function to expand the current node and update the
    data structure accordingly
    """
    closed = set()
    opened = init()
    while not opened.isEmpty():
        node = opened.pop()
        if problem.isGoalState(node["state"]):
            return getActionList(node)
        if node["state"] not in closed:
            closed.add(node["state"])
            expand(node, opened)
    return None

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    ################### QUESTION 1 ###################
    # perform search with stack as the data stucture for open nodes
    def init():
        opened = util.Stack()
        opened.push(make_initial_node(problem.getStartState()))
        return opened

    def expand(node, opened):
        for succ in problem.getSuccessors(node["state"]):
            opened.push(make_succ_node(node, succ))
    
    return search(problem, init, expand)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    ################### QUESTION 2 ###################
    # perform search with queue as the data stucture for open nodes
    def init():
        opened = util.Queue()
        opened.push(make_initial_node(problem.getStartState()))
        return opened

    def expand(node, opened):
        for succ in problem.getSuccessors(node["state"]):
            opened.push(make_succ_node(node, succ))
    
    return search(problem, init, expand)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    ################### QUESTION 3 ###################
    # perform search with priority queue as the data stucture for open nodes
    # cost of actions are used as priorities
    def init():
        opened = util.PriorityQueue()
        opened.push(make_initial_node(problem.getStartState()), 0)
        return opened

    def expand(node, opened):
        for succ in problem.getSuccessors(node["state"]):
            succ = make_succ_node(node, succ)
            cost = problem.getCostOfActions(getActionList(succ))
            opened.update(succ, cost)
    
    return search(problem, init, expand)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ################### QUESTION 3 ###################
    # perform search with priority queue as the data stucture for open nodes
    # (cost + heuristic) values are used as priorities
    def init():
        opened = util.PriorityQueue()
        opened.push(make_initial_node(problem.getStartState()), 0)
        return opened

    def expand(node, opened):
        for succ in problem.getSuccessors(node["state"]):
            succ = make_succ_node(node, succ)
            cost = problem.getCostOfActions(getActionList(succ))
            heur = heuristic(succ["state"], problem)
            opened.update(succ, cost + heur)
    
    return search(problem, init, expand)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
