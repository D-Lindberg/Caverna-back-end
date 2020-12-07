from attrdict import AttrDict




#refence rule appendix page A1 under "The Expedition Loot Items"
EXPEDITION_REWARDS = AttrDict({
    'All_Weapons_PlusOne' : "All Weapons +1",
    'Breed_Animals' : "Breed up 2 types of farm animals",
    'Clearing' : "1 Pasture",
    'Cow' : "1 Cow",
    'Dog' : "1 Dog",
    'Donkey' : "1 Donkey",
    'Dwelling' : "Build a Dwelling for 2 wood & 2 stone",
    'Field' : "1 Field",
    'Furnish_Cavern' : "Furnish 1 Cavern",
    'Gold' : "2 Gold",
    'Large_Pasture' : "Fence a double pasture for 2 wood",
    'Large_Pasture_Discount' : "Fence a double pasture for 1 wood",
    'Nothing' : "Take Nothing",
    'Ore' : "2 Ore",
    'Pig' : "1 Pig",
    'Pumpkin' : "1 Pumpkin",
    'Sheep' : "1 Sheep",
    'Small_Pasture' : "Fence a single pasture for 1 wood",
    'Small_Pasture_Discount' : "Fence a single pasture for 0 wood",
    'Sow' : "Sow up to 2 Wheat and up to 2 Pumkins",
    'Stable' : "1 Stable (free)",
    'Stone' : "1 Stone",
    'Tunnel' : "1 Tunnel",
    'Wheat' : "1 Wheat",
    'Wood' : "1 Wood"
})

#refence rule book appendix A2 under "Weapon Strength 14"
#list all permutations of breeding up to 2 animals from the 4
EXPEDITION_BREEDING_OPTIONS = AttrDict({
    'Sheep_Only' : "Sheep only",
    'Donkeys_Only' : "Donkeys only",
    'Pigs_Only' : "Pigs only",
    'Cows_Only' : "Cows only",
    'Sheep_And_Donkeys' : "Sheep and Donnkeys",
    'Sheep_And_Pigs' : "Sheep and Pigs",
    'Sheep_And_Cows' : "Sheep and Cows",
    'Donkeys_And_Pigs' : "Donkeys and Pigs",
    'Donkeys_And_Cows' : "Donkeys and Cows",
    'Pigs_And_Cows' : "Pigs and Cows",
})

#refence rule appendix page A4 under "Block of 12 #2"
ROUND_BONUS_TYPES = AttrDict({
    'Donkey_Ore' : "donkey ore",
    'Ruby' : "ruby",
    'Stone' : "stone",
    'Wood' : "wood"
})


#refence rule book page 17 under "Rubies"
DWARF_TEXT = AttrDict({
    'Unarmed' : "Unarmed Dwarf",
    'Weapon_Level' : "Dwarf with Weapon Level"
})

#refence rule book pages 9 and 10 under "Harvest Time" and "Which Rounds End With a Harvest"
HARVEST_TYPES = AttrDict({
    'Full_Harvest' : "Full harvest",
    'No_Harvest' : "No harvest",
    'Single_Food_Per_Dwarf' : "Single food per dwarf",
    'Skip_Fields_Or_Animals' : "Skip fields or animals",
    'Special' : "Special",
    'Unknown' : "Unknown"
})

#refence rule book page 10 under "Which Rounds End With a Harvest"
HARVEST_OPTIONS = AttrDict({
    'Skip_Breeding_Phase' : "Skip breeding phase",
    'Skip_Field_Phase' : "Skip field phase"
})

#refence rule book page 11 under "Food Conversion Rules"
FOOD_ACTIONS = AttrDict({
    'Cancel' : "Cancel food conversion",
    'Convert_Cow' : "Convert 1 cow to 3 food",
    'Convert_Donkey' : "Convert 1 donkey to 1 food",
    'Convert_Donkey_Pair' : "Convert 2 donkeys to 3 food",
    'Convert_Gold_2' : "Convert 2 gold to 1 food",
    'Convert_Gold_3' : "Convert 3 gold to 2 food",
    'Convert_Gold_4' : "Convert 4 gold to 3 food",
    'Convert_Pig' : "Convert 1 pig to 2 food",
    'Convert_Pumpkin' : "Convert 1 pumpkin to 2 food",
    'Convert_Ruby' : "Convert 1 ruby to 2 food",
    'Convert_Sheep' : "Convert 1 sheep to 1 food",
    'Convert_Wheat' : "Convert 1 wheat to 1 food",
    'Feed_All_Dwarves' : "Feed All Dwarves",
    'Feed_And_Take_Begging_Cards' : "Partially feed dwarves and take begging cards",
    'Slaughtering_Cave_Convert_Cow' : "Convert 1 cow to 4 food",
    'Slaughtering_Cave_Convert_Donkey' : "Convert 1 donkey to 2 food",
    'Slaughtering_Cave_Convert_DonkeyPair' : "Convert 2 donkeys to 5 food",
    'Slaughtering_Cave_Convert_Pig' : "Convert 1 pig to 3 food",
    'Slaughtering_Cave_Convert_Sheep' : "Convert 1 sheep to 2 food"
})

#refence rule book page 10 under "The Breeding Phase"
#these actions will be provided to player as choices depending on how many types of animals can not be assigned to a location.
DISCARD_ACTIONS = AttrDict({
    'Discard_All_Unassigned_Animals' : "Discard all unassigned animals",
    'Discard_Cow' : "Discard 1 cow",
    'Discard_Donkey' : "Discard 1 donkey",
    'Discard_Pig' : "Discard 1 pig",
    'Discard_Sheep' : "Discard 1 sheep"
})

#refence rule book page 17 under "Rubies"
RUBY_TRADES = AttrDict({
    'Cancel' : "Cancel ruby conversion",
    'Cavern' : "Trade 2 Rubies for 1 Cavern",
    'Clearing' : "Trade 1 Ruby for 1 Pasture",
    'Cow' : "Trade 1 Ruby and 1 Food for 1 Cow",
    'Donkey' : "Trade 1 Ruby for 1 Donkey",
    'Field' : "Trade 1 Ruby for 1 Field",
    'Ore' : "Trade 1 Ruby for 1 Ore",
    'Pig' : "Trade 1 Ruby for 1 Pig",
    'Pumpkin' : "Trade 1 Ruby for 1 Veg",
    'Reorder_Dwarf' : "Pay 1 Ruby to re-order a dwarf",
    'Sheep' : "Trade 1 Ruby for 1 Sheep",
    'Stone' : "Trade 1 Ruby for 1 Stone",
    'Tunnel' : "Trade 1 Ruby for 1 Tunnel",
    'Wheat' : "Trade 1 Ruby for 1 Grain",
    'Wood' : "Trade 1 Ruby for 1 Wood"
})


#refence rule appendix pages A3 through A5
#added "Unavailable" to represent builings already taken from inventory
BUILDING_TYPES = AttrDict({
    'Additional_Dwelling' : "additional dwelling",
    'Beer_Parlor' : "beer parlor",
    'Blacksmith' : "blacksmith",
    'Blacksmithing_Parlor' : "blacksmithing parlor",
    'Breakfast_Room' : "breakfast room",
    'Breeding_Cave' : "breeding cave",
    'Broom_Chamber' : "broom chamber",
    'Builder' : "builder",
    'Carpenter' : "carpenter",
    'Cooking_Cave' : "cooking cave",
    'Couple_Dwelling' : "couple dwelling",
    'Cuddle_Room' : "cuddle room",
    'Dog_School' : "dog school",
    'Dwelling' : "dwelling",
    'Fodder_Chamber' : "fodder chamber",
    'Food_Chamber' : "food chamber",
    'Guest_Room' : "guest room",
    'Hunting_Parlor' : "hunting parlor",
    'Office_Room' : "office room",
    'Main_Storage' : "main storage",
    'Milking_Parlor' : "milking parlor",
    'Miner' : "miner",
    'Mining_Cave' : "mining cave",
    'Mixed_Dwelling' : "mixed dwelling",
    'Ore_Storage' : "ore storage",
    'Peaceful_Cave' : "peaceful cave",
    'Prayer_Chamber' : "prayer chamber",
    'Quarry' : "quarry",
    'Ruby_Supplier' : "ruby supplier",
    'Seam' : "seam",
    'Simple_Dwelling1' : "simple dwelling1",
    'Simple_Dwelling2' : "simple dwelling2",
    'Slaughtering_Cave' : "slaughtering cave",
    'Spare_Part_Storage' : "spare part storage",
    'State_Parlor' : "state parlor",
    'Stone_Carver' : "stone carver",
    'Stone_Storage' : "stone storage",
    'Stone_Supplier' : "stone supplier",
    'Stubble_Room' : "stubble room",
    'Supplies_Storage' : "supplies storage",
    'Trader' : "trader",
    'Treasure_Chamber' : "treasure chamber",
    'Unavailable' : "unavailable",
    'Weapon_Storage' : "weapon storage",
    'Weaving_Parlor' : "weaving parlor",
    'Working_Cave' : "working cave",
    'Work_Room' : "work room",
    'Wood_Supplier' : "wood supplier",
    'Writing_Chamber' : "writing chamber"
})

#refence rule appendix pages A4 and A5
BUILDING_TILE_ACTIONS = AttrDict({
    'Beer_Parlor_1' : "Trade 2 Grain for 3 Gold",
    'Beer_Parlor_2' : "Trade 2 Grain for 4 Food",
    'Blacksmithing_Parlor' : "1 Ore and 1 Ruby for 2 Gold and 1 Food",
    'Cancel' : "Cancel building use",
    'Cooking_Cave' : "Trade 1 Veg and 1 Grain for 5 Food",
    'Invalid' : "ERROR: Invalid tile action",
    'Hunting_Parlor' : "Trade 2 Pigs for 2 Gold and 2 Food",
    'Spare_Parts_Storage' : "Trade 1 Wood, 1 Stone, and 1 Ore for 2 Gold",
    'Trader' : "Trade 2 Gold for 1 Wood, 1 Stone, and 1 Ore",
})

#reference physical game boards and action cards
ACTION_SPACE_TYPES = AttrDict({
    'Adventure' : "adventure",
    'Blacksmithing' : "blacksmithing",
    'Clearing' : "clearing",
    #'Depot' : "depot",
    'Donkey_Farming' : "donkey darming",
    'Drift_Mining' : "drift mining",
    'Excavation' : "excavation",
    'Exploration' : "exploration",
    #'Extension' : "extension",
    'Family_Life' : "family life",
    #'Fence_Building' : "fence building",
    #'Forest_Exploration' : "forest exploration",
    #'Growth' : "growth",
    #'Hardware_Rental' : "hardware rental",
    'Housework' : "housework",
    #'Imitation' : "imitation",
    #'Large_Depot' : "large depot",
    'Logging' : "logging",
    'Ore_Delivery' : "ore delivery",
    'Ore_Mine_Construction' : "ore mine construction",
    'Ore_Mining' : "ore mining",
    'Ore_Trading' : "ore trading",
    'Ruby_Delivery' : "ruby deliver",
    'Ruby_Mine_Construction' : "ruby mine construction",
    'Ruby_Mining' : "ruby mining",
    'Sheep_Farming' : "sheep farming",
    'Skip_Round' : "skip round",
    'Slash_And_Burn' : "slash and burn",
    #'Small_Scale_Drift_mining' : "small scale drift mining",
    'Starting_Player' : "starting player",
    #'Strip_Mining' : "strip mining",
    'Supplies' : "supplies",
    'Sustenance' : "sustenance",
    'Urgent_Wish_For_Children' : "urgent wish for children",
    #'Weekly_Market' : "weekly market",
    'Wish_For_Children' : "wish for children",
    'Wood_Gathering' : "wood gathering"

})


#refence rule book page 1 under "Furnishing and landscape tiles"
#also includes components that make dual tiles such as "Deep tunnel" and "Ore_Mine" these tiles technically don't exist on their own, but
#are broken down to individual parts to use in placing them on the game board (1 tile-type per space in board).
#Finally fields that are in the process of growing food have a specific designation based on the type and quantity of food on that tile.
TILE_TYPES = AttrDict({
    'Cavern' : "Empty cavern",
    'Deep_Tunnel' : "Deep tunnel",
    'Field' : "Empty field",
    'Meadow' : "Empty meadow",
    'Ore_Mine' : "Ore mine",
    'Pasture_Large_Left' : "Big pasture left part",
    'Pasture_Large_Right' : "Big pasture right part ",
    'Pasture_Small' : "Small pasture",
    'Pumpkin_Field_1' : "Field with 1 pumpkin",
    'Pumpkin_Field_2' : "Field with 2 pumpkins",
    'Ruby_Mine' : "Ruby mine",
    'Stable' : "Stable",
    'Starting_Tile' : "Start position",
    'Tunnel' : "Empty tunnel",
    'Wheat_Field_1' : "Field with 1 wheat",
    'Wheat_Field_2' : "Field with 2 wheats",
    'Wheat_Field_3' : "Field with 3 wheats"
})

#refence rule book page 1 under "Furnishing and landscape tiles"
#excluding the "small pasture and field" tile as it physically exist to save on game pieces, but will never be placed in that position.
#it is a result of placing the "meadow and field" tile then upgrading the meadow at a later time.
DUAL_TILES = AttrDict({
    'Cavern_Cavern' : [TILE_TYPES.Cavern, TILE_TYPES.Cavern],
    'Cavern_Tunnel' : [TILE_TYPES.Cavern, TILE_TYPES.Tunnel],
    'Field_Meadow' : [TILE_TYPES.Field, TILE_TYPES.Meadow],
    'Ore_Mine_Deep_Tunnel' : [TILE_TYPES.Ore_Mine, TILE_TYPES.Deep_Tunnel],
    'Large_Pasture' : [TILE_TYPES.Pasture_Large_Left, TILE_TYPES.Pasture_Large_Right]
})

#refence rule book page 1 under "Wooden and acrylic playing pieces"
#everything except "starting player token", "stables", and "dwarf discs"
#begging, food, and gold from refence rule book page 1 under "On counter sheets"
RESOURCE_TYPES = AttrDict({
    'Begging' : "begging",
    'Cows' : "cows",
    'Dogs' : "dogs",
    'Donkeys' : "donkeys",
    'Food' : "food",
    'Gold' : "gold",
    'Ore' : "ore",
    'Pumpkin' : "pumpkin",
    'Pigs' : "pigs",
    'Ruby' : "ruby",
    'Sheep' : "sheep",
    'Score_Marker' : "score",
    'Stone' : "stone",
    'Wheat' : "wheat",
    'Wood' : "wood"
})

#actions that can be taken from an action-space or expedition
CAVERNA_ACTIONS = AttrDict({
    'Add_Cave_Cave_Dual_Tile' : "Add Cave/Cave dual tile",
    'Add_Field_Meadow_Tile' : "Add Field/Meadow dual tile",
    'Add_Ore_Mine_Deep_Tunnel_Dual_Tile' : "Add Ore Mine/Deep Tunnel dual tile",
    'Add_Ruby_Mine_Tile' : "Build a Ruby Mine",
    'Add_Tunnel_Cave_Dual_Tile' : "Add Tunnel/Cave dual tile",
    'Blacksmithing' : "Blacksmithing",
    'Buy_Stable' : "Buy a stable",
    'Cancel' : "Cancel",
    'Collect_Resources' : "Collect Resources",
    'Furnish_Dwelling' : "Furnish a Dwelling",
    'Expedition_Level_1' : "Level 1 Expedition",
    'Expedition_Level_2' : "Level 2 Expedition",
    'Expedition_Level_3' : "Level 3 Expedition",
    #'Expedition_Level_4' : "Level 4 Expedition",
    'Family_Growth' : "Family Growth",
    'Finish' : "Finish",
    'Furnish_Cavern' : "Furnish a Cavern",
    'Furnish_Dwelling_Then_Grow' : "Furnish a dwelling, then Family Growth",
    'Pasture_Large' : "Fence 2 adjacent fields",
    'Pasture_Small' : "Fence 1 field",
    'Sow_Bake' : "Sowing Fields",
    'Sow_1_Pumpkin' : "Sow 1 pumpkin",
    'Sow_1_Wheat' : "Sow 1 wheat",
    'Sow_1_Wheat_1_Pumpkin' : "Sow 1 wheat and 1 pumpkin",
    'Sow_1_Wheat_2_Pumpkin' : "Sow 1 wheat and 2 pumpkins",
    'Sow_2_Pumpkin' : "Sow 2 pumpkins",
    'Sow_2_Wheat' : "Sow 2 wheats",
    'Sow_2_Wheat_1_Pumpkin' : "Sow 2 wheats and 1 pumpkin",
    'Sow_2_Wheat_2_Pumpkin' : "Sow 2 wheats and 2 pumpkins",
    'Trade_2_Ore' : "Trade 2 Ore for 2 Gold and 1 Food",
    'Weapon_Level_8' : "Level 8 Weapon",
    'Weapon_Level_7' : "Level 7 Weapon",
    'Weapon_Level_6' : "Level 6 Weapon",
    'Weapon_Level_5' : "Level 5 Weapon",
    'Weapon_Level_4' : "Level 4 Weapon",
    'Weapon_Level_3' : "Level 3 Weapon",
    'Weapon_Level_2' : "Level 2 Weapon",
    'Weapon_Level_1' : "Level 1 Weapon"
})