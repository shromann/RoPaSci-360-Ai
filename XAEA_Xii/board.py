def play_rps(state_loc):
    # Minimizez the hex at a particular location. The hex can have both upper and lowers tokens as well as its own type. 
    
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


def update_player_state(state, action):

    mv_type = action[0]
    loc     = action[2]

    if mv_type == 'THROW':
        token = action[1]
    elif mv_type in ['SLIDE', 'SWING']:
        # print(action[1], state)
        if action[1] in state.keys():
            token = state[action[1]].pop()
            if not state[action[1]]:
                del state[action[1]]
        else:
            return state

    state[loc].append(token)
    #state[loc] = play_rps(state[loc]) # minimize

    return state

def update_state(state, action):

    state['player'] = update_player_state(state['player'], action)
    state['opponent'] = update_player_state(state['opponent'], action)
    
    return state

def play_game(state):
    player = state['player']
    opponent = state['opponent']

    # There can only be two locations that need to be looked at each round to check overlapping tokens
    # Those locations are the throw,slide,swing new location (always the 2nd index of an action move)
    overlaps = []
    for p in player.keys():
        for o in opponent.keys():
            if o == p:
                overlaps.append(o)


    if overlaps:    
        for o in overlaps:
            feild = play_rps(player[o] + opponent[o])       
            if feild in player[o]:
                del opponent[o]
            if feild in opponent[o]:
                del player[o]
     
    return state



