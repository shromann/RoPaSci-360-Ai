from XAEA_Xii.board import update_state
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
        """
        Called once at the beginning of a game to initialise this player.
        # TODO:
        1. Set up an internal representation of the game state. -> DONE
        2. player is "upper" or "lower -> DONE
        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).

        [(0, 0)]: [s, s] -> 2 sci on (0, 0)
        slide (0, 0), (0, 1)
        use pop function.  


        - what does it mean to play upper or lower?
        - set up internal game board
        """
        self.color = player
        self.state = {"player": defaultdict(list), "opponent": defaultdict(list)}
        
        self.player_throws = 9
        self.opponent_throws = 9


    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        return make_move(state, self.player_throws, self.opponent_opponent)
        
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        if opponent_action[0] == 'THROW':
            self.opponent_throws -= 1
        elif player_action[0] == 'THROW':
            self.player_throws -= 1
        
        update_state(self.board["player"],   player_action)
        update_state(self.board["opponent"], opponent_action)

