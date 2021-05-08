from XAEA_Xii.functions.py import win

def evaluation(max_player, min_player, depth, alpha, beta, is_max, game_state):
    throw_weight = 2
    on_board_weight = 1
    num_captures_weight = 1
    #closest_capture = 0.2
    opp_num_tokens = len(game_state[opponent].values())
    player_num_tokens = len(game_state[player].values())
    diff_in_tokens = player_num_tokens - opp_num_tokens
    diff_in_throws = self.player_throws - self.opponent_throws
    num_captures =  (self.opponent_throws - opp_num_tokens)

    # board state where both players have no throws so invincible tokens are truly invincible
    if self.player_throws == 0 and self.opponent_throws == 0:
        invincible_weight = 10

    # board state where opponent has no throws but player does have
    elif self.opponent_throws == 0:
        # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
        if check_invincible < 0:
            invincible_weight = 5
    
    elif self.player_throws == 0:
        # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
        if check_invincible > 0:
            invincible_weight = 5
    else:
        invincible_weight = 5
    diff_in_invin = check_invincible(game_state)
    return invincible_weight(diff_in_invin) + throw_weight(diff_in_throw) + on_board_weight(diff_in_tokens) + num_captures_weight(num_captures) 


    def check_invincible(board_state):
        # Get the unique token types of player and opponent
        player_tokens = set(board_state[player].values())
        oppo_tokens = set(board_state[opponent].values())
        diff_in_invincible = 0
        
        # play rps for each player type against each oppo type
        for player_type in player_tokens:
            can_be_defeated = 0
            for oppo_type in oppo_tokens:

                # If win function is -1, that means our token type is not invincible 
                if win(player_type, opponent_type) == -1:
                    can_be_defeated = 1
            # If it is not invincible, don't add it to the count of invincible tokens otherwise do add it
            if can_be_defeated != 1:
                diff_in_invincible += 1
        
        # Same as above code but deincrementing if opponent has the invincible token
        for oppo_type in player_tokens:
            can_be_defeated = 0
            for player_type in oppo_tokens:
                if win(oppo_type, player_type) == -1:
                    can_be_defeated = 1
            if can_be_defeated != 1:
                diff_in_invincible -= 1
        
        return diff_in_invincibile