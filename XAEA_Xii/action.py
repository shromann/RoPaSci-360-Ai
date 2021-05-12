from XAEA_Xii.const import board, adjacent_squares, base
from XAEA_Xii.update import update, win
from collections import defaultdict
from random import randint
from math import ceil
from numpy import inf
import itertools
import copy


# ------------------------------------------------------------ AI ----------------------------------------------------------

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
    depth = 1

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

# ---------------------------------------------------  important functions -------------------------------------------------

def minimax(max_player, min_player, depth, alpha, beta, is_max, state):

    game_state = copy.deepcopy(state)
    if depth == 0:
        return evaluation(state)
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

def child_of(team, state):

    throws = []
    slides = []
    swings = []
    
    # throws
    if state[team + "_throws"] < 9:
        sym = select_sym(team, state)
        if sym:
            throws += throw_child(team, state, sym)


    # slides
    for loc in state[team]:
        slides += slide_child(loc, state[team].keys())

    # swings
    for loc_1 in state[team]:
        for loc_2 in state[team]:
            if loc_1 != loc_2 and loc_2 in neigh(loc_1):
                swings += swing_child(loc_1, loc_2, neigh(loc_1))

    childs = throws + swings + slides
    return childs

def sep(dictionary):
    r, p, s = [], [], []
    for k in dictionary:
        if 'r' in dictionary[k]:
            r.append(k)
        if 'p' in dictionary[k]:
            p.append(k)
        if 's' in dictionary[k]:
            s.append(k)
    return r, p, s

def find_min_dist(player, opponent):

    if player == [] or opponent == []:
        return 9

    dists = []
    for p in player:
        for o in opponent:
            dists.append(dist(p, o))
    return min(dists)

def best_distance(game_state):
    player_r, player_p, player_s = sep(game_state['player'])
    opponent_r, opponent_p, opponent_s = sep(game_state['opponent'])

    min_dist_r_s = find_min_dist(player_r, opponent_s)
    min_dist_p_r = find_min_dist(player_p, opponent_r)
    min_dist_s_p = find_min_dist(player_s, opponent_p)

    val = 1/(min(min_dist_r_s, min_dist_p_r, min_dist_s_p))
    return val

def evaluation(game_state):

    throw_weight = 2
    on_board_weight = 1
    num_captures_weight = 3
    game_dists_weight = 0.5

    opp_num_tokens = len(game_state['opponent'].values())
    player_num_tokens = len(game_state['player'].values())
    diff_in_tokens = player_num_tokens - opp_num_tokens
    diff_in_throws = game_state['player_throws'] - game_state['opponent_throws']
    num_captures = game_state['opponent_throws'] - opp_num_tokens
    invinciblity = check_invincible(game_state)
    dists_score = best_distance(game_state)

    # board state where both players have no throws so invincible tokens are truly invincible
    if game_state['player_throws'] == 0 and game_state['opponent_throws'] == 0:
        invincible_weight = 10

    # board state where opponent has no throws but player does have
    elif game_state['opponent_throws'] == 0:
        # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
        if invinciblity < 0:
            invincible_weight = 5

    elif game_state['player_throws'] == 0:
        # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
        if invinciblity > 0:
            invincible_weight = 5
    else:
        invincible_weight = 5
    
    return (invincible_weight*invinciblity) + (throw_weight*diff_in_throws) + (on_board_weight*diff_in_tokens) + (num_captures_weight*num_captures) + (game_dists_weight*dists_score)

def check_invincible(board_state):
    # Get the unique token types of player and opponent
    player_tokens = set(itertools.chain.from_iterable(board_state['player'].values()))
    oppo_tokens = set(itertools.chain.from_iterable(board_state['opponent'].values()))
    diff_in_invincible = 0

    # play rps for each player type against each oppo type
    for player_type in player_tokens:
        can_be_defeated = 0
        for oppo_type in oppo_tokens:
            # If win function is -1, that means our token type is not invincible 
            if win(player_type, oppo_type) == -1:
                can_be_defeated = 1
        # If it is not invincible, don't add it to the count of invincible tokens otherwise do add it
        if can_be_defeated != 1:
            diff_in_invincible += 1

    # Same as above code but deincrementing if opponent has the invincible token
    for oppo_type in player_tokens:
        can_be_defeated = 0
        for player_type in oppo_tokens:
            if win(oppo_type, player_type) == -1:
                can_be_defeated = 1
        if can_be_defeated != 1:
            diff_in_invincible -= 1

    return diff_in_invincible 

# --------------------------------------------------- helper functions -----------------------------------------------------
def neigh(loc):
    nexts = list(adjacent_squares.values())
    nexts = list(map(lambda x:(loc[0]+x[0], loc[1]+x[1]), nexts))
    return nexts

def adjacents(loc):
    nexts = neigh(loc)
    nexts = list(filter(lambda x: x[0] in board.keys() and x[1] in board[x[0]], nexts))
    return nexts

def slide_child(loc, reserved):
    slides = adjacents(loc)
    slides = filter(lambda x: x not in reserved, slides)
    slides = list(map(lambda x: slide(loc, x), slides ))
    return slides

def swing_child(loc_1, loc_2, reserved):

    swings = adjacents(loc_2)
    swings = list(filter(lambda x: x not in reserved, swings))
    swings = list(map(lambda x: swing(loc_1, x), swings))
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

    tt = []
    toks = ['r', 's', 'p']
    for t in range(3):
        win, lose = toks[t], toks[(t+1)%3]
        if win not in player and lose in opponent:
            tt.append(win)

    if len(tt) >= 1:
        return tt.pop()

def dist(loc_1, loc_2):
    return (abs(loc_1[0] - loc_2[0]) 
          + abs(loc_1[0] + loc_1[1] - loc_2[0] - loc_2[1])
          + abs(loc_1[1] - loc_2[1])) / 2

def throw(token, loc):
    return ("THROW", token, loc)

def slide(old_loc, new_loc):
    return ("SLIDE", old_loc, new_loc)

def swing(old_loc, new_loc):
    return ("SWING", old_loc, new_loc)