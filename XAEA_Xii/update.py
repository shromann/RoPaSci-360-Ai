import copy

def update(state, team, action, main = False):

    mv_type = action[0]
    loc = action[2]

    if mv_type == "THROW":
        token = action[1]
        state[team + "_throws"] += 1

    elif mv_type in ["SLIDE", "SWING"]:
        try:
            token = state[team][action[1]].pop()
            if not state[team][action[1]]:
                del state[team][action[1]]
        except IndexError:
            return 
        except KeyError:
            return

    state[team][loc].append(token)

    if not main:
        gameplay(state)
  
def gameplay(state):
    game = []
    player = copy.deepcopy(state['player'])
    opponent = copy.deepcopy(state['opponent'])
    for play in player:
        for opp in opponent:
            if play == opp:
                score = win(state['player'][play], state['opponent'][opp])
                if score == 1:
                    game.append(('opponent', opp))
                elif score == -1:
                    game.append(('player', play))

    for team, loc in game:
        del state[team][loc]
    
    self_kill(state['player'])
    self_kill(state['opponent'])

def self_kill(dictionary):
    for loc in dictionary:
        for tok1 in dictionary[loc]:
            for tok2 in dictionary[loc]:
                if tok1 != tok2:
                    if win(tok1, tok2) == 1:
                        winner = tok1
                    elif win(tok2, tok1) == -1:
                        winner = tok2
                    else:
                        break
                    dictionary[loc] = list(filter(lambda x: x == winner, dictionary[loc]))

def win(a, b):
    toks = ['r', 's', 'p']
    for t in range(3):
        win = toks[t]
        lose = toks[(t+1)%3]
        if win in a and lose in b:
            return 1
        if win in b and lose in a:
            return -1
    return 0

def tracking(state):
    state['track'][tuple(state['player'].keys()) + tuple(state['opponent'].keys())] += 1
