def isTerminal(gameboard): #checks for terminal state
    for i in range(3):
        if gameboard[i][0] != 0 and gameboard[i][0] == gameboard[i][1] and gameboard[i][0] == gameboard[i][2]:
            return (True, gameboard[i][0])
        if gameboard[0][i] != 0 and gameboard[0][i] == gameboard[1][i] and gameboard[0][i] == gameboard[2][i]:
            return (True, gameboard[0][i])
    if gameboard[1][1] != 0 and gameboard[0][0] == gameboard[1][1] and gameboard[0][0] == gameboard[2][2]:
        return (True, gameboard[1][1])
    if gameboard[1][1] != 0 and gameboard[0][2] == gameboard[1][1] and gameboard[0][2] == gameboard[2][0]:
        return (True, gameboard[1][1])
    return (False, "")

valid_pairs = [[(0,0), (1,0)], 
               [(0,0), (0,1)],
               [(0,0), (1,1)],
               [(0,1), (1,1)],
               [(0,1), (0,2)],
               [(0,2), (1,1)],
               [(0,2), (1,2)],
               [(1,0), (1,1)],
               [(1,0), (2,0)],
               [(1,1), (1,2)],
               [(1,1), (2,1)],
               [(1,1), (2,0)],
               [(1,1), (2,2)],
               [(1,2), (2,2)],
               [(2,0), (2,1)],
               [(2,1), (2,2)],
               [(0,0), (0,2)],
               [(0,0), (2,0)],
               [(0,2), (2,2)],
               [(2,0), (2,2)],
               [(0,0), (2,2)],
               [(0,2), (2,0)],]

def numStates(gameboard):
    res = 0
    for row in gameboard:
        for pos in row:
            if pos == 0:
                res += 1
    return res

def heuristics(gameboard, initial):
    state, player = isTerminal(gameboard)
    value = 0
    if state == True and player == 2:
        value -= 5000
    elif state == True and player == 1:
        value += 10000
    current = numStates(gameboard)
    value -= (initial - current) * 100
    for placement in valid_pairs:
        x1, y1 = placement[0]
        x2, y2 = placement[1]
        if gameboard[x1][y1] == gameboard[x2][y2] and gameboard[x1][y1] != 0:
            if gameboard[x1][y1] == 2:
                value -= 10
            else:
                value += 10
    return value

def nextActions(gameboard, player):
    positions = []
    for i in range(9):
        if gameboard[i // 3][i % 3] == 0:
            positions.append([player, (i // 3, i % 3)])
    return positions 

def updateGame(gameboard, action):
    x = action[1][1]
    y = action[1][0]
    gameboard[y][x] = action[0]
    return gameboard

def revert(gameboard, action):
    x = action[1][1]
    y = action[1][0]
    gameboard[y][x] = 0
    return gameboard


def TTC(state):
    gameboard = [[int(state[0]), int(state[1]), int(state[2])], 
                 [int(state[3]), int(state[4]), int(state[5])], 
                 [int(state[6]), int(state[7]), int(state[8])]]
    initial = numStates(gameboard)
    if initial == 9:
        move = [1, (1, 1)]
    else:
        (value, move) = maxplayer(gameboard, -10000, 10000, 4, initial)
        print(move)
    return move

def prettyprint(gameboard):
    for row in gameboard:
        print(row)

def maxplayer(gameboard, alpha, beta, depth, initial):

    terminal = isTerminal(gameboard)[0]
    if depth == 0 or terminal == True or initial == 0:
        return heuristics(gameboard, initial), ""
    v, move = -10000, ""

    for action in nextActions(gameboard, 1):
        if alpha == 5000:
            break
        v2, a2 = minplayer(updateGame(gameboard, action), alpha, beta, depth - 1, initial - 1)
        revert(gameboard, action)
        if v2 > v:
            v, move = v2, action
            alpha = max(alpha, v)
        if v >= beta:
            return (v, move)
    
    return (v, move)

def minplayer(gameboard, alpha, beta, depth, initial):

    terminal = isTerminal(gameboard) [0]
    if depth == 0 or terminal == True or numStates(gameboard) == 0:
        return heuristics(gameboard, initial), ""
    
    v, move = 10000, ""
    for action in nextActions(gameboard, 2):
        v2, a2 = maxplayer(updateGame(gameboard, action), alpha, beta, depth - 1, initial - 1)
        revert(gameboard, action)
        if v2 < v:
            v, move = v2, action
            beta = min(beta, v)
        if v <= alpha:
            return (v, move)
    return (v, move)

#gameboard is a 2d array
#print(TTC("000000000"))

