from XAEA_Xii.board import update_action
from XAEA_Xii.move import make_move

class Player:
    """
    Internal Representation:
        dictionary: 
            - Key: (r, q)
            - Value: "atype"
    """


    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        # TODO:
        1. Set up an internal representation of the game state.
        2. player is "upper" or "lower
        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).

        - what does it mean to play upper or lower?
        - set up internal game board
        """
        self.color = player
        self.state = {"player": {}, "opponent": {}}

        self.player_TD = 0
        self.opponent_TD = 0
        
        self.player_throws = 0
        self.opponent_throws = 0


    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        return make_move(state, self.player_TD, self.opponent_TD)
        
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        update_action(self.board["player"],   player_action)
        update_action(self.board["opponent"], opponent_action)
        


        
        
