from XAEA_Xii.functions import update_state
from XAEA_Xii.minimax import minimax
import numpy as np

def multi_minimax(max_player, min_player, depth, state):
    move_to_make = 0
    max_move = -np.inf
    alpha = -np.inf
    for child in max_player:
        state = update_state(state, child)
        min_move = np.inf
        beta = np.inf
        for opp in min_player:
            min_move = min(min_move, minimax(child, opp, depth-1, alpha, beta, False, state))
            beta = min_move
            if alpha >= beta:
                break
        if min_move >= max_move:
            move_to_make = child
            max_move = min_move
            alpha = max_move
    return move_to_make