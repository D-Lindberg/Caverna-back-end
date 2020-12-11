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

to place a tile. verify that it can be placed and then place or don't place depending on results of verification. finally return true or false of placement.

#export all locations that can have animals to the animal manager.

#answer if a player has a specific tile/building(mainly buildings) reply should only need to be true or false.

#reply answer to whether a specific coordinate has been filled (will be used to apply bonuses)

#given aspecific coordinate reply with what type of tile or building is there or none

#give the total count/occurance of specific types of tile(s)/building(s) again for bonuses or actions.

#return the total count of undiscovered spaces

#dwarf capacity is determined by specific buildings. need to reply with that capacity.

#certain buildings present action options that can be used at various times. Tile manager needs to reply with a list of action options.

chould be able to export everything to be saved back in database

'''

class TileManager2:
    def __init__(self, **kwargs):
        self.WIDTH = 5
        self.HEIGHT = 6
        self.PLAY_AREA = self.play_area_coordinates()
        self.ALL_POSITIONS = self.all_coordinates()
        self.tiles_to_place = []
        self.arrange_animals_triggered = False


        self.caves_location_to_types = kwargs.get('caves',{})
        if not self.caves_location_to_types:
            self.caves_location_to_types = self.generate_cave_dict()
        self.caves_type_to_locations = self.convert_cave_dict()

        self.forest_location_to_types = kwargs.get('forest', {})
        if not self.forest_location_to_types:
            self.forest_location_to_types = self.generate_forest_dict()
        self.forest_type_to_locations = self.convert_forest_dict()

        self.update_large_pasture_locations()

        #variable
        self.expandable_forest = self.has_tile_named(BT.Office_Room)
        self.tunnels_are_also_caverns = self.has_tile_named(BT.Work_Room)

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

    def generate_cave_dict(self):
        D = {location: [] for location in self.PLAY_AREA}
        D[(1, 1)].append(TT.Starting_Tile)
        D[(1, 2)].append(TT.Cavern)
        return D
    
    def convert_cave_dict(self):
        D = {building : [] for building in BT.values()}
        del D[BT.Unavailable]
        for tile_type in CAVE_TYPES:
            D[tile_type] = []
        D['empties'] = set(self.PLAY_AREA)
        for (location, tile_types) in self.caves_location_to_types.items():
            for tile_type in tile_types:
                D[tile_type].append(location)
                D['empties'].discard(location)
        return D

    def generate_forest_dict(self):
        D = {location: [] for location in self.ALL_POSITIONS}
        return D

    def convert_forest_dict(self):
        D = {tile_type: [] for tile_type in FOREST_TYPES}
        del D[DUAL_TILES.Field_Meadow]
        D['empties'] = set(self.PLAY_AREA)
        extra_empty_spaces = set(self.ALL_POSITIONS) - set(self.PLAY_AREA)
        extra_empty_spaces.discard((0,0))
        extra_empty_spaces.discard((0,5))
        extra_empty_spaces.discard((4,0))
        extra_empty_spaces.discard((4,5))
        D['extra empties'] = extra_empty_spaces
        for (location, tile_types) in self.forest_location_to_types:
            for tile_type in tile_types:
                D[tile_type].append(location)
                D['empties'].discard(location)
                D['extra empties'].discard(location)
        return D
        
    def update_large_pasture_locations(self):
        types = self.forest_type_to_locations
        coordinates = self.forest_location_to_types
        tile_a = TT.Pasture_Large_Left
        tile_b = TT.Pasture_Large_Right
        starting_positions = set(types[tile_a])
        matching_positions = set(types[tile_b])
        while len(types['Large Pastures']) != len(types[tile_a]):
            pasture_coordinates = []
            for (x, y) in starting_positions:
                match_above = tile_b in coordinates[(x, y + 1)]
                match_on_side = tile_b in coordinates[(x + 1, y)]
                if match_above and match_on_side:
                    if (x, y + 1) in matching_positions and (x + 1, y) in matching_positions:
                        continue

                if match_above and (x, y + 1) in matching_positions:
                    pasture_coordinates.append(((x, y), (x, y + 1)))
                    break
                pasture_coordinates.append(((x, y), (x + 1, y)))
                break
            types['Large Pastures'].append(pasture_coordinates)
            starting_positions.discard(pasture_coordinates[0])
            matching_positions.discard(pasture_coordinates[1])

    def empty_space_count_for_scoring(self):
        return len(self.forest_type_to_locations['empties']) + len(self.caves_type_to_locations['empties'])


    def get_all_locations_of(self, tile_name):
        F = self.forest_type_to_locations
        C = self.caves_type_to_locations
        return F[tile_name] if tile_name in FOREST_TYPES else C[tile_name]

    def get_tile_count(self, tile_name):
        return len(self.get_all_locations_of(tile_name))

    def get_tile_count_from_list_of_types(self, list_of_types):
        return sum([self.get_tile_count(tile_name) for tile_name in list_of_types])

    def has_tile_named(self, tile_name):
        return self.get_tile_count(tile_name) > 0

    def get_dwarf_Capacity(self):
        capacity = 2
        capacity += self.get_tile_count_from_list_of_types([
            BT.Dwelling, 
            BT.Simple_Dwelling1,
            BT.Simple_Dwelling2
        ])
        capacity += 2 * self.get_tile_count(BT.Couple_Dwelling)
        if capacity > 5:
            capacity = 5
        capacity += self.get_tile_count(BT.Additional_Dwelling)
        return capacity
    
    def get_name_of_tile_at(self, position, is_forest):
        return self.forest_location_to_types[position] if is_forest else self.caves_location_to_types[position]

    def locations_already_occupied_excluding_stables(self, is_forest):
        board = self.forest_type_to_locations if is_forest else self.caves_type_to_locations
        coordinates = self.ALL_POSITIONS if is_forest else self.PLAY_AREA
        all_occupied = set(coordinates) - board['empties']
        diffrent_board = self.forest_location_to_types if is_forest else self.caves_location_to_types
        return [location for location in all_occupied if diffrent_board[location] != [TT.Stable]]

    def excluding_stables_was_tile_placed_at(self, position, is_forest):
        names = self.forest_location_to_types[position] if is_forest else self.caves_location_to_types[position]
        return True if len(names) == 2 or len(names) == 1 and TT.Stable not in names else False

    def all_actions_from_buildings(self):
        return [BUILDING_TILE_ACTIONS[building] for building, _locations in self.caves_type_to_locations.items() if building in BUILDINGS_WITH_ACTIONS]

    def animal_locations_in(self, board_type):
        if board_type == 'forest':
            initial_board = self.forest_type_to_locations
            other_board = self.forest_location_to_types
            base_set = set(ANIMAL_TILE_TYPES).intersection(set(FOREST_TYPES))
        else:
            initial_board = self.caves_type_to_locations
            other_board = self.caves_location_to_types
            base_set = set(ANIMAL_TILE_TYPES).difference(set(FOREST_TYPES))
        base_locations = set([initial_board[tile] for tile in base_set])
        return [(board_type, location, other_board[location]) for location in base_locations]

    def all_animal_locations(self):
        locations = []
        locations.extend(self.animal_locations_in('forest'))
        locations.extend(self.animal_locations_in('caves'))
        return locations






class Tile_Manager:
    def __init__(self, **kwargs):
        #constants or not passed in via kwargs
        self.WIDTH = 5
        self.HEIGHT = 6
        self.PLAY_AREA = self.normal_area_coordinates()
        self.ALL_POSITIONS = self.generate_coordinates()
        self.tiles_to_place = []
        self.arrange_animals_triggered = False
        
        #variable
        self._large_pastures = kwargs.get('Large_Pastures', [])
        self.stable_locations = kwargs.get('Stable_Locations', [])
        self.caves = kwargs.get('Caves', self.new_board('cave'))
        self.forest = kwargs.get('Forest', self.new_board('forest'))
        self.expandable_forest = self.has_tile_named(BT.Office_Room)
        self.tunnels_are_also_caverns = self.has_tile_named(BT.Work_Room)


        
        #may not need
        self._first_part_of_double = [-1, -1]
        self._is_placing_second_part_of_tile = False

    def normal_area_coordinates(self):
        result = []
        for x in range(1, self.WIDTH - 1):
            for y in range(1, self.HEIGHT - 1):
                result.append((x, y))
        return result

    def generate_coordinates(self):
        results = []
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                results.append((x, y))
        return results

    #(X, Y) = board[X][Y] with (0, 0) at bottom left.
    def new_board(self, board_type):
        board = [[-2 for _y in range(6)] for _x in range(5)]
        for (x, y) in self.PLAY_AREA:
            board[x][y] += 1
        if board_type == 'cave':
            board[1][1] = TT.Starting_Tile
            board[1][2] = TT.Cavern
        return board

    def empty_space_count_for_scoring(self):
        empty_count = 0
        for (x, y) in self.PLAY_AREA:
            if self.caves[x][y] == -1:
                empty_count += 1
            if self.forest[x][y] == -1 and (x, y) not in self.stable_locations:
                empty_count += 1
        return empty_count


    def get_all_locations_of(self, tile_name):
        if tile_name == TT.Stable:
            return self.stable_locations
        is_forest = tile_name in FOREST_TYPES
        board = self.forest if is_forest else self.caves
        locations = []
        for (x, y) in self.ALL_POSITIONS:
            if board[x][y] == tile_name:
                locations.append((x, y))
        return locations

    def get_tile_count(self, tile_name):
        if tile_name == TT.Stable:
            return len(self.stable_locations)
        return len(self.get_all_locations_of(tile_name))

    def get_tile_count_from_list_of_types(self, list_of_types):
        count = 0
        for type in list_of_types:
            count += self.get_tile_count(type)
        return count

    def has_tile_named(self, tile_name):
        return self.get_tile_count(tile_name) > 0

    def get_dwarf_Capacity(self):
        capacity = 2
        capacity += self.get_tile_count_from_list_of_types([
            BT.Dwelling, 
            BT.Simple_Dwelling1,
            BT.Simple_Dwelling2
        ])
        capacity += 2 * self.get_tile_count(BT.Couple_Dwelling)
        if capacity > 5:
            capacity = 5
        capacity += self.get_tile_count(BT.Additional_Dwelling)
        return capacity


    def get_name_of_tile_at(self, position, is_forest):
        tile_area = self.forest if is_forest else self.caves
        x, y = position
        result = []
        result.append(tile_area[x][y])
        if is_forest and position in self.stable_locations:
            result.append(TT.Stable)
            if result == [-1, TT.Stable]:
                result = [TT.Stable] 
        return result

    def locations_already_occupied_excluding_stables(self, is_forest):
        tile_area = self.forest if is_forest else self.caves
        spaces = []
        for (x, y) in self.ALL_POSITIONS:
            if tile_area[x][y] != -1:
                spaces.append((x, y))
        return spaces

    def excluding_stables_was_tile_placed_at(self, position, is_forest):
        name = self.get_name_of_tile_at(position, is_forest)[0]
        return False if name == -1 or TT.Stable in name else True

    def all_actions_from_buildings(self):
        actions = []
        for column in self.caves:
            for building in column:
                if building in BUILDINGS_WITH_ACTIONS:
                    actions.extend(BUILDING_TILE_ACTIONS[building])
        return actions

    def animal_locations_in(self, board_type):
        board = self.forest if board_type == "forest" else self.caves
        ANIMAL_TILE_TYPES
        locations = []
        for x, column in enumerate(board):
            for y, tile_type in enumerate(column):
                location_details = []
                if tile_type in ANIMAL_TILE_TYPES:
                    location_details.append(tile_type)
                if board_type == 'forest':
                    if (x, y) in self.stable_locations:
                        location_details.append(TT.Stable)
                if len(location_details) > 0:
                    locations.append((board_type, (x,y), location_details))
        return locations

    def all_animal_locations(self):
        locations = []
        locations.extend(self.animal_locations_in('forest'))
        locations.extend(self.animal_locations_in('caves'))
        return locations





    def get_large_pastures(self):
        return self._large_pastures
    
    def has_space_for_tile(self, tyle_type):
        return self.has_space_for_tiles([tyle_type])
    
    def has_tiles_to_place(self,):
        return len(self.tiles_to_place) > 0

    def set_tiles_to_place(self, input_tiles):
        self.tiles_to_place = input_tiles
        return self.get_valid_tile_spots()
    
    def has_space_for_tiles(self, tyle_types):
        temp = self.tiles_to_place
        self.tiles_to_place = tyle_types
        can_place = len(self.get_valid_tile_spots()) > 0
        self.tiles_to_place = temp
        return can_place

    def get_next_tile(self):
        return self.tiles_to_place[0]

    def set_building_to_place(self, building_type):
        self.tiles_to_place = [building_type]
        return self.get_valid_building_spots()

    def can_build_large_pasture(self):
        meadows = self.get_matching_tile_spaces([TT.Meadow], True)
        temp = self.filter_position_adjacent_to_another_member_of(meadows)
        return len(temp) > 0

    def get_matching_tile_spaces(self, list_of_tile_types, is_forest):
        tile_area = self.forest if is_forest else self.caves
        results = []
        for (x, y) in self.ALL_POSITIONS:
            if tile_area[x][y] in list_of_tile_types:
                results.append((x, y))
        return results

    def is_adjacent(self, pos_1, pos_2):
        X1, Y1 = pos_1
        X2, Y2 = pos_2
        if X1 == X2 and abs(Y1 - Y2) == 1:
            return True
        if Y1 == Y2 and abs(X1 - X2) == 1:
            return True
        return False

    def filter_position_adjacent_to_another_member_of(self, positions):
        results = []
        for i, pos_1 in enumerate(positions):
            for j in range(i + 1, len(positions)):
                pos_2 = positions[j]
                if self.is_adjacent(pos_1, pos_2):
                    results.append(pos_1)
        return results

    def filter_positions_adjacent_to_target(self, positions, target):
        results = []
        for position in positions:
            if self.is_adjacent(position, target):
                results.append(position)
        return results

    def strip_away_locations_with_existing_stables_from(self, positions):
        locations = []
        for position in positions:
            if position not in self.stable_locations:
                locations.append(position)
        return locations

    def set_building_tile_at(self, position, bulding_type):
        self.caves[position[0]][position[1]] = bulding_type

    def has_empty_adjacent_tile(self, position, is_forest):
        result = self.get_adjacent_empty_spaces(position, is_forest)
        return len(result) > 0

    def get_valid_single_empty_tile_spaces(self, is_forest):
        tile_area = self.forest if is_forest else self.caves
        result = []
        xx, yy = self._first_part_of_double
        for (x, y) in self.ALL_POSITIONS:
            if tile_area[x][y] != -1 and xx != x or yy != y:
                result.extend(self.get_adjacent_empty_spaces((x,y), is_forest))
            if is_forest and x == 2 and y == 0 and tile_area[x][y] == -1:
                result.append((x, y))
        results = list(set(result))
        return results

    def get_adjacent_empty_spaces(self, position, is_forest):
        tile_area = self.forest if is_forest else self.caves
        result = []
        x, y = position
        if x > 0 and tile_area[x - 1][y] == -1:
            result.append((x -1, y))
        if x < self.WIDTH and tile_area[x + 1][y] == -1:
            result.append((x + 1, y))
        if y > 0 and tile_area[x][y - 1] == -1:
            result.append((x, y - 1))
        if y < self.HEIGHT and tile_area[x][y + 1] == -1:
            result.append((x, y + 1))
        return result

    def get_valid_tile_spots(self):
        tile = self.tiles_to_place[0]
        number_of_tiles_to_place = len(self.tiles_to_place)
        is_forest = tile in FOREST_TYPES or tile == TT.Stable
        deep_tile = tile == TT.Ore_Mine or tile == TT.Deep_Tunnel

        if tile == TT.Pasture_Large_Right:
            meadows = self.get_matching_tile_spaces([TT.Meadow], is_forest)
            return self.filter_position_adjacent_to_another_member_of(meadows)

        if tile == TT.Pasture_Large_Left:
            meadows = self.get_matching_tile_spaces([TT.Meadow], is_forest)
            target = self._first_part_of_double
            return self.filter_positions_adjacent_to_target(meadows, target)

        if tile == TT.Pasture_Small:
            return self.get_matching_tile_spaces([TT.Meadow], is_forest)

        if tile == TT.Stable:
            potential_spots = self.get_matching_tile_spots([-1, TT.Meadow, TT.Pasture_Small, TT.Pasture_Large_Left, TT.Pasture_Large_Right], is_forest)
            return self.strip_away_locations_with_existing_stables_from(potential_spots)

        if tile == TT.Ruby_Mine:
            return self.get_matching_tile_spaces([TT.Tunnel, TT.Deep_Tunnel], is_forest)


        if deep_tile:
            tunnels = self.get_matching_tile_spaces([TT.Tunnel], is_forest)
            if number_of_tiles_to_place == 1:
                return tunnels
            return self.filter_position_adjacent_to_another_member_of(tunnels)
        
        valid_spaces = self.get_valid_single_empty_tile_spaces(is_forest)
        if number_of_tiles_to_place > 1:
            result_spaces = []
            for valid_space in valid_spaces:
                empty_spaces = self.get_adjacent_empty_spaces(valid_space, is_forest)
                if len(empty_spaces) > 0:
                    result_spaces.extend(empty_spaces)
                    result_spaces.append(valid_space)
            if tile == TT.Field:
                return self.strip_away_locations_with_existing_stables_from(result_spaces)
            return result_spaces
        if self._is_placing_second_part_of_tile:
            first_location = self._first_part_of_double
            if is_forest and first_location == (2,0):
                return self.get_adjacent_empty_spaces(first_location, is_forest)
            if self.has_empty_adjacent_tile(first_location, is_forest):
                return self.get_adjacent_empty_spaces(first_location, is_forest)
            return self.filter_positions_adjacent_to_target(valid_spaces, first_location)
        if tile == TT.Field:
            return self.strip_away_locations_with_existing_stables_from(valid_spaces)
        return valid_spaces







A = Tile_Manager()
A.forest[1][1] = TT.Meadow
A.forest[1][2] = TT.Meadow
A.stable_locations.append((1, 2))
A.stable_locations.append((1, 3))
print(A.can_build_large_pasture())
B = Tile_Manager()
B.forest[1][1] = TT.Meadow
B.forest[1][3] = TT.Meadow
print(B.can_build_large_pasture())
B.caves[3][4] = BT.Dwelling
print(A.get_dwarf_Capacity())
print(B.get_dwarf_Capacity())
print(A.all_animal_locations())
print(B.all_animal_locations())
print(A.excluding_stables_was_tile_placed_at((1,1), True)) #True
print(A.excluding_stables_was_tile_placed_at((1,2), True)) #True
print(A.excluding_stables_was_tile_placed_at((1,3), True)) #False
print(A.get_name_of_tile_at((1,1), True))
print(A.get_name_of_tile_at((1,2), True))
print(A.get_name_of_tile_at((1,3), True))
