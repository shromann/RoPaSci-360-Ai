def update_state(Upper_dict, Lower_dict, player_location, opponent_action, player_action):
    # When we are the lower player
    if player_location == "lower":

        # When both players throw
        if player_action[0] == "THROW" and opponent_action[0] == "THROW":
            Lower_dict = throw(Lower_dict, player_action)
            Upper_dict = throw(Upper_dict, opponent_action)
            
        # When player throws and opponent slides/swings    
        elif player_action[0] == "THROW":
            Lower_dict = throw(Lower_dict, player_action)
            Upper_dict = non_throw(Upper_dict, opponent_action)

        # When opponent throws and player slides/swings
        elif opponent_action[0] == "THROW":
            Upper_dict = throw(Upper_dict, opponent_action)
            Lower_dict = non_throw(Lower_dict, player_action)
            
        # Both players swings/slides
        else:
            Lower_dict = non_throw(Lower_dict, player_action)
            Upper_dict = non_throw(Upper_dict, opponent_action)

    else:
        # When both players throw
        if player_action[0] == "THROW" and opponent_action[0] == "THROW":
            Upper_dict = throw(Upper_dict, player_action)
            Lower_dict = throw(Lower_dict, opponent_action)
            
        # When player throws and opponent slides/swings    
        elif player_action[0] == "THROW":
            Upper_dict = throw(Upper_dict, player_action)
            Lower_dict = non_throw(Lower_dict, opponent_action)

        # When opponent throws and player slides/swings
        elif opponent_action[0] == "THROW":
            Lower_dict = throw(Lower_dict, opponent_action)
            Upper_dict = non_throw(Upper_dict, player_action)
            
        # Both players swings/slides
        else:
            Upper_dict = non_throw(Upper_dict, player_action)
            Lower_dict = non_throw(Lower_dict, opponent_action)


def throw(dictionary, action):
    token_type = action[1]
    hex = action[2]
    dictionary[token_type] = dictionary[token_type].append(hex)
    return dictionary

def non_throw(dictionary, action):
    all_token_types = ['s', 'r', 'p']
    curr_hex = action[1]
    new_hex = action[2]
    for token_type in all_token_types:
        if curr_hex in dictionary[token_type]:
            dictionary[token_type].append(new_hex)
            dictionary[token_type].remove(curr_hex)
            break
    return dictionary

def kill_tokens():
    # NOT FINISHED
    player_types_to_check = opposite_types(player_token_type)
    player_to_remove_list = []
    for token_type in player_types_to_check:
        if player_move_hex in Lower_dict[token_type] and win(player_token_type, token_type):
            player_to_remove_list.append(Lower_dict, token_type)
        elif player_move_hex in Upper_dict[token_type] and win(player_token_type, token_type):
            player_to_remove_list.append(Upper_dict, token_type)
        elif player_move_hex in Lower_dict[token_type] and win(token_type, player_token_type):
            player_to_remove_list.append(Lower_dict, player_token_type)
        elif player_move_hex in Upper_dict[token_type] and win(token_type, player_token_type):
            player_to_remove_list.append(Upper_dict, player_token_type)
def opposite_types(token_type):
    if token_type == 's':
        return ('p','r')
    elif token_type == 'p':
        return ('s','r')
    else:
        return ('p','s')

def win(A , B):
    if A == 's' and B == 'p':
        return 1
    if A == 'p' and B == 'r':
        return 1
    if A == 'r' and B == 's':
        return 1
    if A == 's' and B == 'r':
        return -1
    if A == 'p' and B == 's':
        return -1
    if A == 'r' and B == 'p':
        return -1
    return 0
