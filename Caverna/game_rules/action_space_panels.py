from attrdict import AttrDict
from constants import ACTION_SPACE_TYPES as AST
'''
panel_name :[
    [col_A items], 
    [Col_B items], 
    [Col_C items]],
'''
PANELS = AttrDict({
    'All': [
        ['Round_04', 'Round_05', 'Round_06'],
        ['Round_07', 'Round_08', 'Round_09'],
        ['Round_10', 'Round_11', 'Round_12']], 
    'Not_Equals_2': [
        [AST.Ruby_Mining_A, AST.Housework, AST.Slash_And_Burn],
        ['Round_01', 'Round_02', 'Round_03']],
    'Equals_2' : [
        [AST.Ruby_Mining_B, AST.Housework, AST.Slash_And_Burn],
        ['Round_01', 'Round_02', 'Round_03']],
    'Not_More_Than_3' : [
        [AST.Drift_Mining_A, AST.Logging_A, AST.Wood_Gathering],
        [AST.Excavation_A, AST.Supplies, AST.Clearing_A],
        [AST.Starting_Player_A, AST.Ore_Mining_A, AST.Sustenance_A]],
    'Equals_3' : [
        [AST.Strip_Mining, AST.Imitation_A, AST.Forest_Exploration_A]],
    'More_Than_3' : [
        [AST.Drift_Mining_B, AST.Imitation_B, AST.Logging_B, AST.Forest_Exploration_B],
        [AST.Excavation_B, AST.Growth, AST.Clearing_B],
        [AST.Starting_Player_B, AST.Ore_Mining_B, AST.Sustenance_B]],
    'Equals_5': [
        [AST.Depot, AST.Weekly_Market, AST.Hardware_Rental_A],
        [AST.Small_Scale_Drift_mining, AST.Imitation_A, AST.Fence_Building_A]],
    'More_Than_5': [
        [AST.Depot, AST.Weekly_Market, AST.Hardware_Rental_B],
        [AST.Drift_Mining_A, AST.Imitation_C, AST.Fence_Building_B]],
    'Equals_7': [
        [AST.Large_Depot, AST.Imitation_D, AST.Extension]]
})