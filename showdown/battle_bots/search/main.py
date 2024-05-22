from ..helpers import format_decision
from ..helpers import pick_safest_move_using_dynamic_search_depth_custom
from showdown.battle import Battle


class BattleBot(Battle):
    def __init__(self, *args, **kwargs):
        super(BattleBot, self).__init__(*args, **kwargs)
    def find_best_move(self):
        battles = self.prepare_battles(join_moves_together=True)
        safest_move = pick_safest_move_using_dynamic_search_depth_custom(battles)
        return format_decision(self, safest_move)
