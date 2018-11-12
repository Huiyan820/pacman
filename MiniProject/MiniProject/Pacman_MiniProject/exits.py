def martinsStupidFunction(state):
    realwalls = state.getWalls() #Gets a grid of where walls are located
    walls = realwalls.copy() #A copy of the grid which can be modified

    pacmanPos = state.getPacmanPosition()
    pacmanX, pacmanY = pacmanPos

    ghostsPositions = state.getGhostPositions() #Gets position of ghosts

    #Set ghosts as walls to easier do calculations
    for (ghostPosX, ghostPosY) in ghostsPositions:
        #print('Ghost number ', i, 'at position (', ghostPosX, ghostPosY, ')')
        ghostPosX = int(ghostPosX)
        ghostPosY = int(ghostPosY)
        walls[ghostPosX][ghostPosY] = True

    #"if we get 3 or more ways without walls it's an exit" - Ma Ding 2018

    numberOfExits = 0

    #North
    if(not walls[pacmanX][pacmanY+1]):
        numberOfExits += martinsOtherStupidFunction(walls, (pacmanX,pacmanY+1))
    #East
    if(not walls[pacmanX+1][pacmanY]):
        numberOfExits += martinsOtherStupidFunction(walls, (pacmanX+1,pacmanY))
    #South
    if(not walls[pacmanX][pacmanY-1]):
        numberOfExits += martinsOtherStupidFunction(walls, (pacmanX,pacmanY-1))
    #West
    if(not walls[pacmanX-1][pacmanY]):
        numberOfExits += martinsOtherStupidFunction(walls, (pacmanX-1,pacmanY))       

    return numberOfExits

def martinsOtherStupidFunction(walls, currentPos):
    northCount = 0
    currX, currY = currentPos
    currentNoWalls = 0
    walls[currX][currY] = True

    #print('dir:', direction)

    #North        
    if(not walls[currX][currY+1]):
        currentNoWalls += 1
    
    #East
    if(not walls[currX+1][currY]):
        currentNoWalls += 1

    #South    
    if(not walls[currX][currY-1]):
        currentNoWalls += 1

    #West        
    if(not walls[currX-1][currY]):
        currentNoWalls += 1


    #Hurray we found an exit
    #print("currentNoWalls", currentNoWalls)
    if(currentNoWalls>=2):
        return 1

    if(currentNoWalls == 0):
        return 0
    #Else continue recursively lah

    #North
    if(not walls[currX][currY+1]):
        martinsOtherStupidFunction(walls, (currX,currY+1))
    
    #East
    if(not walls[currX+1][currY]):
        martinsOtherStupidFunction(walls, (currX+1,currY))

    #South
    if(not walls[currX][currY-1]):
        martinsOtherStupidFunction(walls, (currX,currY-1))

    #West
    if(not walls[currX-1][currY]):
        martinsOtherStupidFunction(walls, (currX-1,currY))                

    return 0


# FOR POSITION
# NOT WORKING
# AS INTENDED!!!!!!!!!!!!!!!!!


def PosStupidFunction(state):
    realwalls = state.getWalls() #Gets a grid of where walls are located
    walls = realwalls.copy() #A copy of the grid which can be modified

    pacmanPos = state.getPacmanPosition()
    pacmanX, pacmanY = pacmanPos

    ghostsPositions = state.getGhostPositions() #Gets position of ghosts

    #Set ghosts as walls to easier do calculations
    for (ghostPosX, ghostPosY) in ghostsPositions:
        #print('Ghost number ', i, 'at position (', ghostPosX, ghostPosY, ')')
        ghostPosX = int(ghostPosX)
        ghostPosY = int(ghostPosY)
        walls[ghostPosX][ghostPosY] = True

    #"if we get 3 or more ways without walls it's an exit" - Ma Ding 2018

    numberOfExits = 0

    exitList = []

    #North
    if(not walls[pacmanX][pacmanY+1]):
        exitList.append(PosOtherStupidFunction(walls, (pacmanX,pacmanY+1)))
        #numberOfExits += martinsOtherStupidFunction(walls, pacmanPos)
    #East
    if(not walls[pacmanX+1][pacmanY]):
        exitList.append(PosOtherStupidFunction(walls, (pacmanX+1,pacmanY)))
    #South
    if(not walls[pacmanX][pacmanY-1]):
        exitList.append(PosOtherStupidFunction(walls, (pacmanX,pacmanY-1)))
    #West
    if(not walls[pacmanX-1][pacmanY]):
        exitList.append(PosOtherStupidFunction(walls, (pacmanX-1,pacmanY)))       

    return exitList

def PosOtherStupidFunction(walls, currentPos):
    northCount = 0
    currX, currY = currentPos
    currentNoWalls = 0
    walls[currX][currY] = True

    #print('dir:', direction)

    #North        
    if not walls[currX][currY+1]:
        currentNoWalls += 1
    
    #East
    if not walls[currX+1][currY]:
        currentNoWalls += 1

    #South    
    if not walls[currX][currY-1]:
        currentNoWalls += 1

    #West        
    if not walls[currX-1][currY]:
        currentNoWalls += 1


    #Hurray we found an exit
    #print("currentNoWalls", currentNoWalls)
    if(currentNoWalls>=2):
       # print("currentNoWalls", currentNoWalls)
        print('pls work', currentPos)
        return currentPos

    if(currentNoWalls == 0):
        return None #return None?
    #Else continue recursively lah

    #North
    if(not walls[currX][currY+1]):
        PosOtherStupidFunction(walls, (currX,currY+1))
    
    #East
    if(not walls[currX+1][currY]):
        PosOtherStupidFunction(walls, (currX+1,currY))

    #South
    if(not walls[currX][currY-1]):
        PosOtherStupidFunction(walls, (currX,currY-1))

    #West
    if(not walls[currX-1][currY]):
        PosOtherStupidFunction(walls, (currX-1,currY))                

    return None    