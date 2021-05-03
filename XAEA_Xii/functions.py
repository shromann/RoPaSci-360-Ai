import random

def update_state(Upper_dict, Lower_dict, player, opponent_action, player_action):
    # When we are the lower player
    if player =='lower':
        our_dict = Lower_dict
        their_dict = Upper_dict
    else:
        our_dict = Upper_dict
        their_dict = Lower_dict

    # When both players throw
    if player_action[0] == "THROW" and opponent_action[0] == "THROW":
        our_dict = throw(our_dict, player_action)
        their_dict = throw(their_dict, opponent_action)

    # When player throws and opponent slides/swings    
    elif player_action[0] == "THROW":
        our_dict = throw(our_dict, player_action)
        their_dict = non_throw(their_dict, opponent_action)

    # When opponent throws and player slides/swings
    elif opponent_action[0] == "THROW":
        their_dict = throw(their_dict, opponent_action)
        our_dict = non_throw(our_dict, player_action)
        
    # Both players swings/slides
    else:
        our_dict = non_throw(our_dict, player_action)
        their_dict = non_throw(their_dict, opponent_action)
        
    if player_action[2] != opponent_action[2]:
        kill_tokens(player_action[2], Lower_dict, Upper_dict)
        kill_tokens(opponent_action[2], Lower_dict, Upper_dict)
    else:
        kill_tokens(player_action[2], Lower_dict, Upper_dict)

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

def kill_tokens(new_hex, lower_dict, upper_dict):
    all_token_types = ['s', 'r', 'p']
    types_to_remove = []
    for token_type in all_token_types:
        if new_hex in lower_dict[token_type]:
            types_to_remove.append(lower_dict, token_type)
        if new_hex in upper_dict[token_type]:
            types_to_remove.append(upper_dict, token_type)
    
    if len(set(types_to_remove)) == 2:
        if 's' in types_to_remove and 'p' in types_to_remove:
            lower_dict = remove_hex_in_dict(new_hex, lower_dict, 'p')
            upper_dict = remove_hex_in_dict(new_hex, upper_dict, 'p')
        elif 'p' in types_to_remove and 'r' in types_to_remove:
            lower_dict = remove_hex_in_dict(new_hex, lower_dict, 'r')
            upper_dict = remove_hex_in_dict(new_hex, upper_dict, 'r')
        elif 'r' in types_to_remove and 's' in types_to_remove:
            lower_dict = remove_hex_in_dict(new_hex, lower_dict, 's')
            upper_dict = remove_hex_in_dict(new_hex, upper_dict, 's')

    if len(set(types_to_remove)) == 3:
        for token_types in all_token_types:
            lower_dict = remove_hex_in_dict(new_hex, lower_dict, token_types)
            upper_dict = remove_hex_in_dict(new_hex, upper_dict, token_types)

def remove_hex_in_dict(hex_loc, dictionary, token_type):
    if hex_loc in dictionary[token_type]:
        dictionary.remove(hex_loc)

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
    elif A == 'p' and B == 'r':
        return 1
    elif A == 'r' and B == 's':
        return 1
    elif A == 's' and B == 'r':
        return -1
    elif A == 'p' and B == 's':
        return -1
    elif A == 'r' and B == 'p':
        return -1
    return 0

def out_of_board(location):
    if location[0] < -4 or location[0] > 4 or location[1] < -4 or location[1] > 4 :
        return True
    elif location[0] == -4 and (location[1] > 4 or location[1] < 0):
        return True
    elif location[0] == -3 and (location[1] > 4 or location[1] < -1):
        return True
    elif location[0] == -2 and (location[1] > 4 or location[1] < -2):
        return True
    elif location[0] == -1 and (location[1] > 4 or location[1] < -3):
        return True
    elif location[0] == 0 and (location[1] > 4 or location[1] < -4):
        return True
    elif location[0] == 1 and (location[1] > 3 or location[1] < -4):
        return True
    elif location[0] == 2 and (location[1] > 2 or location[1] < -4):
        return True
    elif location[0] == 3 and (location[1] > 1 or location[1] < -4):
        return True
    elif location[0] == 4 and (location[1] > 0 or location[1] < -4):
        return True
    else:
        return False

def first_move(player):
    loc = (4,-2)
    if player == 'lower':
        loc = (-4, 2)

    