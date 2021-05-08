from XAEA_Xii.evaluation import evaluation
from XAEA_Xii.board import update_state
import numpy as np

def minimax(Player, max_player, min_player, depth, alpha, beta, is_max, state):
    if depth == 0:
        return Player.evaluation(max_player, min_player, depth, alpha, beta, is_max, state)
    if is_max:
        max_move = -np.inf
        for child in max_player:
            state = update_state(state, child)
            max_move = max(max_move, minimax(child, min_player, depth - 1, alpha, beta, False, state))
            alpha = max(alpha, max_move)
            if alpha >= beta:
                break
        return max_move
    else:
        min_move = np.inf
        for child in min_player: 
            state = update_state(state, child)
            min_move = min(min_move, minimax(max_player, min_player, depth - 1, alpha, beta, True, state))
            beta = min(alpha, min_move)
            if alpha >= beta:
                break
        return min_move

    
    