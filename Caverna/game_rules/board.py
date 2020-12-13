from attrdict import AttrDict
from constants import (
    ANIMAL_TILE_TYPES,
    BUILDING_TYPES as BT,
    BUILDING_TILE_ACTIONS,
    BUILDINGS_WITH_ACTIONS,
    CAVE_TYPES,
    DUAL_TILES,
    FOREST_TYPES,
    TILE_TYPES as TT
)

'''
time to regroup.
the tile manager should receive game boards from database to load into current working query.

current working queries will be:

to see if a tile can be placed and reply with list of possible placements for a tile.

to place a tile. verify that it can be placed and then place or don't place depending on results of verification. 
finally return true or false of placement. 


answer if a player has a specific tile/building(mainly buildings) reply should only need to be true or false.


reply answer to whether a specific coordinate has been filled (will be used to apply bonuses)

given a specific coordinate reply with what type of tile or building is there or none

give the total count/occurrence of specific types of tile(s)/building(s) again for bonuses or actions.

dwarf capacity is determined by specific buildings. need to reply with that capacity. certain buildings present 
action options that can be used at various times. Tile manager needs to reply with a list of action options. export 
all locations that can have animals to the animal manager. return the total count of undiscovered spaces Should be 
able to export everything to be saved back in database 

'''


class Board:
    def __init__(self, **kwargs):
        self.WIDTH = 5
        self.HEIGHT = 6
        self.PLAY_AREA = self.play_area_coordinates()
        self.ALL_POSITIONS = self.all_coordinates()
        self.tiles_to_place = []
        self.arrange_animals_triggered = False
        self.board_type = kwargs.get('board_type')
        self.is_forest = self.board_type == 'forest'
        self.board = kwargs.get('board', self.generate_board())
        self.board_inverted = self.convert_board()
        if self.is_forest:
            self.update_large_pasture_locations()
            self.expandable_forest = kwargs.get('expandable_forest', False)
        else:
            self.tunnels_are_also_caverns = self.has_tile_named(BT.Work_Room)

    def activate_expandable_forest(self):
        if self.is_forest:
            self.expandable_forest = True

    def activate_tunnels_are_also_caverns(self):
        if not self.is_forest:
            self.tunnels_are_also_caverns = True

    def play_area_coordinates(self):
        result = []
        for x in range(1, self.WIDTH - 1):
            for y in range(1, self.HEIGHT - 1):
                result.append((x, y))
        return result

    def all_coordinates(self):
        results = []
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                results.append((x, y))
        return results

    def generate_board(self):
        d = {location: {'empty'} for location in self.ALL_POSITIONS}
        temp = set(self.ALL_POSITIONS) - set(self.PLAY_AREA)
        for location in temp:
            d[location].add('expanded_empty')
            d[location].discard('empty')
        if not self.is_forest:
            d[(1, 1)].add(TT.Starting_Tile)
            d[(1, 1)].discard('empty')
            d[(1, 2)].add(TT.Cavern)
            d[(1, 2)].discard('empty')
        return d

    def extract_board(self):
        d = {key: sorted(value) for key, value in self.board.items()}
        return d

    def convert_board(self):
        base_set = set(TT.values())
        if self.is_forest:
            base_set.intersection_update([x for x in FOREST_TYPES if type(x) == str])
            base_set.add('Large_Pasture')
        else:
            base_set.intersection_update([x for x in CAVE_TYPES if type(x) == str])
            [base_set.add(building) for building in BT.values()]
        base_set.add({'empty', 'expanded_empty', 'single', 'double', 'special'})
        d = AttrDict({tile: set() for tile in base_set})

        for (location, tile_types) in self.board.items():
            for tile_type in tile_types:
                d[tile_type].add(location)
                if tile_type != 'empty':
                    d.empty.discard(location)
                if tile_type != 'expanded_empty':
                    d.expanded_empty.discard(location)
        return d

    def update_large_pasture_locations(self):
        board = self.board_inverted
        left_part = TT.Pasture_Large_Left
        right_part = TT.Pasture_Large_Right
        left_locations = board[left_part].copy()
        right_locations = board[right_part].copy()
        while len(board.Large_Pasture) != len(board[left_part]):
            pasture_location = []
            for position in left_locations:
                adjacent_matches = []
                x, y = position
                if (x, y + 1) in right_locations:
                    adjacent_matches.append((x, y + 1))
                if (x + 1, y) in right_locations:
                    adjacent_matches.append((x + 1, y))
                if len(adjacent_matches) == 2:
                    continue
                pasture_location.append((position, adjacent_matches[0]))
                break
            board.Large_Pasture.add(pasture_location)
            left_locations.discard(pasture_location[0])
            right_locations.discard(pasture_location[1])

    def undiscovered_location_count(self):
        results = self.board_inverted.empty.copy()
        results.difference_update(self.board_inverted.Stable)
        return len(results)

    def tile_belongs(self, tile_name):
        # not to be used with empty and expanded_empty
        tile_is_forest = tile_name in FOREST_TYPES
        if self.is_forest and tile_is_forest:
            return True
        if self.is_forest or tile_is_forest:
            return False
        return True

    def tile_does_not_belong(self, tile_name):
        return not self.tile_belongs(tile_name)

    def animal_locations(self):
        lookup = self.board_inverted
        types = set(ANIMAL_TILE_TYPES)
        forest = set([x for x in FOREST_TYPES if type(x) == str])
        tile_types = types.intersection(forest) if self.is_forest else types.difference(forest)
        locations = set([lookup[tile] for tile in tile_types])
        return [(self.board_type, location, list(self.board[location])) for location in locations]

    def all_locations_of(self, tile_name):
        # do not use to lookup dual tiles
        belongs = self.tile_belongs(tile_name)
        return self.board_inverted[tile_name] if belongs else set()

    def tile_count(self, tile_name):
        # do not use to lookup dual tiles
        belongs = self.tile_belongs(tile_name)
        return len(self.board_inverted[tile_name]) if belongs else 0

    def tile_count_from_list(self, list_of_types):
        # list can not contain dual tiles
        return sum([self.tile_count(tile_name) for tile_name in list_of_types])

    def has_tile_named(self, tile_name):
        # do not use to lookup dual tiles
        return self.tile_count(tile_name) > 0

    def dwarf_capacity(self):
        if self.is_forest:
            return 0
        capacity = 2
        capacity += self.tile_count_from_list([
            BT.Dwelling,
            BT.Simple_Dwelling1,
            BT.Simple_Dwelling2
        ])
        capacity += 2 * self.tile_count(BT.Couple_Dwelling)
        if capacity > 5:
            capacity = 5
        capacity += self.tile_count(BT.Additional_Dwelling)
        return capacity

    def get_name_of_tile_at(self, position):
        if position not in self.ALL_POSITIONS:
            return []
        tile = self.board[position].copy()
        tile.discard('empty')
        tile.discard('expanded_empty')
        return sorted(tile)

    def all_non_empty_locations(self):
        board = self.board_inverted
        locations = set(self.ALL_POSITIONS).difference(board.empty, board.expanded_empty)
        return locations

    def locations_of_tiles_placed_excludes_stables(self):
        locations_with_tiles = self.all_non_empty_locations()
        if self.is_forest:
            for location in self.board_inverted.Stable:
                if len(self.board[location]) == 1:
                    locations_with_tiles.discard(location)
        return locations_with_tiles

    def was_non_stable_tile_placed_at(self, position):
        location = self.board[position]
        if len(location) == 2:
            return True
        if len(location) == 1 and TT.Stable not in location:
            return True
        return False

    def all_actions_from_buildings(self):
        if self.is_forest:
            return []
        actions = []
        for building in BUILDINGS_WITH_ACTIONS:
            if len(self.board_inverted[building]) > 0:
                actions.extend(BUILDING_TILE_ACTIONS[building])
        return actions

    def get_large_pastures(self):
        return sorted(self.board_inverted.Large_Pasture) if self.is_forest else []

    def update_available_spaces(self):
        self.update_single_spaces()
        self.update_double_spaces()
        self.update_special_spaces()

    def update_single_spaces(self):
        occupied = self.locations_of_tiles_placed_excludes_stables()
        singles = self.board_inverted.single
        singles.clear()
        for location in occupied:
            singles.update(self.empty_neighbors_of(location))
        if len(singles) == 0:
            singles.add((3, 1))

    def empty_neighbors_of(self, position):
        looking_for_second_part = self.board[position] == 'empty'
        neighbors = set()
        x, y = position
        for location in [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]:
            if location in self.board_inverted.empty:
                neighbors.add(location)
            if looking_for_second_part and self.expandable_forest:
                if location in self.board_inverted.expanded_empty:
                    neighbors.add(location)
        return neighbors

    def update_double_spaces(self):
        doubles = self.board_inverted.double
        doubles.clear()
        for location in self.board_inverted.single:
            adjacent_empties = self.empty_neighbors_of(location)
            for adjacent in adjacent_empties:
                doubles.add((location, adjacent))
                doubles.add((adjacent, location))

    def update_special_spaces(self):
        tile_type = TT.Meadow if self.is_forest else TT.Tunnel
        tile_type_locations = self.all_locations_of(tile_type)
        specials = self.board_inverted.special
        specials.clear()
        for location in tile_type_locations:
            adjacent_matches = self.matching_neighbors_for_special_spaces(location)
            for adjacent in adjacent_matches:
                specials.add((location, adjacent))
                specials.add((adjacent, location))

    def matching_neighbors_for_special_spaces(self, position):
        tile_type = TT.Meadow if self.is_forest else TT.Tunnel
        neighbors = set()
        neighborhood = self.board_inverted[tile_type]
        x, y = position
        for neighbor in [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]:
            if neighbor in neighborhood:
                neighbors.add(neighbor)
        return neighbors

    # building
    def can_building_be_placed(self):
        locations = self.all_locations_of(TT.Cavern).copy()
        if self.tunnels_are_also_caverns:
            locations.update(self.all_locations_of(TT.Tunnel))
            locations.update(self.all_locations_of(TT.Deep_Tunnel))
        if len(locations) > 0:
            return True, str(len(locations)), sorted(locations)
        return False, "No place to build on", []

    def place_building(self, building, location):
        available, msg, locations = self.can_building_be_placed()
        if not available:
            return available, msg, locations
        if location not in locations:
            return False, "Position given doesn't match try from here:", locations
        board = self.board
        lookup = self.board_inverted
        previous_type = board[location]
        board[location].clear()
        board[location].add(building)
        lookup[building].add(location)
        lookup[previous_type].discard(location)
        return True, "Success", location

    # tunnel or cavern
    def can_tunnel_or_cavern_be_placed(self):
        locations = sorted(self.board_inverted.single)
        if len(locations) > 0:
            return True, str(len(locations)), locations
        return False, "No empty spaces", []

    def place_tunnel_or_cavern(self, tile_type, location):
        available, msg, locations = self.can_tunnel_or_cavern_be_placed()
        if not available:
            return available, msg, locations
        if location not in locations:
            return False, "Position given doesn't match try from here:", locations
        board = self.board
        lookup = self.board_inverted
        previous_type = board[location]
        board[location].clear()
        board[location].add(tile_type)
        lookup[tile_type].add(location)
        lookup[previous_type].discard(location)
        return True, "Success", location

    # ruby-mine
    def can_ruby_mine_be_placed(self):
        locations = self.board_inverted[TT.Tunnel].copy()
        locations.update(self.board_inverted[TT.Deep_Tunnel])
        if len(locations) > 0:
            return True, str(len(locations)), sorted(locations)
        return False, "No tunnels to build on", []

    def place_ruby_mine(self, location):
        available, msg, locations = self.can_ruby_mine_be_placed()
        if not available:
            return available, msg, locations
        if locations not in locations:
            return False, "Position given doesn't match try from here", locations
        board = self.board
        lookup = self.board_inverted
        previous_type = board[location]
        board[location].clear()
        board[location].add(TT.Ruby_Mine)
        lookup[TT.Ruby_Mine].add(location)
        lookup[previous_type].discard(location)
        if previous_type == TT.Deep_Tunnel:
            return True, "Success and bonus achieved", location
        return True, "Success", location

    # meadow
    def can_meadow_be_placed(self):
        locations = sorted(self.board_inverted.single)
        if len(locations) > 0:
            return True, str(len(locations)), locations
        return False, "No empty spaces", []

    def place_meadow(self, location):
        available, msg, locations = self.can_meadow_be_placed()
        if not available:
            return available, msg, locations
        if location not in locations:
            return False, "Position given doesn't match try from here", locations
        board = self.board
        lookup = self.board_inverted
        board[location].discard('empty')
        board[location].add(TT.Ruby_Mine)
        lookup[TT.Ruby_Mine].add(location)
        lookup.empty.discard(location)
        return True, "Success", location

    # field
    def can_field_be_placed(self):
        locations = self.board_inverted.single.copy()
        locations.difference_update(self.board_inverted.Stable)
        if len(locations) > 0:
            return True, str(len(locations)), sorted(locations)
        return False, "No spaces available", []

    def place_field(self, location):
        available, msg, locations = self.can_field_be_placed()
        if not available:
            return available, msg, locations
        if location not in locations:
            return False, "Position given doesn't match try from here", locations
        board = self.board
        lookup = self.board_inverted
        board[location].discard('empty')
        board[location].add(TT.Field)
        lookup[TT.Field].add(location)
        lookup.empty.discard(location)
        return True, "Success", location

    # small-pasture
    def can_small_pasture_be_placed(self):
        locations = self.board_inverted[TT.Meadow].copy()
        if len(locations) > 0:
            return True, str(len(locations)), sorted(locations)
        return False, "No spaces available", []

    def place_small_pasture(self, location):
        available, msg, locations = self.can_small_pasture_be_placed()
        if not available:
            return available, msg, locations
        if location not in locations:
            return False, "Position given doesn't match try from here", locations
        board = self.board
        lookup = self.board_inverted
        board[location].discard(TT.Meadow)
        board[location].add(TT.Pasture_Small)
        lookup[TT.Pasture_Small].add(location)
        lookup.empty.discard(location)
        return True, "Success", location

    # ore-mine and deep-tunnel
    def can_ore_mine_and_deep_tunnel_be_placed(self):
        locations = self.board_inverted.special.copy()
        if len(locations) > 0:
            return True, str(len(locations)), sorted(locations)
        return False, "No spaces available", []

    def place_ore_mine_and_deep_tunnel(self, location):
        available, msg, locations = self.can_ore_mine_and_deep_tunnel_be_placed()
        if not available:
            return available, msg, locations
        if location not in locations:
            return False, "Given location doesn't match try from here", locations
        board = self.board
        lookup = self.board_inverted
        board[location[0]].discard(TT.Tunnel)
        board[location[1]].discard(TT.Tunnel)
        board[location[0]].add(TT.Deep_Tunnel)
        board[location[1]].add(TT.Ore_Mine)
        lookup[TT.Tunnel].difference_update(location)
        lookup[TT.Deep_Tunnel].add(location[0])
        lookup[TT.Ore_Mine].add(location[1])
        return True, "Success", location

    # large-pasture
    def can_large_pasture_be_placed(self):
        pass

    # cavern-cavern
    # cavern-tunnel
    # meadow-field
    # stable
    # number of fields available to sow

    def can_specific_tile_be_placed(self, tile_name):
        # can't place an empty tile
        if tile_name == 'empty' or tile_name == 'expanded_empty':
            return False
        is_building = tile_name in BT.values()
        dual_tile = tile_name in DUAL_TILES
        # 3 categories are building, dual_tile, and single tile all need to be on correct board
        if is_building:
            # buildings can't be placed on forest board
            if not self.is_forest:
                return False
        else:
            if dual_tile:
                if self.tile_does_not_belong(tile_name[0]):
                    return False
            else:
                if self.tile_does_not_belong(tile_name):
                    return False

        # at this point we have identified which category and verified that on the right board
        if is_building:
            available_spaces = self.tile_count(TT.Cavern)
            if self.tunnels_are_also_caverns:
                available_spaces += self.tile_count(TT.Tunnel)
                available_spaces += self.tile_count(TT.Deep_Tunnel)
            return available_spaces > 0

        if dual_tile:
            if tile_name == DUAL_TILES.Ore_Mine_Deep_Tunnel or tile_name == DUAL_TILES.Large_Pasture:
                return len(self.board_inverted.special) > 0
            else:
                return len(self.board_inverted.double) > 0
