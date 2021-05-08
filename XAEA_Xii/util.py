def throw(token, loc):
    return ("THROW", token, loc)
def slide(old_loc, new_loc):
    return ("SLIDE", old_loc, new_loc)
def swing(old_loc, new_loc):
    return ("SWING", old_loc, new_loc)

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