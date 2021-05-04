from XAEA_Xii.eval import beat_possible
from XAEA_Xii.util import throw, slide, swing
from XAEA_Xii.functions import out_of_board



def throw_action(throw_token, opponent, opponent_throws, colour, state):
    """
    Use multi-minimax to choose the best throw location
    return: loc (r, q)
    """
    
    

def swing_slide_action(player, opponent, opponent_throws, colour, state):
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
    for child in player_queue:
        player_new_loc = child[0]
        player_old_loc = child[1]
        player_type = child[2]

        # Change based on how to update state
        state = update_state(state, player_loc, player_type)
        min_move = np.inf
        beta = np.inf
        for opp in opponent_queue:
            opponent_loc = opp[0]
            min_move = min(min_move, minimax(player_loc, opponent_loc, depth-1, alpha, beta, False, state))
            beta = min_move
            if alpha >= beta:
                break
        if min_move >= max_move:
            move_to_make = child
            max_move = min_move
            alpha = max_move
    return ("SLIDE", move_to_make[1], move_to_make[0])
    


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
        atype, old_loc, new_loc = swing_slide_action(player, opponent, colour, state) # multi-minimax: slide / swing
        return swing_slide_action(atype, old_loc, new_loc) 


# |---------------------------------------------------------------------------|

def generate_children(dictionary):
    adjacent_squares = {
    "UR":(1, 0), "UL":(+1, -1), "L":(0, -1), 
    "DL":(-1, 0), "DR":(-1, +1), "R":(0, +1)}
    
    # In the move_suggestions will be tuples of (newlocation, oldlocation, type of token)
    moves_suggestions = []
    queue = dictionary.keys()

    # Need to remove duplicate suggestions eg a hex is slide and swing away from curr hex
    for loc in dictionary.keys():
        #loc = dictionary[0]
        for value in adjacent_squares.values():
            new_loc = (loc[0] + value[0], loc[1] + value[1])

            if not out_of_board(new_loc):
                moves_suggestions.append(new_loc, loc, dictionary[loc])
            
                if new_loc in dictionary.keys():
                    for values in adjacent_squares.values():
                        swing_loc = (new_loc[0] + values[0], new_loc[1] + values[1])

                        if not out_of_board(swing_loc):
                            moves_suggestions.append(swing_loc, loc, dictionary[loc])

    return move_suggestions