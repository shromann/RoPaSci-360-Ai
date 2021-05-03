def update_state(store, action, n_throws):
    move_type = action[0]
    end_location = action[2]

    if move_type is "THROW":
        token = action[1]

    elif move_type in ["SLIDE", "SWING"]:
        token = store[action[1]].pop()

    store[end_location].append(token)