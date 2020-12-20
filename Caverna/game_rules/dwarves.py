from constants import CAVERNA_ACTIONS as CA, DWARF_TEXT as DT


class Dwarf:
    def __init__(self, is_offspring, dwarf_id):
        self.ID = dwarf_id
        self.isOffspring = is_offspring
        self.isUsed = is_offspring
        self.weapon_level = 0

    def get_food_requirements(self):
        return 1 if self.isOffspring else 2

    def add_weapon(self, action_name):
        if 'Weapon' in action_name and 'Level' in action_name and 'Dwarf' not in action_name:
            self.weapon_level = int(action_name.split(' ')[1])

    def increase_weapon_level(self):
        if 14 > self.weapon_level > 0:
            self.weapon_level += 1


class DwarfManager:
    def __init__(self, **kwargs):
        self.dwarves = kwargs.get('dwarves', [Dwarf(False, 1), Dwarf(False, 2)])
        self.active_dwarf_index = kwargs.get('active_dwarf_index', 0)

    @property
    def remaining_dwarves(self):
        remaining = []
        for dwarf in self.dwarves:
            if not dwarf.isUsed:
                remaining.append(dwarf)
        return remaining

    @property
    def remaining_dwarf_count(self):
        return len(self.remaining_dwarves)

    @property
    def has_remaining_dwarves(self):
        return self.remaining_dwarf_count > 0

    def reset_dwarves(self):
        self._active_dwarf_index = 0
        for dwarf in self._dwarves:
            dwarf.isOffspring = False
            dwarf.isUsed = False
        self._dwarves.sort(key=lambda x: x.weapon_level)
        for i, dwarf in enumerate(self.dwarves):
            dwarf.ID = i + 1

    def set_dwarf_used(self):
        for dwarf in self.dwarves:
            if dwarf.isUsed:
                continue
            dwarf.isUsed = True
            break

    def action_finished(self):
        self.active_dwarf_index += 1

    def arm_active_dwarf(self, action_name):
        self.dwarves[self.active_dwarf_index].add_weapon(action_name)

    @property
    def get_status_of_dwarves(self):
        status = []
        for dwarf in self.dwarves:
            status.append(f"{dwarf.weapon_level}_{dwarf.isUsed}_{dwarf.isOffspring}")
        return status

    def add_dwarf(self):
        dwarf = Dwarf(True, len(self.dwarves + 1))
        self.dwarves.append(dwarf)

    @property
    def dwarf_count(self):
        return len(self.dwarves)

    @property
    def child_count(self):
        chhildren = list(filter(lambda x: x.isOffspring, self.dwarves))
        return len(chhildren)

    @property
    def adult_count(self):
        return self.dwarf_count - self.child_count

    def get_reorder_dwarf_options(self):
        options = []
        for dwarf in self.remaining_dwarves:
            if dwarf.weapon_level == 0:
                options.append(f"Dwarf {dwarf.ID}: {DT.Unarmed}")
            else:
                options.append(f"Dwarf {dwarf.ID}: {DT.Weapon_Level} {dwarf.weapon_level}")
        return options

    def reorder_dwarf(self, action):
        #when reordering dwarf one is choosing a dwarf that would be played later than the current dwarf
        dwarf_id = int(action[6])
        replacement_index = [x.ID for x in self.dwarves].index(dwarf_id)
        chosen_dwarf = self.dwarves[replacement_index]
        current_index = self.active_dwarf_index
        temp = []
        for index, dwarf in enumerate(self.dwarves):
            if index == current_index:
                temp.append(chosen_dwarf)
            elif dwarf.ID == dwarf_id:
                continue
            temp.append(dwarf)
        self.dwarves = temp

    @property
    def active_dwarf_weapon_level(self):
        return self.dwarves[self.active_dwarf_index].weapon_level





