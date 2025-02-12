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

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Nic'
        if twin: self.nickname += '2'
        self.long_name = 'Templatus Skeletus'
        if twin: self.long_name += ' II'
        self.persona = 'bland'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

    def introduce(self):
        intro = '\nMy name is Templatus Skeletus.\n'+\
            '"An instructor" made me.\n'+\
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
           
       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
       print("Change this to return 'OK' when ready to test the method.")
       return "Not-OK"
   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        print("code to compute a good move should go here.")
        # Here's a placeholder:
        a_default_move = (0, 0) # This might be legal ONCE in a game,
        # if the square is not forbidden or already occupied.
    
        new_state = current_state # This is not allowed, and even if
        # it were allowed, the newState should be a deep COPY of the old.
    
        new_remark = "I need to think of something appropriate.\n" +\
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

        default_score = 0 # Value of the passed-in state. Needs to be computed.
    
        return [default_score, "my own optional stuff", "more of my stuff"]

        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def static_eval(self, state, game_type=None):
        print('calling static_eval. Its value needs to be computed!')
        # Values should be higher when the states are better for X,
        # lower when better for O.

        # for 4 directions, start left, top, diag, diag:
        #     if find x, note num previous k-1 or end blanks and future k-1 or end blanks + 10n;
        #     if run into - or o before can have k, *0;
        #     if have another x, + 10^(k-d), add k - 1 blanks from other side;

        # if have k x win, + 10k^k

        # # left
        # total_score = 0
        # # each row
        # for m in range(state.m):
        #     count = 0
        #     numX = 1
        #     blanks_before = 0
        #     blanks_after = 0
        #     blanks_middle = 0
        #     row_score = 0
        #     k = state.k
        #     # each square
        #     for n in range(state.n):
        #         mark = state[m][n]

        #         # if run into X
        #         if (mark == 'X'):
        #             numX += 1

        #             # if first X, record blanks before
        #             if (numX == 1):
        #                 if (count >= k):
        #                     blanks_before += k - 1
        #                 else:
        #                     blanks_before += count
        #             # if have X already, record middle blanks
        #             else:
        #                 if (count >= k):
        #                     blanks_middle += count
        #                 else:
        #                     blanks_middle += count
        #             count = 0

        #         # if run into O
        #         elif (mark == 'O'):
        #             # if has X and blanks before X + blanks after X + blanks between X's is not greater than k, can't win so reset
        #             if (numX > 0 & count + blanks_before + blanks_middle < k - numX):
        #                 blanks_before = 0
        #                 numX = 0
                    
        #         # if forbidden
        #         elif (mark == '-'):
        #             # if has X and blanks before X + blanks after X + blanks between X's is not greater than k, can't win so reset
        #             if (numX > 0 & count + blanks_before + blanks_middle < k - numX):
        #                 blanks_before = 0
        #                 numX = 0

        #         # blank, increase blank count
        #         else:
        #             count += 1

        #         # if counted k-1 blanks after current X, give score and reset
        #         if (numX > 0 & count > k - 1):
        #             blanks_after = count
        #             numX = 0
        #             count = 0
        #             row_score += blanks_before + blanks_after * 10 * numX
        #             blanks_before = 0
        #             blanks_after = 0

        # return total_score

        # ROUND 2
        # 1. Generate all possible k-in-a-rows as Objs/sets
        # 2. Map each coordinate to their possible k-in-a-rows, where coordinates are keys and k-in-a-rows are values
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

 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

