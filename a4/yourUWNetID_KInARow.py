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
from game_types import State, Game_Type

AUTHORS = 'Jane Smith and Laura Lee'

import time  # You'll probably need this to avoid losing a


# game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin = twin
        self.nickname = 'Nic'
        if twin: self.nickname += '2'
        self.long_name = 'Templatus Skeletus'
        if twin: self.long_name += ' II'
        self.persona = 'bland'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet"  # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None
        self.KInARows = {}  #Stores [[list of k in a rows],[evaluations]]
        self.spaces = {}    #Stores {(i,j): [associated k in a rows]}

    def introduce(self):
        intro = '\nMy name is Templatus Skeletus.\n' + \
                '"An instructor" made me.\n' + \
                'Somebody please turn me into a real game-playing agent!\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
            self,
            game_type,
            what_side_to_play,
            opponent_nickname,
            expected_time_per_move=0.1,  # Time limits can be
            # changed mid-game by the game master.

            utterances_matter=True):  # If False, just return 'OK' for each utterance,
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
        self.who_i_play = what_side_to_play
        self.opponent_nickname = opponent_nickname
        self.time_limit = expected_time_per_move
        global GAME_TYPE
        GAME_TYPE = game_type
        print("Oh, I love playing randomly at ", game_type.long_name)
        self.my_past_utterances = []
        self.opponent_past_utterances = []
        self.repeat_count = 0
        self.utt_count = 0
        if self.twin: self.utt_count = 5  # Offset the twin's utterances.

        return "OK"

    # The core of your agent's ability should be implemented here:
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        possibleMoves = successors_and_moves(current_state)

        # Here's a placeholder:
        a_default_move = (0, 0)  # This might be legal ONCE in a game,
        # if the square is not forbidden or already occupied.

        new_state = current_state  # This is not allowed, and even if
        # it were allowed, the newState should be a deep COPY of the old.

        new_remark = "I need to think of something appropriate.\n" + \
                     "Well, I guess I can say that this move is probably illegal."

        print("Returning from make_move")
        return [[a_default_move, new_state], new_remark]

    # The main adversarial search function:
    def minimax(self,
                state,
                depth_remaining,
                pruning=False,
                alpha=None,
                beta=None):
        print("Calling minimax. We need to implement its body.")
        if not pruning:
            if depth_remaining == 0:
                return self.static_eval(state,GAME_TYPE)
            if state.whose_move == 'X':
                prov = -100000
            else:
                prov = 100000
           # for s in successors()

        default_score = 0  # Value of the passed-in state. Needs to be computed.

        return [default_score, "my own optional stuff", "more of my stuff"]
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc.

    def static_eval(self, state, game_type=None, use_existing_KInARows=False, move=None):
        print('calling static_eval. Its value needs to be computed!')
        # Values should be higher when the states are better for X,
        # lower when better for O.

        # Assumes K value of 3 if no game type specified
        if game_type is None:
            k = 3
        else:
            k = game_type.k

        if not use_existing_KInARows:
            self.KInARows = {}
            self.spaces = {}
        if not self.KInARows and not self.spaces:
            self.find_possible_KInARows(state, k)

        if move is not None:
            for i in self.spaces[move]:
                cscore = self.KInARows[i][1]
                if cscore == 0 and state.whose_move == "X":
                    self.KInARows[i][1] = 10
                elif cscore > 0 and state.whose_move == "X":
                    self.KInARows[i][1] = cscore*10
                elif cscore < 0 and state.whose_move == "X":
                    self.KInARows[i][1] = None
                elif cscore == 0 and state.whose_move == "O":
                    self.KInARows[i][1] = -10
                elif cscore > 0 and state.whose_move == "O":
                    self.KInARows[i][1] = None
                elif cscore < 0 and state.whose_move == "O":
                    self.KInARows[i][1] = cscore*10

        # Find the total score from KInARows
        score = 0
        for k_in_a_row in self.KInARows:
            score += k_in_a_row[1]

        return score

    def find_possible_KInARows(self, state, k):
        board = state.board

        # Transposed board
        board_t = [list(row) for row in zip(*board)]

        # Diagonals 1
        board_d = get_diagonals(board)

        # Diagonals 2
        board_td = get_diagonals(board_t)

        board_configs = [board, board_t, board_d, board_td]

        for board_config in board_configs:
            k_in_a_rows,spaces = search_rows(board_config,k)
            self.KInARows.update(k_in_a_rows)
            self.spaces.update(spaces)

        return

    # def associate_coordinates(self, state):
    #     board = state.board
    #     coordinates = {}
    #     for i,row in enumerate(board):
    #         for j,space in enumerate(row):
    #             for n,k_in_a_row in enumerate(self.KInARows):
    #                 if (i,j) in k_in_a_row[0]:
    #                     if coordinates[(i,j)]
    #                     coordinates[(i,j)] = []

class NextStateEval(State):
    def __init__(self, last_move, whose_turn, k_in_a_rows, spaces):
        super().__init__()
        self.move = last_move
        self.whose_turn = whose_turn
        self.k_in_a_rows = k_in_a_rows.copy()
        self.spaces = spaces

    def run_eval(self):
        for k_in_a_row in self.spaces[self.move]:
            val = self.k_in_a_rows.pop(k_in_a_row)


        pass




def search_rows(board,k):
    k_in_a_rows = {}
    spaces = {}
    for i, row in enumerate(board):
        count = 0
        x_count = 0
        o_count = 0
        for j, space in enumerate(row):
            if len(row) >= k:
                if space == ' ':
                    count += 1
                elif space == 'X':
                    if o_count:
                        count =  0
                        x_count = 0
                        o_count = 0
                    else:
                        count += 1
                        x_count += 1
                elif space == 'O':
                    if x_count:
                        count =  0
                        x_count = 0
                        o_count = 0
                    else:
                        count += 1
                        o_count += 1
                elif space == '-':
                    count = 0
                    x_count = 0
                    o_count = 0

            if count >= k:
                indices = {(i,x+1) for x in range(j-k,j)}
                if x_count and o_count:
                    raise Exception("x_count or o_count should be 0")
                score = x_count**10 - o_count**10
                new_k_in_a_row = [indices,score]
                k_in_a_rows.append(new_k_in_a_row)


                for index in indices:
                    if index in spaces:
                        spaces[index].append(new_k_in_a_row)
                    else:
                        spaces[index] = [new_k_in_a_row]
    return k_in_a_rows,spaces

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

# Figure out who the other player is.
# For example, other("X") = "O".
def other(p):
    if p=='X': return 'O'
    return 'X'

# Randomly choose a move.
def chooseMove(statesAndMoves):
    # states, moves = statesAndMoves
    # if states==[]: return None
    # random_index = randint(0, len(states)-1)
    # my_choice = [states[random_index], moves[random_index]]
    pass

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

list1 = [[0, 1], [2, 3]]

diag = get_diagonals(list1)

print(diag)
