from XAEA_Xii.eval import beat_possible
from XAEA_Xii.util import throw, slide, swing




def throw_action(throw_token, opponenet, opponent_throws, colour):
    """
    Use multi-minimax to choose the best throw location
    return: loc (r, q)
    """
    
    

def swing_slide_action(player, opponenet, opponent_throws, colour):
    """
    Use multi-minimax to choose best slide / swing
    return: atype (slide/swing), old_loc: (r0, q0), new_loc (r_1, q_1)
    """


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
        token, loc = throw_token, throw_action(throw_token, opponent, opponent_throws, colour) # multi-minimax: throw
        return throw(token, loc)        
    else:
        atype, old_loc, new_loc = swing_slide_action(player, opponent, colour) # multi-minimax: slide / swing
        return swing_slide_action(atype, old_loc, new_loc) 


# |---------------------------------------------------------------------------|