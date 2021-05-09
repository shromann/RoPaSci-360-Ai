from XAEA_Xii.board import update_player_state, play_game, play_rps
from XAEA_Xii.move import make_move

from collections import defaultdict
import copy

class Player:
    
    def __init__(self, player):

        self.colour = player
        self.state  = {"player": defaultdict(list), "opponent": defaultdict(list)}
        
        self.player_throws   = 9
        self.opponent_throws = 9

    def action(self):    

        state = copy.deepcopy(self.state)
        player_throws = copy.deepcopy(self.player_throws)
        opponent_throws = copy.deepcopy(self.opponent_throws)

        action = make_move(self.state, self.player_throws, self.opponent_throws, self.colour)

        self.state = state
        self.player_throws = player_throws
        self.opponent_throws = opponent_throws

        return action

    def update(self, opponent_action, player_action):

        if opponent_action[0] == 'THROW':
            self.opponent_throws -= 1
        if player_action[0] == 'THROW':
            self.player_throws   -= 1

        opponent_new_loc = opponent_action[2]
        player_new_loc = player_action[2]
        if player_action[2] != opponent_action:
            self.state["player"]   = update_player_state(self.state["player"]  ,   player_action)
            self.state["opponent"] = update_player_state(self.state["opponent"], opponent_action)
            self.state = play_game(self.state, player_new_loc, opponent_new_loc)

            # Play_rps has to be after play_game as if on a hex upper has 'p', 's' and lower has 'r'
            # This ensures that all 3 tokens are killed
            # If play_rps is first, upper would have 's' remaining and lower would have 'r' remaining
            # So when play_game is called, the 's' would still be remaining when all 3 should have been killed
            self.state["player"]   = play_rps(self.state["player"], player_action[2])
            self.state["opponent"] = play_rps(self.state["opponent"], opponent_action[2])