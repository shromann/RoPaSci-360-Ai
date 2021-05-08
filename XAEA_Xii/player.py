from XAEA_Xii.board import update_player_state, update_state
from XAEA_Xii.move import make_move
from XAEA_Xii.evaluation import check_invincible

from collections import defaultdict

class Player:
    """
    Internal Representation:
        dictionary: 
            - Key: (r, q)
            - Value: "atype"
    """

    def __init__(self, player):

        self.colour = player
        self.state  = {"player": defaultdict(list), "opponent": defaultdict(list)}
        
        self.player_throws   = 9
        self.opponent_throws = 9

    def action(self):

        return make_move(super, self.state, self.player_throws, self.opponent_throws, self.colour)



    def update(self, opponent_action, player_action):

        if opponent_action[0] == 'THROW':
            self.opponent_throws -= 1
        if player_action[0] == 'THROW':
            self.player_throws   -= 1

        self.state["player"]   = update_player_state(self.state["player"]  ,   player_action)
        self.state["opponent"] = update_player_state(self.state["opponent"], opponent_action)
        print(self.state)


    def evaluation(self, max_player, min_player, depth, alpha, beta, is_max, game_state):
        throw_weight = 2
        on_board_weight = 1
        num_captures_weight = 1
        closest_capture = 0.2
        opp_num_tokens = len(self.state['opponent'].values())
        player_num_tokens = len(self.state['player'].values())
        diff_in_tokens = player_num_tokens - opp_num_tokens
        diff_in_throws = self.player_throws - self.opponent_throws
        num_captures =  (self.opponent_throws - opp_num_tokens)
        invincible = check_invincible(game_state)

        # board state where both players have no throws so invincible tokens are truly invincible
        if self.player_throws == 0 and self.opponent_throws == 0:
            invincible_weight = 10

        # board state where opponent has no throws but player does have
        elif self.opponent_throws == 0:
            # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
            if invincible < 0:
                invincible_weight = 5
        
        elif self.player_throws == 0:
            # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
            if invincible > 0:
                invincible_weight = 5
        else:
            invincible_weight = 5
        diff_in_invin = check_invincible(game_state)
        return invincible_weight*(diff_in_invin) + throw_weight*(diff_in_throws) + on_board_weight*(diff_in_tokens) + num_captures_weight*(num_captures) 




