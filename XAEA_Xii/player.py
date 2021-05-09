from XAEA_Xii.board import update_player_state, play_game
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