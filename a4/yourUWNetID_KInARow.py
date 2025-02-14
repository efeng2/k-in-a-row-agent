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

        self.initial_turn = True
        self.kInARowSet = {}
        self.coodinateDict = {}

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

    def straightLoop(self, sideA, sideB, game_type, state):
        k = game_type.k

        total_score = 0
        blank_count = 0

        for m in range(sideA):
            for n in range(sideB):
                
                # coordinate (m, n), increase blank count
                blank_count += 1

                # if run into "-"
                if state.board[m][n] == "-":
                    blank_count = 0

                self.coodinateDict[(m, n)] = [] 

                # if possible k in a row, create new kInARow and add all previous coordinates to set
                if blank_count == k:
                    newKInARow = []
                    coordSet = set()
                    newKInARow.append(coordSet)

                    # append num X/O
                    newKInARow.append(0)

                    for blank in range(blank_count):
                        newKInARow[0].add((m, n - blank))

                        self.coodinateDict[(m, n - blank)].append(newKInARow)
                        
                        # add set as value to every coordinate in coodinateDict
                    blank_count += -1

                # # If X
                # if state.board[m][n] == 'X':
                #     # Every kInARow with this coordinate, increase numX count
                #     for kInaRow in self.coodinateDict[(m, n)]:
                #         # delete if kInaRow contains numO
                #         if kInaRow['numO'] > 0:
                #             del kInaRow
                #         else:
                #             kInaRow['numX'] += 1
                #             total_score += 10 ** kInaRow['numX']
                    
                # # If O
                # if state.board[m][n] == 'O':
                #     # Every kInARow with this coordinate, increase numO count
                #     for kInaRow in self.coodinateDict[(m, n)]:
                #         # delete if kInaRow contains numO
                #         if kInaRow['numX'] > 0:
                #             del kInaRow
                #         else:
                #             kInaRow['numO'] += 1
                #             total_score += -10 ** kInaRow['numO']

                # # reset blank count when moving to the next row
            blank_count = 0
        print(self.coodinateDict)
        return total_score
    
    def makeUserMove(self, state):
        return 0
    
    def static_eval(self, state, game_type=None):
        print('calling static_eval. Its value needs to be computed!')
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

        if (self.initial_turn == True):

            # loop through horizontal
            total_score += self.straightLoop(game_type.m, game_type.n, game_type, state)
            # loop through vertical
            total_score += self.straightLoop(game_type.n, game_type.m, game_type, state)

            # loop through diag left

            # loop through diag right

            self.initial_turn = False

        else:
            self.makeUserMove(state)

        return total_score

    
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

