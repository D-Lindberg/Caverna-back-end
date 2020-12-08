""" 
    contains dictionary object represenations of action spaces.
    """
from constants import ACTION_SPACE_TYPES as AST, CAVERNA_ACTIONS as CA, ACTION_GROUP_TYPES as AGT


Drift_Mining_A = {
    'id': 1,
    'name': AST.Drift_Mining_A,
    'stone_initial': 1,
    'stone_accumulating': 1,
    'action_group': ([CA.Collect_Resources, CA.Add_Tunnel_Cave_Dual_Tile], AGT.Optional)
}

Drift_Mining_B = {
    'id': 1,
    'name': AST.Drift_Mining_A,
    'stone_initial': 2,
    'stone_accumulating': 2,
    'action_group': ([CA.Collect_Resources, CA.Add_Tunnel_Cave_Dual_Tile], AGT.Optional),
}

Excavation_A = {
    'id': 1,
    'name': AST.Excavation_A,
    'stone_initial': 1,
    'stone_accumulating': 1,
    'action_group': ([CA.Collect_Resources, ([CA.Add_Tunnel_Cave_Dual_Tile, AGT.CA.Add_Cave_Cave_Dual_Tile], AGT.Exclusive)], AGT.Optional),
}

Excavation_B = {
    'id': 1,
    'name': AST.Excavation_B,
    'stone_initial': 2,
    'stone_accumulating': 1,
    'action_group': ([CA.Collect_Resources, ([CA.Add_Tunnel_Cave_Dual_Tile, AGT.CA.Add_Cave_Cave_Dual_Tile], AGT.Exclusive)], AGT.Optional),
}

Starting_Player_A = {
    'id': 1,
    'name': AST.Starting_Player_A,
    'food_initial' : 1,
    'food_accumulating' : 1,
    'ore_static' : 2,
    'action_group': (CA.Collect_Resources)
}

Starting_Player_B = {
    'id': 1,
    'name': AST.Starting_Player_B,
    'food_initial' : 1,
    'food_accumulating' : 1,
    'ruby_static' : 1,
    'action_group': (CA.Collect_Resources)
}