from Caverna.game_rules.constants import TILE_TYPES
from attrdict import AttrDict
from constants import (
    ANIMAL_TILE_TYPES,
    BUILDING_TILE_ACTIONS,
    BUILDING_TYPES as BT,
    BUILDINGS_WITH_ACTIONS,
    CAVE_TYPES,
    DUAL_TILES as DT,
    FOREST_TYPES,
    HARVEST_SEQUENCE,
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
        self.PLAY_AREA = [(x,y) for x in range(1, 4) for y in range(1, 5)]
        self.ALL_POSITIONS = [(x,y) for x in range(5) for y in range(6)]
        self.board_type = kwargs.get('board_type')
        self.is_forest = self.board_type == 'forest'
        self.board = kwargs.get('board', self._generate_board())
        self.board_inverted = self._convert_board()
        if self.is_forest:
            self._update_large_pasture_locations()
            self.expandable_forest = kwargs.get('expandable_forest', False)
        else:
            self.tunnels_are_also_caverns = self.has_tile_named(BT.Work_Room)
        self._update_available_spaces()

    def activate_expandable_forest(self):
        if self.is_forest:
            self.expandable_forest = True

    def _generate_board(self):
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

    def _convert_board(self):
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

    def _update_large_pasture_locations(self):
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

    def unused_space_count(self):
        results = self.board_inverted.empty.copy()
        results.difference_update(self.board_inverted.Stable)
        return len(results)

    def _tile_belongs(self, tile_name):
        # not to be used with empty and expanded_empty
        tile_is_forest = tile_name in FOREST_TYPES
        if self.is_forest and tile_is_forest:
            return True
        if self.is_forest or tile_is_forest:
            return False
        return True

    def _tile_does_not_belong(self, tile_name):
        return not self._tile_belongs(tile_name)

    def extract_animal_locations(self):
        locations_of = self.board_inverted
        board = self.board_type
        animal_tiles = set(ANIMAL_TILE_TYPES)
        #forest animal_tiles may include lists, but only need strings
        forest_tiles = set([x for x in FOREST_TYPES if type(x) == str])
        if self.is_forest:
            animal_tiles.intersection_update(forest_tiles)
            animal_tiles.update('Large_Pasture')
        else:
            animal_tiles.difference_update(forest_tiles)
        return [(board, tile, sorted(locations_of[tile])) for tile in animal_tiles]

    def has_tile_named(self, tile_name):
        # do not use to lookup dual tiles
        count = self.board_inverted.get(tile_name, set())
        return len(count) > 0

    def dwarf_capacity(self):
        if self.is_forest:
            return 0
        board = self.board_inverted
        capacity = 2
        capacity += len(board[BT.Dwelling])
        capacity += len(board[BT.Simple_Dwelling1])
        capacity += len(board[BT.Simple_Dwelling2])
        capacity += 2 * len(board[BT.Couple_Dwelling])
        if capacity > 5:
            capacity = 5
        capacity += len(board[BT.Additional_Dwelling])
        return capacity

    def get_name_of_tile_at(self, position):
        if position not in self.ALL_POSITIONS:
            return []
        tile = self.board[position].copy()
        tile.discard('empty')
        tile.discard('expanded_empty')
        return sorted(tile)

    def _locations_claimed_by_tiles_other_than_stables(self):
        board = self.board_inverted
        locations = set(self.ALL_POSITIONS)
        locations.difference_update(board.empty, board.expanded_empty)
        return locations

    def bonus_position_was_reached_at(self, position):
        location = self.board[position]
        if len(location) == 2:
            return True
        if len(location) == 1 and TT.Stable not in location:
            return True
        return False

    def retrieve_actions_available_from_placed_buildings(self):
        if self.is_forest:
            return []
        actions = []
        for building in BUILDINGS_WITH_ACTIONS:
            if len(self.board_inverted[building]) > 0:
                actions.extend(BUILDING_TILE_ACTIONS[building])
        return actions

    def _empty_neighbors_of(self, position):
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

    def _matching_neighbors_for_special_spaces(self, position):
        tile_type = TT.Meadow if self.is_forest else TT.Tunnel
        neighbors = set()
        neighborhood = self.board_inverted[tile_type]
        x, y = position
        for neighbor in [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]:
            if neighbor in neighborhood:
                neighbors.add(neighbor)
        return neighbors

    def _update_available_spaces(self):
        self._update_single_spaces()
        self._update_double_spaces()
        self._update_special_spaces()

    def _update_single_spaces(self):
        occupied = self._locations_claimed_by_tiles_other_than_stables()
        singles = self.board_inverted.single
        singles.clear()
        for location in occupied:
            singles.update(self._empty_neighbors_of(location))
        if len(singles) == 0:
            singles.add((3, 1))

    def _update_double_spaces(self):
        doubles = self.board_inverted.double
        doubles.clear()
        for location in self.board_inverted.single:
            adjacent_empties = self._empty_neighbors_of(location)
            for adjacent in adjacent_empties:
                doubles.add((location, adjacent))
                doubles.add((adjacent, location))

    def _update_special_spaces(self):
        tile_type = TT.Meadow if self.is_forest else TT.Tunnel
        tile_type_locations = self.board_inverted[tile_type]
        specials = self.board_inverted.special
        specials.clear()
        for location in tile_type_locations:
            adjacent_matches = self._matching_neighbors_for_special_spaces(location)
            for adjacent in adjacent_matches:
                specials.add((location, adjacent))
                specials.add((adjacent, location))

    def _can_place_stable(self):
        if len(self.board_inverted.Stable) > 3:
            return False, "Already have 3 stables", []
        board = self.board_inverted
        locations = self._locations_claimed_by_tiles_other_than_stables()
        locations.update(board.empty)
        locations.difference_update(board.Stable, board[TT.Field])
        if len(locations) > 0:
            return True, str(len(locations)), sorted(locations)
        return False, "No spaces available", []

    def can_tile_be_placed(self, tile_type):
        if self._tile_does_not_belong(tile_type):
            return False, "Incorrect board", []
        if tile_type == TT.Stable:
            return self._can_place_stable()
        building_list = [BT.values()]
        doubles_list = [DT.Field_Meadow, DT.Cavern_Cavern, DT.Cavern_Tunnel]
        specials_list = [DT.Large_Pasture, DT.Ore_Mine_Deep_Tunnel]
        divide_by_2_list = [DT.Cavern_Cavern, DT.Large_Pasture]
        exclude_stables_list = [DT.Field_Meadow, TT.Field]
        single_list = [TT.Field, TT.Meadow, TT.Tunnel, TT.Cavern]
        building = tile_type in building_list
        double = tile_type in doubles_list
        special = tile_type in specials_list
        divide_by_2 = tile_type in divide_by_2_list
        exclude_stables = tile_type in exclude_stables_list
        single = tile_type in single_list
        board = self.board_inverted
        locations = set()
        if building:
            locations.update(board[TT.Cavern])
            if self.tunnels_are_also_caverns:
                locations.update(board[TT.Tunnel], board[TT.Deep_Tunnel])
        if double:
            locations.update(board.double)
            if exclude_stables:
                result = [(a, b) for (a, b) in locations if TT.Stable not in self.board[a] ]
                locations.intersection_update(result)
        if special:
            locations.update(board.special)
        if divide_by_2:
            result = [(a,b) for (a, b) in locations if a < b]
            locations.intersection_update(result)
        if single:
            locations.update(board.single)
            if exclude_stables:
                locations.difference_update(board.Stable)
        if tile_type == TT.Pasture_Small:
            locations.update(board[TT.Meadow])
        if tile_type == TT.Ruby_Mine:
            locations.update(board[TT.Tunnel], board[TT.Deep_Tunnel])
        if len(locations) > 0:
            return True, str(len(locations)), sorted(locations)
        return False, "No space available", []

    def _remove_tile_from_location(self, tile_type, position):
        self.board[position].discard(tile_type)
        self.board_inverted[tile_type].discard(position)

    def _place_single_tile(self, tile, location):
        empty_list = {TT.Tunnel, TT.Cavern, TT.Field, TT.Meadow}
        tunnel_list = {TT.Ruby_Mine, TT.Ore_Mine, TT.Deep_Tunnel}.union(BT.values())
        deep_tunnel_list = {TT.Ruby_Mine}.union(BT.values())
        meadow_list = {TT.Pasture_Small, TT.Pasture_Large_Left, TT.Pasture_Large_Right}
        cavern_list = {}.union(BT.values())
        if tile in empty_list:
            self._remove_tile_from_location('empty', location)
        if tile in tunnel_list:
            self._remove_tile_from_location(TT.Tunnel, location)
        if tile in deep_tunnel_list:
            self._remove_tile_from_location(TT.DeepTunnel, location)
        if tile in meadow_list:
            self._remove_tile_from_location(TT.Meadow, location)
        if tile in cavern_list:
            self._remove_tile_from_location(TT.Cavern, location)
        self.board[location].add(tile)
        self.board_inverted[tile].add(location)

    def place_tile(self,tile_type, location):
        # verification
        available, msg, locations = self.can_tile_be_placed(tile_type)
        if not available:
            return available, msg, locations
        if location not in locations:
            return False, "Position given doesn't match try from here", locations
        ruby_bonus = tile_type == TT.Ruby_Mine and TT.Deep_Tunnel in self.board[location]
        if tile_type in DT.values():
            self._place_single_tile(tile_type[0], location[0])
            self._place_single_tile(tile_type[1], location[1])
        else:
            self._place_single_tile(tile_type, location)
        self._update_available_spaces()
        if tile_type == BT.Work_Room:
            self.tunnels_are_also_caverns = True
            return True, "Success and Tunnels and Deep Tunnels can be furnished", location
        if tile_type == BT.Office_Room:
            return True, "Success and Remember to activate the expandable_forest", location
        if ruby_bonus:
            return True, "Success and Ruby Bonus", location
        return True, "Success", location

    def retrieve_number_of_empty_fields(self):
        return len(self.board_inverted.get(TT.Field, []))

    def sow_pumpkin(self):
        location = self.board_inverted[TT.Field].pop()
        self.board_inverted[TT.Pumpkin_Field_2].add(location)
        self.board[location].add(TT.Pumpkin_Field_2)
        self.board[location].discard(TT.Field)
    
    def sow_wheat(self):
        location = self.board_inverted[TT.Field].pop()
        self.board_inverted[TT.Wheat_Field_3].add(location)
        self.board[location].add(TT.Wheat_Field_3)
        self.board[location].discard(TT.Field)

    def _count_and_replace_tiles(self, tile_a, tile_b):
        lookup = self.board_inverted
        board = self.board
        count = 0
        while len(lookup[tile_a]) > 0:
            count += 1
            location = lookup[tile_a].pop()
            lookup[tile_b].add(location)
            board[location].add(tile_b)
            board[location].discard(tile_a)
        return count

    def harvest(self):
        wheat = 0
        pumpkin = 0
        for tile_a, tile_b in HARVEST_SEQUENCE:
            count = self._count_and_replace_tiles(tile_a, tile_b)
            if 'wheat' in tile_a:
                wheat += count
            else:
                pumpkin += count
        return {'wheat':wheat, 'pumpkin':pumpkin}





