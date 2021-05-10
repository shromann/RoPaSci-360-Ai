from collections import defaultdict
from XAEA_Xii.action import action
from XAEA_Xii.update import update, gameplay, self_kill

class Player:
    
    def __init__(self, player):
        
        self.state  = {"player": defaultdict(list), "opponent": defaultdict(list), "player_throws": 0, "opponent_throws": 0, "colour": player}
        
    def action(self):
        return action(self.state)

    def update(self, opponent_action, player_action):
        
        update(self.state, 'player', player_action, main=True)
        update(self.state, 'opponent', opponent_action, main=True)
        gameplay(self.state)
 






    
