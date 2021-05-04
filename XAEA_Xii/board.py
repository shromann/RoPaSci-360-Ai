def update_state(state, action):
    mv_type = action[0]
    loc     = action[2]

    if mv_type == 'THROW':
        token = action[1]
    elif mv_type in ['SLIDE', 'SWING']:
        token = state[action[1]].pop()
        # remove from states if no token on that hex
        if not state[action[1]]:
            del state[action[1]]
    
    state[loc].append(token)
    return state


