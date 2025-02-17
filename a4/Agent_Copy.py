'''
<yourUWNetID>_KInARow.py
Authors: <your name(s) here, lastname first and partners separated by ";">
  Example:  
    Authors: Smith, Jane; Lee, Laura

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
# from game_types import State, Game_Type
import game_types
from random import randint

AUTHORS = 'Jane Smith and Laura Lee' 

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:
# Constants
BETA_DEFAULT = -10000000
ALPHA_DEFAULT = 10000000
MINIMAX_DEPTH = 2

# For utterances to change according to game state
WIN_THRESHOLD = 100000
LOSE_THRESHOLD = 100000
NUETRAL_THRESHOLD = 5000




class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'OurAgent'
        if twin: self.nickname += '2'
        self.long_name = 'IBOT3000'
        if twin: self.long_name += ' II'
        self.persona = 'bland'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

        self.initial_turn = True
        self.kInARowSet = {}
        self.coodinateDict = {}

    def introduce(self):
        intro = 'HELLO I AM TEST BOT'
        if self.twin: intro += " TOO"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1, # Time limits can be
                                      # changed mid-game by the game master.

        utterances_matter=True):      # If False, just return 'OK' for each utterance,
                                      # or something simple and quick to compute
                                      # and do not import any LLM or special APIs.
                                      # During the tournament, this will be False..
       if utterances_matter:
           pass
           # Optionally, import your LLM API here.
           # Then you can use it to help create utterances.

       self.who_i_play = what_side_to_play
       self.opponent_nickname = opponent_nickname
       self.time_limit = expected_time_per_move
       global GAME_TYPE
       GAME_TYPE = game_type
       print("I CAN WIN AT", game_type.long_name)
       self.my_past_utterances = []
       # self.opponent_past_utterances = []
       self.utt_count = 0
       if self.twin: self.utt_count = 5 # Offset the twin's utterances.
           
       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
       return "OK"
   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        myMove = self.chooseMove(current_state)
        minimax_value, newState, newMove = myMove

        myUtterance = self.nextUtterance(minimax_value)

        return [[newMove, newState], myUtterance]
    
    def nextUtterance(self, minimax_value):
        # if self.repeat_count > 1: return "I'M TESTING."
        utterances = UTTERANCE_BANK

        if minimax_value > WIN_THRESHOLD:
            return WIN_UTTERANCE
        elif minimax_value > NUETRAL_THRESHOLD:
            utterances = HAPPY_UTTERANCE
        elif minimax_value < - NUETRAL_THRESHOLD:
            utterances = SAD_UTTERANCE
        elif minimax_value < - LOSE_THRESHOLD:
            return LOSE_UTTERANCE

        n = len(utterances)
        #if self.utt_count == n:
            #self.utt_count = 0
        random_index = randint(0, n-1)

        this_utterance = utterances[random_index]
        #self.utt_count += 1
        return this_utterance
   

    # The main adversarial search function:
    def minimax(self,
            state,
            move,
            depth_remaining,
            pruning=False,
            alpha=None,
            beta=None):
        # print("Calling minimax with " + str(state.whose_move) + str(state) + str(move))

        # generate sucessors
        child_nodes, moves = successors_and_moves(state)
        
        if (depth_remaining == 0 or child_nodes==[]):
            node_value = self.static_eval(state)

            # return node's value and which move node it came from
            return [node_value, state, move]

        # If Maximizing Node
        if state.whose_move == 'X':
            max_value = BETA_DEFAULT

            # traverse all possible options
            for index in range(len(child_nodes)):
                node_value, node_state, node_move = self.minimax(child_nodes[index], moves[index], depth_remaining - 1, pruning, alpha, beta)

                max_value = max(node_value, max_value)
                alpha = max(alpha, max_value)

                # if pruning is true and beta pass alpha, prune node
                if pruning == True and beta <= alpha:
                    break
            return [max_value, node_state, node_move]
        
        # If Minimizing Node
        else:
            max_value = ALPHA_DEFAULT

            # traverse all possible options
            for index in range(len(child_nodes)):
                node_value, node_state, node_move = self.minimax(child_nodes[index], moves[index], depth_remaining - 1, pruning, alpha, beta)

                max_value = min(node_value, max_value)
                beta = min(beta, max_value)

                # if pruning is true and beta pass alpha, prune node
                if pruning == True and beta <= alpha:
                    break
            return [max_value, node_state, node_move]

        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 

    # Choose Move based on minimax
    def chooseMove(self, root_state):

        # run minimax
        minimax_value, state, move = self.minimax(root_state, (0,0), MINIMAX_DEPTH, True, ALPHA_DEFAULT, BETA_DEFAULT)

        my_choice = [minimax_value, state, move]
        return my_choice
    
    def static_eval(self, state, game_type=None):
        print('calling static_eval.')
        # Values should be higher when the states are better for X,
        # lower when better for O.

        # If initial state:
            # 1. Generate all possible k-in-a-rows as Objs/sets for m * n
            # 2. Map each coordinate to their possible k-in-a-rows, where coordinates are keys and k-in-a-rows are values
            # Run through state board, call userMakeNewMove() for each X and O encounter

        # If not initial run: helper function userMakeNewMove()
            # 3. User put X on coordinate, look up coordinate, numX+=1 for reach k-in-a-rows
            # 4. User put O on coordinate, look up coordinate, numO+=1 for each k-in-a-rows
            # 5. if look up coordinate numX > 0 and == numO, delete possibility
            # 6. Calculate score, 10^numX * numk-in-a-rows - 10^numO * numk-in-a-rows
            # 8. If numX = k Win
            # Win check
            #   Filter k-2 in a rows
            #     If intersection >=4, guarenteed win
            #   Filter k-1 in a rows
            #     If intersection >=2, guarenteed win
        
        total_score = 0
        m = 0
        n = 0
        
        if game_type != None:
            m = game_type.m
            n = game_type.n
        # else:
        #     m = state.m
        #     n = state.n

        # simple static eval for now...
        for i in range(m):
            count = 0
            for j in range(n):
                if state[i][j] == 'X':
                    count += 1
                if state[i][j] == 'O':
                    count -= 1
            total_score += 10 ** count

        return total_score
    
# Figure out who the other player is.
# For example, other("X") = "O".
def other(p):
    if p=='X': return 'O'
    return 'X'

# The following is a Python "generator" function that creates an
# iterator to provide one move and new state at a time.
# It could be used in a smarter agent to only generate SOME of
# of the possible moves, especially if an alpha cutoff or beta
# cutoff determines that no more moves from this state are needed.
def move_gen(state):
    b = state.board
    p = state.whose_move
    o = other(p)
    mCols = len(b[0])
    nRows = len(b)

    for i in range(nRows):
        for j in range(mCols):
            if b[i][j] != ' ': continue
            news = do_move(state, i, j, o)
            yield [(i, j), news]

# This uses the generator to get all the successors.
def successors_and_moves(state):
    moves = []
    new_states = []
    for item in move_gen(state):
        moves.append(item[0])
        new_states.append(item[1])

    return [new_states, moves]

# Performa a move to get a new state.
def do_move(state, i, j, o):
            news = game_types.State(old=state)
            news.board[i][j] = state.whose_move
            news.whose_move = o
            return news

UTTERANCE_BANK = ["TESTING PHRASE 1",
                  "TESTING PHRASE 2",
                  "TESTING PHRASE 3"]

WIN_UTTERANCE = ["BOT WIN"]

LOSE_UTTERANCE = ["BOT LOSE"]

SAD_UTTERANCE = ["BOT SAD", "BOT SADDER"]

HAPPY_UTTERANCE = ["BOT HAPPY", "BOT HAPPIER"]

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

 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

