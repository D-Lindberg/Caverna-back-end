from constants import CAVERNA_ACTIONS as CA

class Dwarf:
    def __init__(self, isOffspring, ID):
        self.ID = ID
        self.isOffspring = isOffspring
        self.isUsed = isOffspring
        self.weapon_level = 0

    def get_food_requirements(self):
        return 1 if self.isOffspring else 2

    def add_weapon(self, action_name):
        if 'Weapon' in action_name and 'Level' in action_name and 'Dwarf' not in action_name:
            self.weapon_level = int(action_name.split(' ')[1])

    def increase_weapon_level(self):
        if self.weapon_level < 14 and self.weapon_level > 0:
            self.weapon_level += 1

