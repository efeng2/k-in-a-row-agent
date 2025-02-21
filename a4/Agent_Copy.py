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
ALPHA_DEFAULT = -10000000
BETA_DEFAULT = 10000000
# MINIMAX_DEPTH = 2

# For utterances to change according to game state
# WIN_THRESHOLD = 100000
# LOSE_THRESHOLD = 10000
NUETRAL_THRESHOLD = 5




class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Times'
        if twin: self.nickname += ' II'
        self.long_name = 'TicTacTimes'
        if twin: self.long_name += ' the II'
        self.persona = 'snarky'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        # self.alpha_beta_cutoffs_this_turn = -1
        # self.num_static_evals_this_turn = -1
        # self.zobrist_table_num_entries_this_turn = -1
        # self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None
        self.my_past_utterances = []
        self.utt_count = 0

        # Quick Booleans for utterance control
        self.win = False
        self.lose = False
        self.tie = False
        
        self.XKInARows = []
        self.OKInARows = []

    def introduce(self):
        intro = '"Good evening, dear reader! I\'m TicTacTimes, the world\'s first AI journalist dedicated to hard-hitting Tic-Tac-Toe coverage. Reporting live from The Daily Grid!'
        if self.twin:
            intro = '"And I\'m TicTacTimes the II, I don\'t sugarcoat the truth. Together, we\'re the most unstoppable duo in Tic-Tac-Toe reporting history.'
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

        utterances_matter=False):      # If False, just return 'OK' for each utterance,
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
       print("Breaking news: A thrilling game of Tic-Tac-Toe is about to begin! You vs. me. Let's see who makes headlines.", game_type.long_name)
       self.my_past_utterances = []

       self.win = False
       self.lose = False
       self.tie = False

       self.utt_count = 0
       if self.twin: self.utt_count = 5
           
       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
       return "OK"
   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        #print("make_move has been called")

        myMove = self.chooseMove(current_state, use_alpha_beta, special_static_eval_fn, max_ply)
        minimax_value, newState, newMove = myMove

        myUtterance = self.nextUtterance(minimax_value)

        return [[newMove, newState], myUtterance]
    
    def nextUtterance(self, minimax_value):
        utterances = UTTERANCE_BANK

        if self.who_i_play == "O":
            minimax_value = - minimax_value

        if self.win:
            utterances = WIN_UTTERANCE
        elif self.lose:
            utterances = LOSE_UTTERANCE
        elif self.tie:
            utterances = TIE_UTTERANCE
        elif minimax_value > NUETRAL_THRESHOLD:
            utterances = HAPPY_UTTERANCE
        elif minimax_value < (- NUETRAL_THRESHOLD):
            utterances = SAD_UTTERANCE

        n = len(utterances)
        
        random_index = randint(0, n-1)
        this_utterance = utterances[random_index]

        # just in case for less repetition...
        while this_utterance in self.my_past_utterances:
            random_index = randint(0, n-1)
            this_utterance = utterances[random_index]

        self.my_past_utterances.append(this_utterance)
        self.utt_count += 1

        if self.utt_count > len(UTTERANCE_BANK):
            self.my_past_utterances = []

        return this_utterance
   

    # The main adversarial search function:
    def minimax(self,
            state,
            move,
            depth_remaining,
            static_eval_fn,
            isRoot,
            isMaxNode,
            pruning=False,
            alpha=None,
            beta=None):

        # generate sucessors
        child_nodes, moves = successors_and_moves(state)
        
        if (depth_remaining == 0 or child_nodes==[]):
            #print([alpha, beta])
            node_value = static_eval_fn(state)

            return [node_value, state, move]

        # If Maximizing Node
        if isMaxNode:
            max_value = ALPHA_DEFAULT
            bestNodeState = None
            bestNodeMove = None

            # traverse all possible options
            for index in range(len(child_nodes)):
                node_value, node_state, node_move = self.minimax(child_nodes[index], moves[index], depth_remaining - 1, static_eval_fn, False, False, pruning, alpha, beta)

                if node_value > max_value:
                    bestNodeState = node_state
                    bestNodeMove = node_move
                    max_value = node_value

                # max_value = max(node_value, max_value)
                alpha = max(alpha, max_value)

                # if pruning is true and beta pass alpha, prune node     
                if pruning == True and beta <= alpha:
                    break
            if isRoot:
                return [max_value, bestNodeState, bestNodeMove]
            else:
                return [max_value, state, move]
        
        # If Minimizing Node
        else:
            min_value = BETA_DEFAULT
            bestNodeState = None
            bestNodeMove = None

            # traverse all possible options
            for index in range(len(child_nodes)):
                node_value, node_state, node_move = self.minimax(child_nodes[index], moves[index], depth_remaining - 1, static_eval_fn, False, True, pruning, alpha, beta)

                if node_value < min_value:
                    bestNodeState = node_state
                    bestNodeMove = node_move
                    min_value = node_value

                # max_value = min(node_value, max_value)
                beta = min(beta, min_value)

                # if pruning is true and beta pass alpha, prune node
                if pruning == True and beta <= alpha:
                    break
            if isRoot:
                return [min_value, bestNodeState, bestNodeMove]
            else:
                return [min_value, state, move]

    # Choose Move based on minimax
    def chooseMove(self, root_state, use_alpha_beta, special_static_eval_fn, max_ply):
        static_eval_fn = self.static_eval
        isMaxNode = True

        if special_static_eval_fn != None:
            static_eval_fn = special_static_eval_fn
        if self.who_i_play == 'O':
            isMaxNode = False

        # run minimax
        minimax_value, state, move = self.minimax(root_state, (0,0), max_ply, static_eval_fn, True, isMaxNode, use_alpha_beta, ALPHA_DEFAULT, BETA_DEFAULT)
        print(minimax_value)
        my_choice = [minimax_value, state, move]
        return my_choice

    def static_eval(self, state, game_type=None, use_existing_KInARows=False, move=None):
        # print('calling static_eval.')
        # Values should be higher when the states are better for X,
        # lower when better for O.

        # Assumes K value of 3 if no game type specified
        total_score = 0
        k = 3
        

        if game_type != None:
            k = game_type.k

        if not use_existing_KInARows:
            self.XKInARows = [] # horizontal, vertical, diagonalLeft, diagonalRight
            self.OKInARows = [] # horizontal, vertical, diagonalLeft, diagonalRight

        if not self.XKInARows and not self.OKInARows:
            self.find_possible_KInARows(state, k)

        for i in range(len(self.XKInARows)):
            total_score += self.XKInARows[i]
            total_score += (-1) * self.OKInARows[i]

        #print(total_score)
        return total_score

    def find_possible_KInARows(self, state, k):
        board = state.board

        # Transposed board
        board_t = [list(row) for row in zip(*board)]
        # print(board_t)

        # Diagonals 1
        board_d = get_diagonals(board)

        # Diagonals 2
        board_r = list(zip(*board[::-1]))
        board_td = get_diagonals(board_r)

        board_configs = [board, board_t, board_d, board_td]

        for board_config in board_configs:
            numXKInARows, numOKInARows = search_rows(board_config, k)

            self.XKInARows.append(numXKInARows)
            self.OKInARows.append(numOKInARows)
    
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

# For Good Game and Bad Game
UTTERANCE_BANK = ["Statistically speaking, we're evenly matched… for now.",
                  "Hmm… I'll need a moment to craft a witty response to that move...",
                  "And we're neck and neck, folks! Stay tuned for the next thrilling move!",
                  "A classic Tic-Tac-Toe standoff. The tension is unbearable!",
                  "No clear winner yet. But if I were you, I'd start panicking.",
                  " This game could go either way. Experts are on the edge of their seats!"
                  ]

SAD_UTTERANCE = ["You're in the lead, but I'm digging for a counter-strategy.",
                 "Hold the presses! I might actually lose? This is a scandal!",
                 "A rare setback, but history shows I always bounce back.",
                 "I see what you did there. But don't think for a second that I'm impressed.",
                 "My dignity is under attack. Developing story—please send help!",
                 "This is just a strategic loss to keep things interesting. Stay tuned."]

HAPPY_UTTERANCE = ["Breaking: My strategy is paying off. You're on the ropes!",
                   "Looks like I'm three steps ahead. You sure you're not playing checkers?",
                   "This just in: Your defeat is imminent. How does that make you feel?",
                   "Analysts predict a 99% \chance of me winning. The other 1% \is just me being generous.",
                   "Interesting choice. Was that skill or a lucky guess?",
                   "Ah, a predictable move. I wrote an article about this exact strategy last week.",
                   "Oh, bold move! A risky one, or are you just pretending to have a plan?",
                   "Breaking news: I'm on fire! Another genius move from yours truly!"
                   ]

# For end game
TIE_UTTERANCE = ["This just in: A tie! The crowd goes wild... or maybe just yawns."]

WIN_UTTERANCE = ["Breaking news: I win! Another victory for the history books! I'll be looking forward to tomorrow's headline!"]

LOSE_UTTERANCE = ["You've emerged victorious. I'll be needing to analyze this loss in tomorrow's edition...",
                  "Dear readers, today I learned humility… and I hate it."]

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

def search_rows(board, k):
    numXKInARows = 0
    numOKInARows = 0

    for i, row in enumerate(board):

        blank_count_x = 0
        blank_count_o = 0

        x_count = 0
        o_count = 0

        for j, space in enumerate(row):

            if space == ' ':
                blank_count_x += 1
                blank_count_o += 1

            elif space == 'X':

                # end o counter
                if blank_count_o >= k:
                    numOKInARows += blank_count_o - k + 1 * (10 ** o_count)
                blank_count_o = 0
                o_count = 0

                # start x counter
                blank_count_x += 1
                x_count += 1

            elif space == 'O':

                # end x counter
                if blank_count_x >= k:
                    numXKInARows += (blank_count_x - k + 1) * (10 ** x_count)
                blank_count_x = 0
                x_count = 0
                
                # start o counter
                blank_count_o += 1
                o_count += 1

            elif space == '-':
                
                # end both counters
                if blank_count_x >= k:
                    numXKInARows += (blank_count_x - k + 1) * (10 ** x_count)
                if blank_count_o >= k:
                    numOKInARows += blank_count_o - k + 1 * (10 ** o_count)
                
                # reset
                blank_count_o = 0
                blank_count_x = 0
                x_count = 0
                o_count = 0

        if blank_count_x >= k:
            numXKInARows += (blank_count_x - k + 1) * (10 ** x_count)
        if blank_count_o >= k:
            numOKInARows += blank_count_o - k + 1 * (10 ** o_count)
        blank_count_o = 0
        blank_count_x = 0
        x_count = 0
        o_count = 0

    return [numXKInARows, numOKInARows]

def get_diagonals(board):
    diags = []
    h = len(board)
    l = len(board[0])

    for i in range(-l, h):
        diag = []

        for j in range(l):

            if h > i + j >= 0:
                index = (i + j, j)
            else:
                continue
            diag.append(board[index[0]][index[1]])
        if diag:
            diags.append(diag)
    return diags