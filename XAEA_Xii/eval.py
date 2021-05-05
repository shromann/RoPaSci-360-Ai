from random import randint
from itertools import chain
from XAEA_Xii.board import play_rps


def to_throw(player, opponent, colour, player_throws, opponent_throws):
    """
    tells us if player can beat upper or not,
    if it can't, then returns a token to beat lower with 
    """

    tok = None    
    # first throw
    if player_throws == 9 and opponent_throws == 9:
        tok = ['r','p','s'][randint(0,2)]
        return tok

    # throw when player can't beat opponent
    player_tokens   = list(chain.from_iterable(player.values()))
    opponent_tokens = list(chain.from_iterable(opponent.values()))
    
    player_tok_counts = {k:player_tokens.count(k)   for k in ['r', 'p', 's']}
    opponent_tok_counts = {k:opponent_tokens.count(k) for k in ['r', 'p', 's']}

    # checking
    toks = ['r', 's', 'p']
    max_count = 0
    to_throw = []
    for t in range(3):
        if not player_tok_counts[toks[t]] and opponent_tok_counts[toks[(t+1)%3]]:
            if opponent_tok_counts[toks[(t+1)%3]] >= max_count:
                tok = toks[t]
                max_count = opponent_tok_counts[toks[(t+1)%3]]

    print(player_tok_counts, opponent_tok_counts, tok)

    return tok

