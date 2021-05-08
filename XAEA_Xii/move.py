from XAEA_Xii.util import throw, slide, swing, out_of_board
from XAEA_Xii.board import update_state
from XAEA_Xii.minimax import minimax
from random import randint
import numpy as np


def first_throw(colour):
    tok = ['r', 'p', 's'][randint(0,2)]
    if   colour == 'lower':
        loc =  (-4, randint(0, 4))
    elif colour == 'upper':
        loc = (4, -randint(0, 4))
    return throw(tok, loc)
        

def swing_slide_throw(player, opponent, state):

    # Only implemented slides so far
    player_queue = generate_children(player)
    opponent_queue = generate_children(opponent)
    
    # This is multiminimax
    move_to_make = 0
    max_move = -np.inf
    alpha = -np.inf
    depth = 3
    for child in player_queue:
        state = update_state(state, child)
        min_move = np.inf
        beta = np.inf
        for opp in opponent_queue:
            opponent_action = opp
            min_move = min(min_move, minimax((child), (opp), depth-1, alpha, beta, False, state))
            beta = min_move
            if alpha >= beta:
                break
        if min_move >= max_move:
            move_to_make = child
            max_move = min_move
            alpha = max_move

    return (move_to_make[3], move_to_make[1], move_to_make[0])


    

# |---------------------------------------------------------------------------|

def make_move(state, player_throws, opponent_throws, colour):
    """
    LOGIC:
        - first throw      => random token & random depth:1 hex location
        - post first-throw => multi-minimax 
    """
    
    
    player = state["player"]
    opponent = state["opponent"]
    
    # first throw => random token & random depth:1 hex location
    if player_throws == 9 and opponent_throws == 9:
        return first_throw(colour)      
    

    # post first-throw => multi-minimax 
    return swing_slide_throw(player, opponent, state) 
    


# |---------------------------------------------------------------------------|

def generate_children(dictionary):
    adjacent_squares = {
    "UR":(1, 0), "UL":(+1, -1), "L":(0, -1), 
    "DL":(-1, 0), "DR":(-1, +1), "R":(0, +1)}
        
    final_moves_suggestions = []

    for loc in dictionary.keys():
        hex_suggestions = []

        for value in adjacent_squares.values():
            new_loc = (loc[0] + value[0], loc[1] + value[1])
            if not out_of_board(new_loc):
                final_moves_suggestions.append(slide(loc, new_loc))
                hex_suggestions.append(new_loc)
                
                # If a new hex is already in our keys, that means it is the location of one of our tokens and we can use it to swing
                if new_loc in dictionary.keys():
                    for values in adjacent_squares.values():
                        swing_loc = (new_loc[0] + values[0], new_loc[1] + values[1])
                        
                        # If swing_loc is in hex_suggestions that means that location is already slidable so doesnt need to be included
                        if not out_of_board(swing_loc) and swing_loc not in hex_suggestions:
                            final_moves_suggestions.append((swing_loc, loc, dictionary[loc], "SWING"))

    return final_moves_suggestions
