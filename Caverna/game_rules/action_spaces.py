from constants import ACTION_SPACE_TYPES as AST
from action_grouper import Action_Group


#refence rule appendix page A6 under "Part 3: The Action Spaces"
class Game_Action_Space:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.is_used = False
        self._action_group = self.unpack_this(kwargs.get['action_group'], 0)
        self.is_clearing_prevented = False

        self._dog_static = kwargs.get('dog_static', 0)

        self._donkey_initial = kwargs.get('donkey_initial', 0)
        self._donkey_accumulating = kwargs.get('donkey_accumulating', 0)
        self._donkey_current = self._donkey_initial

        self._food_initial = kwargs.get('food_initial', 0)
        self._food_accumulating = kwargs.get('food_accumulating', 0)
        self._food_current = self._food_initial
        self._food_static = kwargs.get('food_static', 0)

        self._gold_static = kwargs.get('gold_static', 0)

        self._ore_initial = kwargs.get('ore_initial', 0)
        self._ore_accumulating = kwargs.get('ore_accumulating', 0)
        self._ore_current = self._ore_initial
        self._ore_static = kwargs.get('ore_static', 0)

        self._pumpkin_initial = kwargs.get('pumpkin_initial', 0)
        self._pumpkin_accumulating = kwargs.get('pumpkin_accumulating', 0)
        self._pumpkin_current = self._pumpkin_initial
        self._pumpkin_static = kwargs.get('pumpkin_static', 0)

        self._ruby_initial = kwargs.get('ruby_initial', 0)
        self._ruby_accumulating = kwargs.get('ruby_accumulating', 0)
        self._ruby_current = self._ruby_initial
        self._ruby_static = kwargs.get('ruby_static', 0)

        self._sheep_initial = kwargs.get('sheep_initial', 0)
        self._sheep_accumulating = kwargs.get('sheep_accumulating', 0)
        self._sheep_current = self._sheep_initial

        self._stone_initial = kwargs.get('stone_initial', 0)
        self._stone_accumulating = kwargs.get('stone_accumulating', 0)
        self._stone_current = self._stone_initial
        self._stone_static = kwargs.get('stone_static', 0)

        self._wheat_static = kwargs.get('wheat_static', 0)

        self._wood_initial = kwargs.get('wood_initial', 0)
        self._wood_accumulating = kwargs.get('wood_accumulating', 0)
        self._wood_current = self._wood_initial
        self._wood_static = kwargs.get('wood_static', 0)

        self.accumulating_resources_total = self.get_accumulating_resources_total()

    def get_is_used(self):
        return self._action_group.get_is_used() or self.type == AST.Skip_Round

    def mark_action_used(self, action_name):
        self._action_group.mark_action_used(action_name)

    def mark_as_finished(self):
        self._action_group.set_is_used(True)
    
    def get_accumulating_resources_total(self):
        total = self._wood_current
        total += self._stone_current
        total += self._ore_current
        total += self._food_current
        total += self._ruby_current
        total += self._sheep_current
        total += self._donkey_current
        total += self._wheat_current
        total += self._pumpkin_current

    def cleanup_and_add_resources(self, is_solo_game):
        if self.name == AST.Skip_Round:
            return
        self._action_group.set_is_used(False)
        if self.accumulating_resources_total == 0 or self.accumulating_resources_total >= 6 and is_solo_game and not self.is_clearing_prevented:
            self._wood_current = self._wood_initial
            self._stone_current = self._stone_initial
            self._ore_current = self._ore_initial
            self._food_current = self._food_initial
            self._ruby_current = self._ruby_initial
            self._sheep_current = self._sheep_initial
            self._donkey_current = self._donkey_initial
            self._wheat_current = self._wheat_initial
            self._pumpkin_current = self._pumpkin_initial
        else:
            self._wood_current += self._wood_accumulating
            self._stone_current += self._stone_accumulating
            self._ore_current += self._ore_accumulating
            self._food_current += self._food_accumulating
            self._ruby_current += self._ruby_accumulating
            self._sheep_current += self._sheep_accumulating
            self._donkey_current += self._donkey_accumulating
            self._wheat_current += self._wheat_accumulating
            self._pumpkin_current += self._pumpkin_accumulating

    def unpack_this(self, package, order):
        if len(package) == 1:
            return Action_Group(package[0], True, order)
        nested = Action_Group("Nested", False, order)
        nested.type = package[1]
        for index, element in enumerate(package[0]):
            if type(element) == type('abcdefghijklmnopqrstuvwxyz'):
                nested.actions.append(Action_Group(element, True, index))
            else:
                nested.actions.append(self.unpack_this(element, index))
        





