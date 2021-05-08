from XAEA_Xii.util import throw, slide, swing, out_of_board, win
from XAEA_Xii.board import update_state, play_rps
from XAEA_Xii.minimax import minimax
from random import randint
import copy
import numpy as np
import itertools


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
    return swing_slide_throw(state, player_throws, opponent_throws, colour) 
    
# |---------------------------------------------------------------------------|

def swing_slide_throw(state, player_throws, opponent_throws, colour):

    player = state["player"]
    opponent = state["opponent"]
    
    player_need_throw, opponent_need_throw, player_throw_symbol, opponent_throw_symbol  = need_throw(state)
    player_colour, opponent_colour = set_colours(colour)

    player_queue = generate_children(player, player_need_throw, player_throws, player_colour, player_throw_symbol)
    opponent_queue = generate_children(opponent, opponent_need_throw, opponent_throws, opponent_colour, opponent_throw_symbol)
    
    info = {'player_throws': player_throws, 'opponent_throws': opponent_throws}

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
            min_move = min(min_move, minimax([child], [opp], depth-1, alpha, beta, False, state, info))
            beta = min_move
            if alpha >= beta:
                break
        if min_move >= max_move:
            move_to_make = child
            max_move = min_move
            alpha = max_move

    return move_to_make

def generate_children(dictionary, generate_throws, throws_left, colour, symbol):

    if generate_throws:
        final_moves_suggestions = generate_throw_children(dictionary, throws_left, colour, symbol)
        return final_moves_suggestions

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
                        if not out_of_board(swing_loc) and swing_loc not in hex_suggestions and swing_loc != loc:
                            final_moves_suggestions.append(swing(loc, swing_loc))

    return final_moves_suggestions

def first_throw(colour):
    tok = ['r', 'p', 's'][randint(0,2)]
    if   colour == 'lower':
        loc =  (-4, randint(0, 4))
    elif colour == 'upper':
        loc = (4, -randint(0, 4))
    return throw(tok, loc)

def need_throw(state):
    p_toks = list(itertools.chain.from_iterable(state['player'].values()))
    o_toks = list(itertools.chain.from_iterable(state['opponent'].values()))
    game = play_rps(p_toks + o_toks)

    if not game:
        return False, False, '', ''

    toks = ['r', 's', 'p']
    for t in range(3):
        win = toks[t]
        lose = toks[(t+1)%3]
        if game[0] == lose:
            tok = win

    if game[0] in p_toks and game[0] not in o_toks:
        return False, True, '', tok
    elif game[0] in o_toks and game[0] not in p_toks:
        return True, False, tok, ''
    elif game[0] in p_toks and game[0] in o_toks:
        return True, True, tok, tok
    else:
        return False, False, '', ''

def generate_throw_children(dictionary, throws_left, colour, symbol):
    
    wide = {4: range(-4, 1), 3: range(-4, 2), 2: range(-4, 3), 1: range(-4, 4), 0: range(-4, 5),
           -3: range(-3, 5), -2: range(-2, 5), -1: range(-1, 5), -4: range(0, 5)}

    if colour == 'upper':
        min_d = min(4, 4-(10-throws_left))
        max_d = max(4, 4-(10-throws_left))
    elif colour == 'lower':
        min_d = min(-4, -4+(10-throws_left))
        max_d = max(-4, -4+(10-throws_left))

    depth = range(min_d, max_d, 1)

    throw_hexs = []
    for d in depth:
        width = wide[d]
        for w in width:
            open_hex = (d, w)
            if (d, w) not in dictionary.keys():
                throw_hexs.append(throw(symbol, open_hex))

    return throw_hexs
    
def set_colours(colour):
    if colour == 'upper':
        return 'upper', 'lower'
    elif colour == 'lower':
        return 'lower', 'upper' 