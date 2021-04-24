from team_name.functions import update_state

class Player:

    state = {}

    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        # TODO:
        1. Set up an internal representation of the game state.
        2. player is "upper" or "lower
        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """

        # put your code here
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # Needs to check for tokens on the same hex and kill the correct token  
        state = update_state(state, opponent_action, player_action)
        # put your code here

