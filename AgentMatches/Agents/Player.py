''' Player.py
A player for the game of K-in-a-Row (on N by M board with forbidden squares.)
This player is based on code from an older file called newGroundTruth.py


The successors functions returns a pair of lists:
a list of all the new states
that can be generated from the given state, in the game
of K-in-a-Row on an M by N board with forbidden squares,
and a list of the corresponding moves.

SLT  October 19.2012.
'''

def prepare(initial_state, K, what_side_I_play, opponent_nickname):
    pass

def copyBoard(b):
    return [row[:] for row in b]

def other(p):
    if p=='X': return 'O'
    return 'X'

def successors_and_moves(state):
    b = state[0]
    p = state[1]
    o = other(p)
    new_states = []
    moves = []
    mRows = len(b)
    nCols = len(b[0])
    for i in range(mRows):
        for j in range(nCols):
            if b[i][j] != ' ': continue
            b2 = copyBoard(b)
            b2[i][j] = p
            new_states += [[b2, o]]
            moves.append([i, j])
    return [new_states, moves]

def chooseMove(statesAndMoves):
    states, moves = statesAndMoves
    if states==[]: return None
    return [states[0], moves[0]]

def introduce():
    return "I am Kaylen, the Krazy K-in-a-Row player, written by tanimoto."

def nickname(): return "Kaylen"

def makeMove(state, lastUtterance, timeLimit):
    possibleMoves = successors_and_moves(state)
    myMove = chooseMove(possibleMoves)
    myUtterance = "So there!"
    newState, newMove = myMove
    return [[newMove, newState], myUtterance]

def test():
    ttt = 3*[[' ',' ',' ']]
    print("ttt initial state: ")
    print(ttt)
    print("successors_and_moves: ")
    print(successors_and_moves([ttt, 'X']))

#test()

