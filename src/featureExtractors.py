# featureExtractors.py
# --------------------
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


"Feature extractors for Pacman game states"

from game import Directions, Actions
import util

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state,action)] = 1.0
        return feats

class CoordinateExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closestFood(pos, food, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

def ghostScaredTime(index, state):
    return state.getGhostState(index).scaredTimer

def closestScaredGhost(pos, ghosts, walls, state):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()

    # scared_ghosts_exists = False

    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        scared_ghost_index = -1
        for p in range(len(ghosts)):
            if ghostScaredTime(p+1, state)>0:
                scared_ghosts_exists = True
                # print(ghostScaredTime(p+1, state))
            if (int(ghosts[p][0]+0.5), int(ghosts[p][1]+0.5)) == (pos_x,pos_y) and ghostScaredTime(p+1, state)>0:
                scared_ghost_index = p
                break
        if scared_ghost_index != -1:
            return dist, scared_ghost_index
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    # if scared_ghosts_exists:
    #     print (ghosts) 
    return None, None


class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features


#Added for AI project IIITB
#SimpleExtractor along with power pellet eating feature
class SimpleExtractorPellet(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a scared ghost is one step away
    - whether a non-scared ghost is one step away
    - closest scared ghost
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away

        features["#-of-scared-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(ghosts[g], walls) for g in range(len(ghosts)) if ghostScaredTime(g+1,state) >0)

        features["#-of-non-scared-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(ghosts[g], walls) for g in range(len(ghosts)) if ghostScaredTime(g+1,state) <= 0)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-non-scared-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        
        scared_ghost_dist, scared_ghost_index = closestScaredGhost((next_x,next_y), ghosts, walls, state)
        if scared_ghost_dist is not None:
            features["scaredTime-ghostDist"] = float(ghostScaredTime(scared_ghost_index+1,state))*0.5 - float(scared_ghost_dist) / (walls.width * walls.height)

        features.divideAll(10.0)



        return features

    def getFeatureDescriptions(self):
        return ["bias","run into scared ghosts 1 step away", "run into non-scared ghosts 1 step away", "eat food", "distance to closest food", "hunt scared ghost"]

    def getFeatureNames(self):
        return ["bias","#-of-scared-ghosts-1-step-away", "#-of-non-scared-ghosts-1-step-away", "eats-food", "closest-food", "scaredTime-ghostDist"]