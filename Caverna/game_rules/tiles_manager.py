from constants import (
    ACTION_GROUP_TYPES,
    ACTION_SPACE_TYPES, 
    BUILDING_TYPES, 
    CAVERNA_ACTIONS, 
    DISCARD_ACTIONS, 
    DUAL_TILES, 
    EXPEDITION_BREEDING_OPTIONS, 
    EXPEDITION_REWARDS, 
    FOOD_ACTIONS, 
    HARVEST_OPTIONS, 
    HARVEST_TYPES, 
    RESOURCE_TYPES, 
    ROUND_BONUS_TYPES, 
    RUBY_TRADES, 
    TILE_TYPES as TT, 
)


class Tile_Manager:
    def __init__(self):
        self._large_pastures = []
        self.tiles_to_place = []
        self.TILE_AREA_WIDTH = 3
        self.TILE_AREA_HEIGHT = 4
        self.all_coordinates = self.get_list_of_all_board_coordinates()
        #1st quadrant view 
        #access with coordinates (X, Y) with (0, 0) at bottom left
        self.cave_spaces = [[-1 for _y in range(self.TILE_AREA_HEIGHT)] for _x in range(self.TILE_AREA_WIDTH)]
        self.forest_spaces = [[-1 for _y in range(self.TILE_AREA_HEIGHT)] for _x in range(self.TILE_AREA_WIDTH)]
        self.stable_spaces = [[-1 for _y in range(self.TILE_AREA_HEIGHT)] for _X in range(self.TILE_AREA_WIDTH)]
        self.arrange_animals_triggered = False
        self._first_part_of_double = [-1, -1]
        self._is_placing_second_part_of_tile = False
        self.cave_spaces[0][0] = TT.Starting_Tile
        self.cave_spaces[0][1] = TT.Cavern
        self.cave_types = [TT.Cavern, TT.Deep_Tunnel, TT.Ore_Mine, TT.Ruby_Mine, TT.Tunnel]
        self.forest_types = [TT.Field, TT.Meadow, TT.Pasture_Large_Right, TT.Pasture_Large_Left, TT.Pasture_Small, TT.Pumpkin_Field_1, TT.Pumpkin_Field_2, TT.Wheat_Field_1, TT.Wheat_Field_2, TT.Wheat_Field_3]

    def get_list_of_all_board_coordinates(self):
        results = []
        for x in range(self.TILE_AREA_WIDTH):
            for y in range(self.TILE_AREA_HEIGHT):
                results.append((x, y))
        return results

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
        if is_forest:
            tile_area = self.forest_spaces
        else:
            tile_area = self.cave_spaces
        results = []
        for (x, y) in self.all_coordinates:
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
        results = []
        for (x, y) in positions:
            if self.stable_spaces[x][y] == -1:
                results.append((x, y))
        return results

    def set_building_tile_at(self, position, bulding_type):
        self.cave_spaces[position[0]][position[1]] = bulding_type

    def has_empty_adjacent_tile(self, position, is_forest):
        result = self.get_adjacent_empty_spaces(position, is_forest)
        return len(result) > 0

    def get_valid_single_empty_tile_spaces(self, is_forest):
        if is_forest:
            tile_area = self.forest_spaces
        else:
            tile_area = self.cave_spaces
        result = []
        xx, yy = self._first_part_of_double
        for (x, y) in self.all_coordinates:
            if tile_area[x][y] != -1 and xx != x or yy != y:
                result.extend(self.get_adjacent_empty_spaces((x,y), is_forest))
            if is_forest and x == 2 and y == 0 and tile_area[x][y] == -1:
                result.append((x, y))
        results = list(set(result))
        return results

    def get_adjacent_empty_spaces(self, position, is_forest):
        if is_forest:
            tile_area = self.forest_spaces
        else:
            tile_area = self.cave_spaces
        result = []
        x, y = position
        if x > 0 and tile_area[x - 1][y] == -1:
            result.append((x -1, y))
        if x < self.TILE_AREA_WIDTH and tile_area[x + 1][y] == -1:
            result.append((x + 1, y))
        if y > 0 and tile_area[x][y - 1] == -1:
            result.append((x, y - 1))
        if y < self.TILE_AREA_HEIGHT and tile_area[x][y + 1] == -1:
            result.append((x, y + 1))
        return result

    def get_dwarf_Capacity(self):
        capacity = 2
        capacity += self.get_tile_count(BUILDING_TYPES.Dwelling)
        capacity += self.get_tile_count(BUILDING_TYPES.Simple_Dwelling1)
        capacity += self.get_tile_count(BUILDING_TYPES.Simple_Dwelling2)
        capacity += 2 * self.get_tile_count(BUILDING_TYPES.Couple_Dwelling)
        if capacity > 5:
            capacity = 5
        capacity += self.get_tile_count(BUILDING_TYPES.Additional_Dwelling)
        return capacity

    def get_tile_count(self, tile_type_to_match):
        tile_count = 0
        for (x, y) in self.all_coordinates:
            if self.cave_spaces[x][y] == tile_type_to_match:
                tile_count += 1
            if self.forest_spaces[x][y] == tile_type_to_match:
                tile_count += 1
            if self.stable_spaces[x][y] == tile_type_to_match:
                tile_count += 1
        return tile_count
    
    def get_tile_type(self, position, is_forest):
        x, y = position
        if is_forest:
            tile_area = self.forest_spaces
        else:
            tile_area = self.cave_spaces
        result = []
        result.append(tile_area[x][y])
        if is_forest and self.stable_spaces[x][y] != -1:
            result.append(TT.Stable)

    def set_tile_at(self, position, is_forest, is_expedition):
        food_gain = 0
        pig_gain = 0
        ruby_gain = 0

        return [food_gain, pig_gain, ruby_gain]

    def get_valid_tile_spots(self):
        tile = self.tiles_to_place[0]
        number_of_tiles_to_place = len(self.tiles_to_place)
        is_forest = tile in self.forest_types or tile == TT.Stable
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
A.forest_spaces[0][0] = TT.Meadow
A.forest_spaces[0][1] = TT.Meadow
print(A.can_build_large_pasture())
B = Tile_Manager()
B.forest_spaces[0][0] = TT.Meadow
B.forest_spaces[0][2] = TT.Meadow
print(B.can_build_large_pasture())