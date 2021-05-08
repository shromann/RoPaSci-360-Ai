from XAEA_Xii.board import update_player_state
from XAEA_Xii.move import make_move

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

        return make_move(self.state, self.player_throws, self.opponent_throws, self.colour)


    def update(self, opponent_action, player_action):

        if opponent_action[0] == 'THROW':
            self.opponent_throws -= 1
        if player_action[0] == 'THROW':
            self.player_throws   -= 1

        self.state["player"]   = update_player_state(self.state["player"]  ,   player_action)
        self.state["opponent"] = update_player_state(self.state["opponent"], opponent_action)
<<<<<<< HEAD


=======
        
>>>>>>> parent of bce3c3c... before the big change
