board = {4: range(-4, 1),  3: range(-4, 2),  2: range(-4, 3),  1: range(-4, 4), 0: range(-4, 5), 
        -3: range(-3, 5), -2: range(-2, 5), -1: range(-1, 5), -4: range(0, 5)}

adjacent_squares = {"UR":(1, 0),  "UL":(+1, -1), "L":(0, -1), 
                    "DL":(-1, 0), "DR":(-1, +1), "R":(0, +1)}

base = {'upper': 1, 'lower': -1}