from XAEA_Xii.eval import beat_possible
from XAEA_Xii.util import throw, slide, swing
from XAEA_Xii.functions import out_of_board
from XAEA_Xii.minimax import minimax
from XAEA_Xii.board import update_state
import numpy as np

def throw_action(throw_token, opponent, opponent_throws, colour, state):
    """
    Use multi-minimax to choose the best throw location
    return: loc (r, q)
    """
    
    

def swing_slide_action(player, opponent, state):
    """
    Use multi-minimax to choose best slide / swing
    return: atype (slide/swing), old_loc: (r0, q0), new_loc (r_1, q_1)
    """
    # Only implemented slides so far
    player_queue = generate_children(player)
    opponent_queue = generate_children(opponent)
    
    # This is multiminimax
    move_to_make = 0
    max_move = -np.inf
    alpha = -np.inf
    depth = 3
    for child in player_queue:
        player_new_loc = child[0]
        player_old_loc = child[1]

        action = (child[3], player_old_loc, player_new_loc)
        state = update_state(state, action)
        min_move = np.inf
        beta = np.inf
        for opp in opponent_queue:
            opponent_loc = opp[0]
            min_move = min(min_move, minimax(player_new_loc, opponent_loc, depth-1, alpha, beta, False, state))
            beta = min_move
            if alpha >= beta:
                break
        if min_move >= max_move:
            move_to_make = child
            max_move = min_move
            alpha = max_move
    print(move_to_make)
    #move_to_make is of form (new location, old location, type of token, move type)
    #return (move_to_make[3], move_to_make[1], move_to_make[0])
    return ("SWING", (0,0), (0,0))
    



# |---------------------------------------------------------------------------|
"""
Strategy:
    - IF I can't win, then throw the right token
    - IF I can win, then move to a better state

Comments: 
    - These are two differents minimax algorithm implementations. 
    - This method is better than using one single minimax because we minimise the width of the tree, making it easier to go deeper. 
"""


def make_move(state, player_throws, opponent_throws, colour):
    """
    Check if player has the right tokens to -beat-> opponenet
        - no:
            THROW
        - yes:
            SLIDE/SWING
    """
    player = state["player"]
    opponent = state["opponent"]

    throw_token = beat_possible(player, opponent)
    if throw_token and player_throws:
        token, loc = throw_token, throw_action(throw_token, opponent, opponent_throws, colour, state) # multi-minimax: throw
        return throw(token, loc)        
    else:
        atype, old_loc, new_loc = swing_slide_action(player, opponent, state) # multi-minimax: slide / swing
        if atype == "SWING":
            swing(old_loc, new_loc)
        else:
            slide(old_loc, new_loc) 


# |---------------------------------------------------------------------------|

def generate_children(dictionary):
    adjacent_squares = {
    "UR":(1, 0), "UL":(+1, -1), "L":(0, -1), 
    "DL":(-1, 0), "DR":(-1, +1), "R":(0, +1)}
    
    # In the move_suggestions will be tuples of (new location, old location, type of token, move type)
    final_moves_suggestions = []

    # Find each adjacent hex to each hex in our dictionary and add the new hex to suggestions
    for loc in dictionary.keys():
        hex_suggestions = []

        for value in adjacent_squares.values():
            new_loc = (loc[0] + value[0], loc[1] + value[1])
            if not out_of_board(new_loc):
                final_moves_suggestions.append(new_loc, loc, dictionary[loc], "SLIDE")
                hex_suggestions.append(new_loc)
                
                # If a new hex is already in our keys, that means it is the location of one of our tokens and we can use it to swing
                if new_loc in dictionary.keys():
                    for values in adjacent_squares.values():
                        swing_loc = (new_loc[0] + values[0], new_loc[1] + values[1])
                        
                        # If swing_loc is in hex_suggestions that means that location is already slidable so doesnt need to be included
                        if not out_of_board(swing_loc) and swing_loc not in hex_suggestions:
                            final_moves_suggestions.append(swing_loc, loc, dictionary[loc], "SWING")

    return final_moves_suggestions