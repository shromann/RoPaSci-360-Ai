from XAEA_Xii.const import board, adjacent_squares, base
from XAEA_Xii.update import update
from random import randint
from numpy import inf
import itertools
import copy
from collections import defaultdict

def action(state):
    game_state = state.copy()

    initial_action = first_throw(game_state)
    if initial_action:
        return initial_action

    return AI_move(game_state)
    

def first_throw(state):
    if state["player_throws"] == 0 and state["opponent_throws"] == 0:
        tok = ['r', 'p', 's'][randint(0,2)]
        loc = {'lower': (-4, randint(0, 4)), 'upper': (4, -randint(0, 4))}
        return throw(tok, loc[state['colour']])
    return False


def AI_move(state):
    
    game_state = copy.deepcopy(state)
    depth = 4

    move_to_make = 0
    max_move = -inf
    alpha = -inf

    player_queue = child_of('player', game_state)
    opponent_queue = child_of('opponent', game_state)

    for child in player_queue:
        game_state = copy.deepcopy(state)
        update(game_state, 'player', child)
        min_move = inf
        beta = inf
        for opponent in opponent_queue:
            min_move = min(min_move, minimax(child, opponent, depth - 1, alpha, beta, False, game_state))
            beta = min_move
            if alpha >= beta:
                break
        if min_move >= max_move:
            move_to_make = child
            max_move = min_move
            alpha = max_move
    
    return move_to_make


# ---------------------------------------------------  important function -------------------------------------------


def minimax(max_player, min_player, depth, alpha, beta, is_max, state):

    game_state = copy.deepcopy(state)

    # max_queue = filter(lambda x: x[2] == max_player[1] or x[1] in ['r', 'p', 's'], max_queue)
    # min_queue = filter(lambda x: x[2] == min_player[1] or x[1] in ['r', 'p', 's'], min_queue)

    if depth == 0:
        return evaluation()
    if is_max:
        max_queue = child_of('player', game_state)
        max_move = -inf
        for child in max_queue:
            game_state = copy.deepcopy(state)
            update(game_state, 'player', child)
            max_move = max(max_move, minimax(child, min_player, depth-1, alpha, beta, False, game_state))
            alpha = max(alpha, max_move)
            if alpha >= beta:
                break
        return max_move
    else:
        min_queue = child_of('opponent', game_state)
        min_move = inf
        for child in min_queue:
            game_state = copy.deepcopy(state)
            update(game_state, 'opponent', child)
            min_move = min(min_move, minimax(max_player, child, depth-1, alpha, beta, True, game_state))
            beta = min(alpha, min_move)
            if alpha >= beta:
                break
        return min_move

    return 0 


def evaluation():
    return 0

def child_of(team, state):

    throws = []
    slides = []
    swings = []
    
    # throws
    if state[team + "_throws"] < 9:
        sym = select_sym(team, state)
        if sym:
            throws += throw_child(team, state, sym)
            return throws

    # slides
    for loc in state[team]:
        slides += slide_child(loc, state[team].keys())

    # swings
    for loc_1 in state[team]:
        for loc_2 in state[team]:
            if loc_1 != loc_2 and loc_1 in adjacents(loc_2):
                swings += swing_child(loc_1, loc_2, slides + list(state[team].keys()))

    childs = throws + swings + slides
    return childs


# --------------------------------------------------- helper functions -----------------------------------------------------
def adjacents(loc):
    nexts = list(adjacent_squares.values())
    nexts = list(map(lambda x:(loc[0]+x[0], loc[1]+x[1]), nexts))
    nexts = list(filter(lambda x: x[0] in board.keys() and x[1] in board[x[0]], nexts))
    return nexts

def slide_child(loc, reserved):
    slides = adjacents(loc)
    slides = filter(lambda x: x not in reserved, slides)
    slides = list(map(lambda x: slide(loc, x), slides ))
    return slides

def swing_child(loc_1, loc_2, reserved):

    swings = adjacents(loc_2)
    swings = list(map(lambda x: swing(loc_1, x), filter(lambda x: x not in reserved, swings)))
    return swings 

def throw_child(team, state, sym):

    side = state['colour']
    depth = state[team + "_throws"] + 1
    if depth == 10:
        depth = 9

    if team == 'opponent':
        if side == 'upper':
            side = 'lower'
        else:
            side = 'upper'

    
    space = range(4*base[side], (4*base[side])-(depth*base[side]), -base[side])
    throw_space = [[(d, w) for w in board[d]] for d in space]
    throw_space = list(itertools.chain.from_iterable(throw_space))
    throw_space = filter(lambda x: x not in state[team], throw_space)

    throws  = list(map(lambda x: throw(sym, x), throw_space))
    return throws  
    
def select_sym(team, state):

    player = set(itertools.chain.from_iterable(state[team].values()))

    if team == 'player':
        opponent = set(itertools.chain.from_iterable(state['opponent'].values())) 
    if team == 'opponent':
        opponent = set(itertools.chain.from_iterable(state['player'].values())) 

    toks = ['r', 's', 'p']
    
    for t in range(3):
        win, lose = toks[t], toks[(t+1)%3]
        if win not in player and lose in opponent:
            return win
        
def throw(token, loc):
    return ("THROW", token, loc)

def slide(old_loc, new_loc):
    return ("SLIDE", old_loc, new_loc)

def swing(old_loc, new_loc):
    return ("SWING", old_loc, new_loc)