from showdown.battle import Battle

from ..helpers import format_decision
from ..helpers import pick_safest_move_using_dynamic_search_depth_custom
from showdown.battle import Battle
from showdown.battle import get_possible_moves

class BattleBot(Battle):
    def __init__(self, *args, **kwargs):
        super(BattleBot, self).__init__(*args, **kwargs)
    def find_best_move(self):
        # TODO: implement search-based bot by replacing this function.
        #  see showdown/battle_bots/helpers.py for helper functions.
        # Get all possible moves
        moves = get_possible_moves(self)  # Import the get_possible_moves function
        # Initialize variables to track the best move and its damage
        safest_move = None
        best_damage = 0
        battles = self.prepare_battles(join_moves_together=True)
        # # Iterate over each move
        # for move in moves:
        #     # Simulate the battle with the current move
        #     simulated_battle = self.simulate_battle(move)
        #     # Calculate the damage caused by the opponent
        #     opponent_damage = simulated_battle.calculate_opponent_damage()
        #     # Calculate the damage caused by the bot
        #     bot_damage = simulated_battle.calculate_bot_damage()
        #     # Calculate the safety score based on opponent damage and bot damage
        #     safety_score = bot_damage - opponent_damage
        #     # Update the best move if the safety score is higher and the bot damage is greater than 0
        #     if safety_score > best_damage and bot_damage > 0:
        #         safest_move = move
        #         best_damage = safety_score

        safest_move = pick_safest_move_using_dynamic_search_depth_custom(battles)

        return format_decision(self, safest_move)