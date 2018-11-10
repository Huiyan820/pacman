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


"Feature extractors for Ghost Agent game states"

from game import Directions, Actions
import util
from util import manhattanDistance


class GhostFeatureExtractor:
    def getFeatures(self, state, action, agentIndex):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()


class GhostIdentityExtractor(GhostFeatureExtractor):
    def getFeatures(self, state, action,agentIndex):
        feats = util.Counter()
        feats[(state, action)] = 1.0
        return feats


def closestFood(pacman_pos, food, walls):
    fringe = [(pacman_pos[0], pacman_pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        if food[pos_x][pos_y]:
            return dist
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    return None

def totalNumberofFood(walls, food):
    totalFood = 0
    width = walls.width
    height = walls.height
    for i in range(width):
        for j in range(height):
            if food[i][j] :
                totalFood = totalFood + 1
    return totalFood


def closestCapsule(pacman_pos, capsules, walls):
    fringe = [(pacman_pos[0], pacman_pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        if (pos_x, pos_y) in capsules:
            return dist
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    return None


def stepDistance(from_pos, to_pos, walls):
    fringe = [(from_pos[0], from_pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        if (pos_x, pos_y) == (int(to_pos[0]), int(to_pos[1])):
            return dist
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    return None


 


class GhostAdvancedExtractor(GhostFeatureExtractor):
    
    
    def getFeatures(self, state, action, agentIndex):

        ghostState = state.getGhostState(1)
        ghostPositions = state.getGhostPositions()
        
        ghostPosition1 = state.getGhostPosition(1)
        ghostPosition2 = state.getGhostPosition(2)

        capsule = state.getCapsules()
        dx, dy = Actions.directionToVector(action)
        pacmanPosition = state.getPacmanPosition()
        isScared = ghostState.scaredTimer > 0
        food = state.getFood()

        walls = state.getWalls()
        features = util.Counter()
        pacman_x, pacman_y = pacmanPosition
        
        #Feature 1: average distance between ghost to pacman
        #--------------------------------------------------------------------------------------------------
        # closestghost = sum([stepDistance((ghost[0]+dx,ghost[1]+dy),pacmanPosition, walls) for ghost in ghostPositions])/len(ghostPositions)
        # if closestghost is not None:
        #     features["closest-ghost"] = float(closestghost) / (walls.width * walls.height)*10
        if (agentIndex==1):
            distanceFromAgent1toPac = stepDistance((ghostPosition1[0]+dx,ghostPosition1[1]+dy),pacmanPosition,walls)
            if distanceFromAgent1toPac is not None:
                features["dist1-to-pac"] = float( distanceFromAgent1toPac) / (walls.width * walls.height)*10
        
        if (agentIndex==2):
            distanceFromAgent2toPac = stepDistance((ghostPosition2[0]+dx,ghostPosition2[1]+dy),pacmanPosition,walls)
            if distanceFromAgent2toPac is not None:
                features["dist2-to-pac"] = float( distanceFromAgent2toPac) / (walls.width * walls.height)*10

        
        #Feature 2: distance between pacman to capsule
        #--------------------------------------------------------------------------------------------------
        distFromPacmanToCapsule = closestCapsule(pacmanPosition,capsule,walls) 
        if distFromPacmanToCapsule is not None:
            features["distance-pacman-capsule"] = float(distFromPacmanToCapsule) / (walls.width * walls.height)*10
            if(distFromPacmanToCapsule<10 or isScared):
                features["run"] = 20
            else:
                features["run"] = 0
            
        #Feature 4: distance between ghost
        disBetweenGhost = stepDistance(ghostPosition1,ghostPosition2,walls)
        if  disBetweenGhost is not None and disBetweenGhost!=0 :
            features["distance-between-ghosts"] = 0.5/(disBetweenGhost + 1)


        #Feature 5: minimum distance between pacman to food
        #--------------------------------------------------------------------------------------------------
        total_food = totalNumberofFood(walls, food)
        dist_closestFood = closestFood((pacman_x, pacman_y), food, walls)
        features["distance-to-food"] = (((96 - total_food) / 96) * (0.9 ** dist_closestFood)) + 0.1

        #Feature 6: the number of exits
        # actions = Actions.getLegalNeighbors((pacman_x, pacman_y), walls)-1
        # numOfValidActions = len(actions)
        # if(numOfValidActions==2):
        #     for a in actions: 
        #         dx, dy = Actions.directionToVector(a)

                


            
        #print(numOfValidActions)
        #else:
        




        
        features.divideAll(10.0)
        return features


    def scaredGhost(self, state, agentIndex, legalActions):
        ghostPosition = state.getGhostPosition(agentIndex)
        ghostState = state.getGhostState(agentIndex)
        pacmanPosition = state.getPacmanPosition()
        isScared = ghostState.scaredTimer

        if isScared <= 0:
            return None

        action = None
    
        maxDistance = float('-inf')
        if isScared > 0:
            for act in legalActions:
                dx, dy = Actions.directionToVector(act)
                newGhostPosition = (ghostPosition[0]+dx,ghostPosition[1]+dy)
                dist = util.manhattanDistance(newGhostPosition, pacmanPosition)
                if dist > maxDistance:
                    action = act
                    maxDistance = dist 
        return action