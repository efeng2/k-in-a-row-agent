'''
nshukla_KInARow.py
Authors: Shukla, Nishchal

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
from game_types import State, Game_Type

AUTHORS = 'Nishchal Shukla' 

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Ed'
        if twin: self.nickname += '2'
        self.long_name = 'Edward Dorian'
        if twin: self.long_name += ' II'
        self.persona = 'bland'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None
        self.opponent = "don't know yet" # Opponent's nickname
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        self.autograding = False
        self.special_static_eval_fn = None

    def introduce(self):
        intro = '\nMy name is Edward Dorian.\n'+\
            'Fear not the darkness, but welcome its embrace.\n'+\
            'Insiemme per la vittoria!\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
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
           
       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
       self.playing = what_side_to_play
       self.opponent = opponent_nickname
       self.current_game_type = game_type

       #print("Change this to return 'OK' when ready to test the method.")
       return "OK"
   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        #print("make_move has been called")

        #print("code to compute a good move should go here.")

        if(autograding):
            self.autograding = True
            self.special_static_eval_fn = special_static_eval_fn

        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0

        resulting_array = self.minimax(state=current_state, depth_remaining=max_ply, pruning=use_alpha_beta)
        # Here's a placeholder:
        a_default_move = (resulting_array[1], resulting_array[2])
    
        new_state = do_move(current_state, a_default_move[0], a_default_move[1], other(current_state.whose_move)) # This is not allowed, and even if
        # it were allowed, the newState should be a deep COPY of the old.
    
        new_remark = "I need to think of something appropriate.\n" +\
        "Well, I guess I can say that this move is probably illegal."

        if(autograding):
            stats = [self.alpha_beta_cutoffs_this_turn,
                    self.num_static_evals_this_turn,
                    -1,
                    -1]
            return [[a_default_move, new_state] + stats, new_remark]

        #print("Returning from make_move")
        return [[a_default_move, new_state], new_remark]

    # The main adversarial search function:
    def minimax(self,
            state,
            depth_remaining,
            pruning=True,
            alpha=-2147483648,
            beta=2147483647):
        #print("Calling minimax. We need to implement its body.")
        if depth_remaining == 0:
            if(self.autograding):
                return [self.special_static_eval_fn(state), None, None]
            return [self.static_eval(state, game_type = self.current_game_type), None, None]

        default_score = 0 # Value of the passed-in state. Needs to be computed.
        move = (0, 0) # Overriden below with other moves
        new_states, moves = successors_and_moves(state)

        if(len(new_states) == 0):
            return [self.static_eval(state, game_type = self.current_game_type), (None, None)]

        if state.whose_move == "X": # Maximizing player
            #print("X is Moving")
            default_score = -2147483648
            for i in range(0, len(new_states)):
                #print("Judging state: " + str(new_states[i]))
                #print("Move for this state: " + str(moves[i]))
                res_array = self.minimax(new_states[i], depth_remaining - 1, pruning=pruning, alpha=alpha, beta=beta)
                if(res_array[0] > default_score):
                    default_score = res_array[0]
                    move = moves[i]
                    #print("New move: " + str(move))
                if(pruning):
                    alpha = max(alpha, default_score)
                    if(beta <= alpha):
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
            
        else: # Minimizing player
            #print("O is Moving")
            default_score = 2147483647
            for i in range(0, len(new_states)):
                #print("Judging state: " + str(new_states[i]))
                #print("Move for this state: " + str(moves[i]))
                res_array = self.minimax(new_states[i], depth_remaining - 1, pruning=pruning, alpha=alpha, beta=beta)
                if(res_array[0] < default_score):
                    default_score = res_array[0]
                    move = moves[i]
                    #print("New move: " + str(move))
                if(pruning):
                    beta = min(beta, default_score)
                    if(beta <= alpha):
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
        #print("Result: " + str([default_score, move[0], move[1]]))
        return [default_score, move[0], move[1]]
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def static_eval(self, state, game_type=None):
        #print('calling static_eval. Its value needs to be computed!')
        # Values should be higher when the states are better for X,
        # lower when better for O.
        self.num_static_evals_this_turn += 1
        k = game_type.k
        b = state.board
        #print("Board: " + str(b))
        max_col = len(b[0])
        max_row = len(b)
        cols = [[] for _ in range(max_col)]
        rows = [[] for _ in range(max_row)]
        fdiag = [[] for _ in range(max_row + max_col - 1)]
        bdiag = [[] for _ in range(len(fdiag))]
        min_bdiag = -max_row + 1

        for x in range(max_col):
            for y in range(max_row):
                cols[x].append(b[y][x])
                rows[y].append(b[y][x])
                fdiag[x+y].append(b[y][x])
                bdiag[x-y-min_bdiag].append(b[y][x])
        
        diag_condition = lambda x: len(x) < k
        fdiag = [x for x in fdiag if not diag_condition(x)]
        bdiag = [x for x in bdiag if not diag_condition(x)]
        
        '''
        print("Rows: " + str(rows))
        print("Cols: " + str(cols))
        print("Fdiag: " + str(fdiag))
        print("Bdiag: " + str(bdiag))
        '''
        xs_in_seq = [0] * k
        os_in_seq = [0] * k
        for i in range(0, max(len(rows), len(cols), len(fdiag), len(bdiag))):
            row_str = ''.join(rows[i]) if i < len(rows) else ''
            #print("Row str: " + str(row_str))
            col_str = ''.join(cols[i]) if i < len(cols) else ''
            #print("Col str: " + str(col_str))
            fdiag_str = ''.join(fdiag[i]) if i < len(fdiag) else ''
            #print("Fdiag str: " + str(fdiag_str))
            bdiag_str = ''.join(bdiag[i]) if i < len(bdiag) else ''
            #print("Bdiag str: " + str(bdiag_str))
            for j in range(k - 1, -1, -1):
                x_str = "X" * (j + 1)
                x_str_gaps = "X " * (j + 1)
                x_str_gaps = x_str_gaps[:len(x_str_gaps) - 1]
                #print("X Checking for: " + x_str)
                o_str = "O" * (j + 1)
                o_str_gaps = "O " * (j + 1)
                o_str_gaps = x_str_gaps[:len(o_str_gaps) - 1]
                #print("O Checking for: " + o_str)
                x_num_instances = row_str.count(x_str) + col_str.count(x_str) + fdiag_str.count(x_str) + bdiag_str.count(x_str) + row_str.count(x_str_gaps) + col_str.count(x_str_gaps) + fdiag_str.count(x_str_gaps) + bdiag_str.count(x_str_gaps)
                #print("x_num_instances for " + str(j + 1) + " in a row: " + str(x_num_instances))
                xs_in_seq[j] += x_num_instances
                row_str = row_str.replace(x_str, "")
                col_str = col_str.replace(x_str, "")
                fdiag_str = fdiag_str.replace(x_str, "")
                bdiag_str = bdiag_str.replace(x_str, "")
                row_str = row_str.replace(x_str_gaps, "")
                col_str = col_str.replace(x_str_gaps, "")
                fdiag_str = fdiag_str.replace(x_str_gaps, "")
                bdiag_str = bdiag_str.replace(x_str_gaps, "")
                o_num_instances = row_str.count(o_str) + col_str.count(o_str) + fdiag_str.count(o_str) + bdiag_str.count(o_str) + row_str.count(o_str_gaps) + col_str.count(o_str_gaps) + fdiag_str.count(o_str_gaps) + bdiag_str.count(o_str_gaps)
                #print("o_num_instances for " + str(j + 1) + " in a row: " + str(o_num_instances))
                os_in_seq[j] += o_num_instances
                row_str = row_str.replace(o_str, "")
                col_str = col_str.replace(o_str, "")
                fdiag_str = fdiag_str.replace(o_str, "")
                bdiag_str = bdiag_str.replace(o_str, "")
                row_str = row_str.replace(o_str_gaps, "")
                col_str = col_str.replace(o_str_gaps, "")
                fdiag_str = fdiag_str.replace(o_str_gaps, "")
                bdiag_str = bdiag_str.replace(o_str_gaps, "")
                '''
                print("New row_str: " + row_str)
                print("New col_str: " + col_str)
                print("New fdiag_str: " + fdiag_str)
                print("New bdiag_str: " + bdiag_str)
                '''

        total = 0
        #print("Xs in seq: " + str(xs_in_seq))
        #print("Os in seq: " + str(os_in_seq))
        for i in range(0, len(xs_in_seq)):
            power = xs_in_seq[i] - os_in_seq[i]
            total += (10 ** i) * power
        #print("Total from static evaluation: " + str(total))
        return total
 
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
    #print("New states: " + str(new_states))
    #print("Moves: " + str(moves))
    return [new_states, moves]

# Performa a move to get a new state.
def do_move(state, i, j, o):
            news = State(old=state)
            news.board[i][j] = state.whose_move
            news.whose_move = o
            return news

# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

