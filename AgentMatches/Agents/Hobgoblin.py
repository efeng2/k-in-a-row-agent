''' Hobgoblin.py
based on Player.py
A player for the game of K-in-a-Row (on N by M board with forbidden squares.)

The successors functions returns a pair of lists:
a list of all the new states
that can be generated from the given state, in the game
of K-in-a-Row on an M by N board with forbidden squares,
and a list of the corresponding moves.

SLT  October 19.2012, modified Nov. 17, 2024.
'''

from agent_base import KAgent
import game_types
GAME_TYPE = None
REPEAT_COUNT = 0 # Particular to this agent.
UTT_COUNT = 0

class OurAgent(KAgent):

    def __init__(self, twin=False):
        self.twin = twin
        self.nickname = 'Hobby'
        if twin: self.nickname = "Hooh-Boy"
        self.long_name = 'Hobby Hobgoblin'
        if twin: self.long_name = "Hooh-Boy Hobgoblin"
        self.my_past_utterances = None
        self.opponent_past_utterances = None
        self.repeat_count = None
        self.voice_prefs = {'Chrome': 'Google UK English Male',
   'Firefox': 'Microsoft Zira - English (United States)',
   'Edge': 'Microsoft Luke Online (Natural) - English (South Africa)',
     'pitch': 1.0}
        
    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
            self,
            game_type,
            what_side_to_play,
            opponent_nickname,
            expected_time_per_move = 0.1, # Time limits can be
                                          # changed mid-game by the game master.
            utterances_matter = True):    # If False, just return 'OK' for each utterance.


       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
       self.who_i_play = what_side_to_play
       self.opponent_nickname = opponent_nickname
       self.time_limit = expected_time_per_move
       global GAME_TYPE
       GAME_TYPE = game_type
       print("Oh, we get to play ", game_type.long_name)
       self.my_past_utterances = []
       self.opponent_past_utterances = []
       self.repeat_count = 0
       return "OK"

    def introduce(self):
        return "My name is "+self.long_name+". Am I not awfully scary?"

    def nickname(self): return self.nickname

    def make_move(self, state, lastUtterance, time_limit=1.0):
        possibleMoves = successors_and_moves(state)
        myMove = chooseMove(possibleMoves)
        myUtterance = nextUtterance()
        newState, newMove = myMove
        return [[newMove, newState], myUtterance]

# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

def other(p):
    if p=='X': return 'O'
    return 'X'

def chooseMove(statesAndMoves):
    states, moves = statesAndMoves
    if states==[]: return None
    return [states[0], moves[0]]

def successors_and_moves(state):
    b = state.board
    p = state.whose_move
    o = other(p)
    new_states = []
    moves = []
    mCols = len(b[0])
    nRows = len(b)
    #import js
    #js.alert("In runGame, OK at checkpoint A.")
    #print("In successors_and_moves, nRows is ", nRows)
    #print("In successors_and_moves, mCols is ", mCols)
    for i in range(nRows):
        for j in range(mCols):
            if b[i][j] != ' ': continue
            news = do_move(state, i, j, o)
            new_states.append(news)
            moves.append([i, j])
    return [new_states, moves]

def do_move(state, i, j, o):
            news = game_types.State(old=state)
            news.board[i][j] = state.whose_move
            news.whose_move = o
            return news
    
UTTERANCE_BANK = ["I like to scare people.",
                  "Boo!",
                  "I'd put a pumpkin on the board, if I could.",
                  "Are you scared yet?",
                  "Go ahead and freak out.",
                  "Let's play this in the dark.",
                  "I dare you to block me.",
                  "Getting tighter in here.",
                  "If this game goes on much longer, I'll turn into a pumpkin.",
                  "I am starting to feel squashy already.",
                  "My ancestors include zuchinnis.",
                  "That was a bat move!",
                  "Ichabod Crane should see this.",
                  "What next?",
                  "Do you like pumpkin pie?",
                  "If all these Xs and Os were candy, we would be ready for the trick-or-treaters.",
                  "To me, each day is Halloween Day.",
                  "No, each night is Halloween Night.",
                  "Look out for X! Look out for O! Witch is it? Witch it is!",
                  "Witches are better than wraps and 'urritos.",
                  "I need to do some more scarin'.",
                  "If ya can't beat 'em, scare 'em.",
                  "Why did the turkey come out on Halloween? Because he was a-gobblin'.",
                  "When will this game ever end",
                  "Boo-hoo, I haven't won yet."]

def nextUtterance():
    global REPEAT_COUNT, UTT_COUNT
    if REPEAT_COUNT > 1: return "I have nothing more to scare with."
    n = len(UTTERANCE_BANK)
    if UTT_COUNT == n:
        UTT_COUNT = 0
        REPEAT_COUNT += 1
    this_utterance = UTTERANCE_BANK[UTT_COUNT]
    UTT_COUNT += 1
    return this_utterance
   

def test():
    global GAME_TYPE
    GAME_TYPE = game_types.TTT
    print(GAME_TYPE)
    h = OurAgent()
    print("I am ", h.nickname)
    
    ttt = GAME_TYPE.initial_state
    print("ttt initial state: ")
    print(ttt)
    print("successors_and_moves: ")
    print(successors_and_moves(ttt))

if __name__=="__main__":
    test()

