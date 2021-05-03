def throw(token, loc):
    return ("THROW", token, loc)
def slide(old_loc, new_loc):
    return ("SLIDE", old_loc, new_loc)
def swing(old_loc, new_loc):
    return ("SWING", old_loc, new_loc)