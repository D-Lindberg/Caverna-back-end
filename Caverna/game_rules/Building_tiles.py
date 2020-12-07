from constants import BUILDING_TYPES as BT

class Building_Tile:
    def __init__(self, building_name):
        details = self.get_characteristics(building_name)
        self.building_group = details.get('group')
        self.building_type = details.get('name')
        self.cost_food = details.get('food', 0)
        self.cost_gold = details.get('gold', 0)
        self.cost_ore = details.get('ore', 0)
        self.cost_pumpkin = details.get('pumpkin', 0)
        self.cost_stone = details.get('stone', 0)
        self.cost_wheat = details.get('wheat', 0)
        self.cost_wood = details.get('wood', 0)
        self.has_actions = details.get('action', False)
        self.is_introductory = details.get('introductory', True)
        self.is_unlimited = details.get('unlimited', False)
        self.victory_points = details.get('victory', 0)

    def get_characteristics(self, builing_name):
        if builing_name == BT.Dwelling:
            return dict(name = builing_name, group = "Dwelling", victory = 3, wood = 4, stone = 3, unlimited = True)
        if builing_name == BT.Simple_Dwelling1:
            return dict(name = builing_name, group = "Dwelling", wood = 4, stone = 2)
        if builing_name == BT.Simple_Dwelling2:
            return dict(name = builing_name, group = "Dwelling", wood = 3, stone = 3)
        if builing_name == BT.Mixed_Dwelling:
            return dict(name = builing_name, group = "Dwelling", victory = 4, wood = 5, stone = 4, introductory = False)
        if builing_name == BT.Couple_Dwelling:
            return dict(name = builing_name, group = "Dwelling", victory = 5, wood = 8, stone = 6, introductory = False)
        if builing_name == BT.Additional_Dwelling:
            return dict(name = builing_name, group = "Dwelling", victory = 5, wood = 4, stone = 3, introductory = False)
        if builing_name == BT.Cuddle_Room:
            return dict(name = builing_name, group = "Working", victory = 2, wood = 1)
        if builing_name == BT.Breakfast_Room:
            return dict(name = builing_name, group = "Working", wood = 1)
        if builing_name == BT.Stubble_Room:
            return dict(name = builing_name, group = "Working", victory = 1, wood = 1, ore = 1)
        if builing_name == BT.Work_Room:
            return dict(name = builing_name, group = "Working", victory = 2, stone = 1, introductory = False)
        if builing_name == BT.Guest_Room:
            return dict(name = builing_name, group = "Working", wood = 1, stone = 1, introductory = False)
        if builing_name == BT.Office_Room:
            return dict(name = builing_name, group = "Working", stone = 1, introductory = False)
        if builing_name == BT.Carpenter:
            return dict(name = builing_name, group = "Working", stone = 1)
        if builing_name == BT.Stone_Carver:
            return dict(name = builing_name, group = "Working", victory = 1, wood = 1)
        if builing_name == BT.Blacksmith:
            return dict(name = builing_name, group = "Working", victory = 3, wood = 1, stone = 2)
        if builing_name == BT.Miner:
            return dict(name = builing_name, group = "Working", victory = 3, wood = 1, stone = 1, introductory = False)
        if builing_name == BT.Builder:
            return dict(name = builing_name, group = "Working", victory = 2, stone = 1, introductory = False)
        if builing_name == BT.Trader:
            return dict(name = builing_name, group = "Working", victory = 2, wood = 1, action = True, introductory = False)
        if builing_name == BT.Wood_Supplier:
            return dict(name = builing_name, group = "Working", victory = 2, stone = 1)
        if builing_name == BT.Stone_Supplier:
            return dict(name = builing_name, group = "Working", victory = 1, wood = 1)
        if builing_name == BT.Ruby_Supplier:
            return dict(name = builing_name, group = "Working", victory = 2, wood = 2, stone = 2)
        if builing_name == BT.Dog_School:
            return dict(name = builing_name, group = "Working", introductory = False)
        if builing_name == BT.Quarry:
            return dict(name = builing_name, group = "Working", victory = 2, wood = 1, introductory = False)
        if builing_name == BT.Seam:
            return dict(name = builing_name, group = "Working", victory = 1, wood = 2, introductory = False)
        if builing_name == BT.Slaughtering_Cave:
            return dict(name = builing_name, group = "Working", victory = 2, wood = 2, stone = 2)
        if builing_name == BT.Cooking_Cave:
            return dict(name = builing_name, group = "Working", victory = 2, stone = 2, action = True)
        if builing_name == BT.Working_Cave:
            return dict(name = builing_name, group = "Working", victory = 2, wood = 1, stone = 1)
        if builing_name == BT.Mining_Cave:
            return dict(name = builing_name, group = "Working", victory = 2, wood = 3, stone = 2, introductory = False)
        if builing_name == BT.Breeding_Cave:
            return dict(name = builing_name, group = "Working", victory = 2, wheat = 1, stone = 1, introductory = False)
        if builing_name == BT.Peaceful_Cave:
            return dict(name = builing_name, group = "Working", victory = 2, wood = 2, stone = 2, action = True, introductory = False)
        if builing_name == BT.Weaving_Parlor:
            return dict(name = builing_name, group = "Scoring", wood = 2, stone = 2)
        if builing_name == BT.Milking_Parlor:
            return dict(name = builing_name, group = "Scoring", wood = 4, stone = 3)
        if builing_name == BT.State_Parlor:
            return dict(name = builing_name, group = "Scoring", gold = 5, stone = 3, introductory = False)
        if builing_name == BT.Hunting_Parlor:
            return dict(name = builing_name, group = "Scoring", victory = 1, wood = 2, action = True)
        if builing_name == BT.Beer_Parlor:
            return dict(name = builing_name, group = "Scoring", victory = 3, wood = 2, stone = 3, action = True)
        if builing_name == BT.Blacksmithing_Parlor:
            return dict(name = builing_name, group = "Scoring", victory = 2, ore = 3, action = True, introductory = False)
        if builing_name == BT.Stone_Storage:
            return dict(name = builing_name, group = "Scoring", wood = 3, ore = 1)
        if builing_name == BT.Ore_Storage:
            return dict(name = builing_name, group = "Scoring", wood = 1, stone = 2)
        if builing_name == BT.Spare_Part_Storage:
            return dict(name = builing_name, group = "Scoring", wood = 2, action = True, introductory = False)
        if builing_name == BT.Main_Storage:
            return dict(name = builing_name, group = "Scoring", wood = 2, stone = 1)
        if builing_name == BT.Weapon_Storage:
            return dict(name = builing_name, group = "Scoring", wood = 3, stone = 2)
        if builing_name == BT.Supplies_Storage:
            return dict(name = builing_name, group = "Scoring", wood = 3, food = 3, introductory = False)
        if builing_name == BT.Broom_Chamber:
            return dict(name = builing_name, group = "Scoring", wood = 1, introductory = False)
        if builing_name == BT.Treasure_Chamber:
            return dict(name = builing_name, group = "Scoring", wood = 1, stone = 1)
        if builing_name == BT.Food_Chamber:
            return dict(name = builing_name, group = "Scoring", wood = 2, pumpkin = 2)
        if builing_name == BT.Prayer_Chamber:
            return dict(name = builing_name, group = "Scoring", wood = 2, introductory = False)
        if builing_name == BT.Writing_Chamber:
            return dict(name = builing_name, group = "Scoring", stone = 2)
        if builing_name == BT.Fodder_Chamber:
            return dict(name = builing_name, group = "Scoring", wheat = 2, stone = 1)
        

