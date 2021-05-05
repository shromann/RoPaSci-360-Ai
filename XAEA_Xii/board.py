def play_rps(state_loc):
    """
    Minimizez the hex at a particular location. The hex can have both upper and lowers tokens as well as its own type. 
    """
    toks = ['r', 's', 'p']
    to_remove = []
    for t in range(3):
        win = toks[t]
        lose = toks[(t+1)%3]
        if (win in state_loc and lose in state_loc) or (win.upper() in state_loc and lose in state_loc):
            to_remove.append(lose)
        if (win.upper() in state_loc and lose.upper() in state_loc) or (win in state_loc and lose.upper() in state_loc):
            to_remove.append(lose.upper())
        
    for r in to_remove:
        state_loc = list(filter(lambda t: t != r, state_loc))
    return state_loc            


def update_state(state, action):
    mv_type = action[0]
    loc     = action[2]

    if mv_type == 'THROW':
        token = action[1]
    elif mv_type in ['SLIDE', 'SWING']:
        token = state[action[1]].pop()
        if not state[action[1]]:
            del state[action[1]]
    
    state[loc].append(token)
    state[loc] = play_rps(state[loc]) # minimize

    return state



# INCASE 
# def eval(player, old_state, new_state):
#     if   player == 'lower':
#         ro, pa, sci = 'R', 'P', 'S'
#     elif player == 'upper':
#         ro, pa, sci = 'r', 'p', 's'
    
#     if ro in old_state or pa in old_state or sci in old_state:
#         if not (ro in new_state or pa in new_state or sci in new_state):
#             return 1
    


    


