""" 
    contains dictionary object represenations of action spaces.
    """
from constants import ACTION_SPACE_TYPES as AST, CAVERNA_ACTIONS as CA, ACTION_GROUP_TYPES as AGT


Adventure = {
    'name' : AST.Adventure,
    'action_group' :([CA.Blacksmithing, ([CA.Expedition_Level_1, CA.Expedition_Level_1],AGT.Ordered)], AGT.Ordered_Optional)
}

Blacksmithing = {
    'name' : AST.Blacksmithing,
    'action_group' : ([CA.Blacksmithing, CA.Expedition_Level_3], AGT.Ordered_Optional)
}

Clearing_A = {
    'name' : AST.Clearing_A,
    'wood_initial' : 1,
    'wood_accumulating' : 1,
    'action_group' : ([CA.Collect_Resources, CA.Add_Field_Meadow_Tile], AGT.Optional)
}

Clearing_B = {
    'name' : AST.Clearing_B,
    'wood_initial' : 2,
    'wood_accumulating' : 2,
    'action_group' : ([CA.Collect_Resources, CA.Add_Field_Meadow_Tile], AGT.Optional)
}

Depot = {
    'name' : AST.Depot,
    'wood_initial' : 1,
    'wood_accumulating' : 1,
    'ore_initial' : 1,
    'ore_accumulating' : 1,
    'action_group' : (CA.Collect_Resources)
}

Donkey_Farming = {
    'name' : AST.Donkey_Farming,
    'donkey_initial' : 1,
    'donkey_accumulating' : 1,
    'action_group' : ([([CA.Pasture_Small, CA.Pasture_Large, CA.Buy_Stable], AGT.Optional), CA.Collect_Resources], AGT.Ordered_Optional)
}

Drift_Mining_A = {
    'name': AST.Drift_Mining_A,
    'stone_initial': 1,
    'stone_accumulating': 1,
    'action_group': ([CA.Collect_Resources, CA.Add_Tunnel_Cave_Dual_Tile], AGT.Optional)
}

Drift_Mining_B = {
    'name': AST.Drift_Mining_A,
    'stone_initial': 2,
    'stone_accumulating': 2,
    'action_group': ([CA.Collect_Resources, CA.Add_Tunnel_Cave_Dual_Tile], AGT.Optional),
}

Excavation_A = {
    'name': AST.Excavation_A,
    'stone_initial': 1,
    'stone_accumulating': 1,
    'action_group': ([CA.Collect_Resources, ([CA.Add_Tunnel_Cave_Dual_Tile, AGT.CA.Add_Cave_Cave_Dual_Tile], AGT.Exclusive)], AGT.Optional),
}

Excavation_B = {
    'name': AST.Excavation_B,
    'stone_initial': 2,
    'stone_accumulating': 1,
    'action_group': ([CA.Collect_Resources, ([CA.Add_Tunnel_Cave_Dual_Tile, AGT.CA.Add_Cave_Cave_Dual_Tile], AGT.Exclusive)], AGT.Optional),
}

Exploration = {
    'name' : AST.Exploration,
    'action_group' : (CA.Expedition_Level_4)
}

Extension = {
    'name' : AST.Extension,
    'action_group' : ([CA.Extension_A, CA.Extension_B], AGT.Exclusive)
}

Family_Life = {
    'name' : AST.Family_Life,
    'action_group' : ([CA.Family_Growth, CA.Sow_Bake], AGT.Optional)
}

Fence_Building_A = {
    'name' : AST.Fence_Building_A,
    'wood_initial' : 1,
    'wood_accumulating' : 1,
    'action_group' : ([CA.Collect_Resources, ([CA.Pasture_Small, CA.Pasture_Large], AGT.Optional)], AGT.Ordered_Optional)
}

Fence_Building_B = {
    'name' : AST.Fence_Building_B,
    'wood_initial' : 2,
    'wood_accumulating' : 1,
    'action_group' : ([CA.Collect_Resources, ([CA.Pasture_Small, CA.Pasture_Large], AGT.Optional)], AGT.Ordered_Optional)
}

Forest_Exploration_A = {
    'name' : AST.Forest_Exploration_A,
    'wood_initial' : 1,
    'wood_accumulating' : 1,
    'pumpkin_static' : 1,
    'action_group' : (CA.Collect_Resources)
}

Forest_Exploration_B = {
    'name' : AST.Forest_Exploration_B,
    'wood_initial' : 2,
    'wood_accumulating' : 1,
    'food_static' : 2,
    'action_group' : (CA.Collect_Resources)
}

Hardware_Rental_A = {
    'name' : AST.Hardware_Rental_A,
    'action_group' : ([CA.Expedition_Level_2, CA.Sow_Bake], AGT.Ordered_Optional)
}

Hardware_Rental_B = {
    'name' : AST.Hardware_Rental_B,
    'wood_static' : 2,
    'action_group' : ([CA.Collect_Resources, CA.Expedition_Level_2, CA.Sow_Bake], AGT.Ordered_Optional)
}

Housework = {
    'name' : AST.Housework,
    'dog_static' : 1,
    'action_group' : ([CA.Collect_Resources, CA.Furnish_Cavern], AGT.Optional)
}

Imitation_A = {
    'name' : AST.Imitation_A,
    'action_group' : (CA.Imitation_A)
}

Imitation_B = {
    'name' : AST.Imitation_B,
    'action_group' : (CA.Imitation_B)
}

Imitation_C = {
    'name' : AST.Imitation_C,
    'action_group' : (CA.Imitation_C)
}

Imitation_D = {
    'name' : AST.Imitation_D,
    'action_group' : (CA.Imitation_D)
}

Growth = {
    'name' : AST.Growth,
    'wood_static' : 1,
    'stone_static' : 1,
    'ore_static' : 1,
    'food_static': 1,
    'gold_static' : 2,
    'action_group' : ([CA.Collect_Resources, CA.Family_Growth], AGT.Exclusive)
}

Large_Depot = {
    'name' : AST.Large_Depot,
    'ore_static' : 1,
    'stone_static' : 1,
    'wood_initial' : 2,
    'wood_accumulating' : 1,
    'action_group' : (CA.Collect_Resources)
}

Logging_A = {
    'name' : AST.Logging_A,
    'wood_initial' : 3,
    'wood_accumulating' : 1,
    'action_group' : ([CA.Collect_Resources, CA.Expedition_Level_1], AGT.Ordered_Optional)
}

Logging_B = {
    'name' : AST.Logging_B,
    'wood_initial' : 3,
    'wood_accumulating' : 3,
    'action_group' : ([CA.Collect_Resources, CA.Expedition_Level_1], AGT.Ordered_Optional)
}

Ore_Delivery = {
    'name' : AST.Ore_Delivery,
    'ore_bonus_for_mines' : 2,
    'ore_initial' : 1,
    'ore_accumulating' : 1,
    'stone_initial' : 1,
    'stone_accumulating' : 1,
    'action_group' : (CA.Collect_Resources, CA)
}

Ore_Mine_Construction = {
    'name' : AST.Ore_Mine_Construction,
    'action_group' : ([CA.Add_Ore_Mine_Deep_Tunnel_Dual_Tile, CA.Expedition_Level_2], AGT.Ordered_Optional)
}

Ore_Mining_A = {
    'name' : AST.Ore_Mining_A,
    'ore_initial' : 2,
    'ore_accumulating' : 1,
    'ore_bonus_for_mines' : 2,
    'action_group' : (CA.Collect_Resources)
}

Ore_Mining_B = {
    'name' : AST.Ore_Mining_B,
    'ore_initial' : 3,
    'ore_accumulating' : 2,
    'ore_bonus_for_mines' : 2,
    'action_group' : (CA.Collect_Resources)
}

Ore_Trading = {
    'name' : AST.Ore_Trading,
    'action_group' : ([CA.Trade_2_Ore, CA.Trade_2_Ore, CA.Trade_2_Ore], AGT.Optional)
}

Ruby_Delivery = {
    'name' : AST.Ruby_Delivery,
    'ruby_initial' : 2,
    'ruby_accumulating' : 1,
    'mines_needed_for_ruby_bonus' : 1,
    'action_group' : (CA.Collect_Resources)
}

Ruby_Mine_Construction = {
    'name' : AST.Ruby_Mine_Construction,
    'action_group' : (CA.Add_Ruby_Mine_Tile)
}

Ruby_Mining_A = {
    'name' : AST.Ruby_Mining_A,
    'ruby_initial' : 1,
    'ruby_accumulating' : 1,
    'mines_needed_for_ruby_bonus' : 1,
    'action_group' : (CA.Collect_Resources)
}

Ruby_Mining_B = {
    'name' : AST.Ruby_Mining_B,
    'ruby_initial' : 1,
    'ruby_accumulating' : 1,
    'mines_needed_for_ruby_bonus' : 1,
    'start_on_round' : 3,
    'action_group' : (CA.Collect_Resources)
}

Sheep_Farming = {
    'name' : AST.Sheep_Farming,
    'sheep_initial' : 1,
    'sheep_accumulating' : 1,
    'action_group' : ([([CA.Pasture_Small, CA.Pasture_Large, CA.Buy_Stable], AGT.Optional), CA.Collect_Resources], AGT.Ordered_Optional)
}

Slash_And_Burn = {
    'name' : AST.Slash_And_Burn,
    'action_group' : ([CA.Add_Field_Meadow_Tile, CA.Sow_Bake], AGT.Ordered_Optional)
}

Small_Scale_Drift_mining = {
    'name' : AST.Small_Scale_Drift_mining,
    'stone_static' : 1,
    'action_group' : ([CA.Collect_Resources, CA.Add_Tunnel_Cave_Dual_Tile], AGT.Optional)
}

Starting_Player_A = {
    'name': AST.Starting_Player_A,
    'food_initial' : 1,
    'food_accumulating' : 1,
    'ore_static' : 2,
    'action_group': (CA.Collect_Resources)
}

Starting_Player_B = {
    'name': AST.Starting_Player_B,
    'food_initial' : 1,
    'food_accumulating' : 1,
    'ruby_static' : 1,
    'action_group': (CA.Collect_Resources)
}

Strip_Mining = {
    'name': AST.Strip_Mining,
    'wood_static' : 2,
    'ore_static' : 1,
    'stone_initial' : 0,
    'stone_accumulating' : 1,
    'action_group': (CA.Collect_Resources)
}

Supplies = {
    'name': AST.Supplies,
    'wood_static' : 1,
    'stone_static' : 1,
    'ore_static' : 1,
    'food_static' : 1,
    'gold_static' : 2,
    'action_group' : (CA.Collect_Resources)
}

Sustenance_A = {
    'name': AST.Sustenance_A,
    'wheat_static' : 1,
    'food_initial' : 1,
    'food_accumulating' : 1,
    'action_group' : ([CA.Collect_Resources, CA.Add_Field_Meadow_Tile], AGT.Optional)
}

Sustenance_B = {
    'name': AST.Sustenance_B,
    'wheat_static' : 1,
    'pumpkin_initial' : 0,
    'pumpkin_accumulating' : 1,
    'action_group' : ([CA.Collect_Resources, CA.Add_Field_Meadow_Tile], AGT.Optional)
}

Urgent_Wish_For_Children = {
    'name' : AST.Urgent_Wish_For_Children,
    'gold_static' : 3,
    'action_group' : ([CA.Furnish_Dwelling_Then_Grow, CA.Collect_Resources], AGT.Exclusive)
}

Weekly_Market = {
    'name' : AST.Weekly_Market,
    'gold_static' : 4,
    'action_group' : ([CA.Collect_Resources, ([CA.Gold_Cow, CA.Gold_Dog, CA.Gold_Donkey, CA.Gold_Ore, CA.Gold_Pig, CA.Gold_Pumpkin, CA.Gold_Sheep, CA.Gold_Stone, CA.Gold_Wheat, CA.Gold_Wood], AGT.Optional)], AGT.Ordered_Optional)
}

Wish_For_Children = {
    'name' : AST.Wish_For_Children,
    'action_group' : ([CA.Family_Growth, CA.Furnish_Dwelling], AGT.Exclusive)
}

Skip_Round = {
    'name' : AST.Skip_Round
}