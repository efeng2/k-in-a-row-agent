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
from game_types import State, Game_Type, FIAR, Cassini, TTT

AUTHORS = 'Jane Smith and Laura Lee'

import time  # You'll probably need this to avoid losing a


# game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:
GAME_TYPE = None

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
        self.current_state = None
        self.k_in_a_rows  = {}  #Stores all possible k in a rows and their current scores {{k_in_a_row},score}
        self.open_spaces  = []  #Stores all available open spaces
        self.future_kiars = []  #Stores possible k in a rows for future moves where move is ('X',(1,2)) [[move1, {k_in_a_rows}{open_spaces}],[move2, {k_in_a_rows},{open_spaces}, [move2.1, {k_in_a_rows}{open_spaces}]]]]
        self.space_assoc  = {}  #Stores {(i,j): [associated k in a rows]}
        self.t_start = None


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

        self.find_possible_k_in_a_rows(game_type.initial_state,game_type.k)

        return "OK"

    # The core of your agent's ability should be implemented here:
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        self.t_start = time.time()

        old_state = self.current_state
        self.current_state = current_state

        new_remark = "I need to think of something appropriate.\n" + \
                     "Well, I guess I can say that this move is probably illegal."

        print("Returning from make_move")
        return [[chosen_move, new_state], new_remark]

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
            for move in self.open_spaces:
                if state.whose_move == 'X':
                    eval_move(('X',move),self.k_in_a_rows,self.space_assoc,self.open_spaces)
                elif state.whose_move == 'O':
                    eval_move(('O',move),self.k_in_a_rows,self.space_assoc,self.open_spaces)
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
            self.current_state = state
        if not self.KInARows and not self.spaces:
            self.find_possible_k_in_a_rows(state, k)

        if move is not None:
            new_k_in_a_rows, new_space_assoc, new_open_spaces = eval_move(move, self.k_in_a_rows, self.space_assoc, self.open_spaces)

        # Find the total score from KInARows
        score = 0
        for k_in_a_row in self.KInARows:
            score += k_in_a_row[1]

        return score

    def find_possible_k_in_a_rows(self, state, k):
        board = []
        for i, row in enumerate(state.board):
            new_row = []
            for j, space in enumerate(row):
                new_row.append((space,(i,j)))
            board.append(new_row)

        board_t = [list(row) for row in zip(*board)]    # Transposed board
        board_d = get_diagonals(state.board)  # Diagonals
        board_configs = [board, board_t, board_d]

        for board_config in board_configs:
            search_rows(board,board_config,k,self.k_in_a_rows,self.space_assoc,self.open_spaces)
        return

def eval_move(move, k_in_a_rows, space_assoc, open_spaces):
    new_k_in_a_rows = k_in_a_rows.copy()
    new_space_assoc = space_assoc.copy()
    new_open_spaces = open_spaces.copy()
    new_open_spaces.remove(move[1])

    # Updates the new k_in_a_row values
    for k_in_a_row in space_assoc[move[1]]:
        if move[0] == 'X':
            if k_in_a_rows[k_in_a_row] >= 0:
                new_k_in_a_rows[k_in_a_row] += 1
            else:
                del new_k_in_a_rows[k_in_a_row]
                new_space_assoc[move[1]].remove(k_in_a_row)
        elif move[0] == 'O':
            if k_in_a_rows[k_in_a_row] <= 0:
                new_k_in_a_rows[k_in_a_row] -= 1
            else:
                del new_k_in_a_rows[k_in_a_row]
                new_space_assoc[move[1]].remove(k_in_a_row)
    eval_k_in_a_rows(new_k_in_a_rows)
    return new_k_in_a_rows, new_space_assoc, new_open_spaces

def eval_k_in_a_rows(k_in_a_rows):
    cur_score = 0
    max_count = 0
    if 'score' in k_in_a_rows:
        del k_in_a_rows['score']
    for kiar in k_in_a_rows:
        if max_count < abs(k_in_a_rows[kiar]):
            max_count = abs(k_in_a_rows[kiar])
            cur_score = k_in_a_rows[kiar]
        elif max_count == abs(k_in_a_rows[kiar]):
            cur_score += k_in_a_rows[kiar]
    score = 10**max_count*cur_score
    k_in_a_rows.update({'score':score})
    return

def search_rows(board,board_config,k,k_in_a_rows,space_assoc,open_spaces):
    for row in board_config:
        x_count = 0
        o_count = 0
        indices = []
        for col in row:
            space = col[0]
            i = col[1][0]
            j = col[1][1]
            index = (i,j)
            if space == ' ':
                indices.append(index)
                if index not in open_spaces:
                    open_spaces.append(index)
            elif space == 'X':
                if o_count:
                    x_count = 0
                    o_count = 0
                    indices = []
                else:
                    x_count += 1
                    indices.append(index)
            elif space == 'O':
                if x_count:
                    x_count = 0
                    o_count = 0
                    indices = []
                else:
                    o_count += 1
                    indices.append(index)
            elif space == '-':
                x_count = 0
                o_count = 0
                indices = []

            if len(indices) == k:
                kiar_indices = frozenset(indices)
                if x_count and o_count:
                    raise Exception("x_count or o_count should be 0")
                score = x_count - o_count
                new_k_in_a_row = {kiar_indices:score}
                k_in_a_rows.update(new_k_in_a_row)

                for kiar_index in kiar_indices:
                    if kiar_index in space_assoc:
                        space_assoc[kiar_index].append(kiar_indices)
                    else:
                        space_assoc[kiar_index] = [kiar_indices]

                if board[indices[0][0]][indices[0][1]][0] == 'X':
                    x_count -= 1
                elif board[indices[0][0]][indices[0][1]][0] == 'O':
                    o_count -= 1

                indices = indices[1:]
    eval_k_in_a_rows(k_in_a_rows)
    return

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
            diag.append((board[index[0]][index[1]],index))
        if diag:
            diags.append(diag)

    for i in range(l + h - 1, -1, -1):
        diag = []

        for j in range(l):

            if i - j < h and i - j >= 0:
                index = (i - j, j)
            else:
                continue
            diag.append((board[index[0]][index[1]],index))
        if diag:
            diags.append(diag)

    return diags



def other(p):
    # Figure out who the other player is.
    # For example, other("X") = "O".
    if p=='X': return 'O'
    return 'X'

def chooseMove(statesAndMoves):
    # states, moves = statesAndMoves
    # if states==[]: return None
    # random_index = randint(0, len(states)-1)
    # my_choice = [states[random_index], moves[random_index]]
    pass

# The following is a Python "generator" function that creates an
# iterator to provide one move and new state at a time.
# It could be used in a smarter agent to only generate SOME
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

# Perform a move to get a new state.
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
if __name__ == '__main__':

    mocha = OurAgent()
    mocha.prepare(FIAR,'X','fig')
    # fig = search_rows(Cassini.initial_state.board,5)[0]
    fig = mocha.k_in_a_rows


    count = 0
    for entry in fig:
        print(str(entry)+"  ---  "+str(fig[entry]))
        count +=1

    print(count)
    count = 0

    sam = mocha.open_spaces
    for entry in sam:
        print(str(entry))
        count+=1

    print(count)

    start = time.time()
    puggle = eval_move(('X',(0,1)),fig,mocha.space_assoc,sam)
    # x = eval_k_in_a_rows((puggle[0]))
    end = time.time()


    print('new')

    puggle0 = puggle[0]
    puggle1 = puggle[1]
    puggle2 = puggle[2]

    for entry in puggle0:
        print(str(entry) +"  ---  "+str(puggle0[entry]))

    for entry in puggle1:
        print(str(entry)+"  ---  "+str(puggle1[entry]))

    for entry in puggle2:
        print(str(entry))




    print(TTT.initial_state)
    print((end - start) * 100000)




