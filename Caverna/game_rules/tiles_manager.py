from constants import (
    BUILDING_TYPES as BT, 
    BUILDING_TILE_ACTIONS, 
    BUILDINGS_WITH_ACTIONS, 
    TILE_TYPES as TT
    )

'''
time to regroup.
the tile manager should receive game boards from database to load into current working query.

current working queries will be:

to see if a tile can be placed and reply with list of possible placements for a tile.

to place a tile. verify that it can be placed and then place or don't place depending on results of verification. finally return true or false of placement.

export all locations that can have animals to the animal manager.

#answer if a player has a specific tile/building(mainly buildings) reply should only need to be true or false.

#reply answer to whether a specific coordinate has been filled (will be used to apply bonuses)

#given aspecific coordinate reply with what type of tile or building is there or none

#give the total count/occurance of specific types of tile(s)/building(s) again for bonuses or actions.

#return the total count of undiscovered spaces

#dwarf capacity is determined by specific buildings. need to reply with that capacity.

#certain buildings present action options that can be used at various times. Tile manager needs to reply with a list of action options.

chould be able to export everything to be saved back in database

'''

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

    def empty_space_count(self):
        empty_count = 0
        for (x, y) in self.all_coordinates:
            if self.cave_spaces[x][y] == -1:
                empty_count += 1
            if self.forest_spaces[x][y] == -1 and self.stables_spaces[x][y] == -1:
                empty_count += 1
        return empty_count

    def get_tile_count(self, tile_name):
        if tile_name == -1:
            return self.empty_space_count()
        tile_count = 0
        for (x, y) in self.all_coordinates:
            if self.cave_spaces[x][y] == tile_name:
                tile_count += 1
            if self.forest_spaces[x][y] == tile_name:
                tile_count += 1
            if self.stable_spaces[x][y] == tile_name:
                tile_count += 1
        return tile_count

    def get_tile_count_from_list_of_types(self, list_of_types):
        count = 0
        for type in list_of_types:
            count += self.get_tile_count(type)
        return count

    def get_tile_type(self, position, is_forest):
        tile_area = self.forest_spaces if is_forest else self.cave_spaces
        x, y = position
        result = []
        result.append(tile_area[x][y])
        if is_forest and self.stable_spaces[x][y] != -1:
            result.append(TT.Stable)
            if result == [-1, TT.Stable]:
                result = [TT.Stable] 
        return result

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

    def get_occupied_spaces_not_including_stables(self, is_forest):
        tile_area = self.forest_spaces if is_forest else self.cave_spaces
        spaces = []
        for (x, y) in self.all_coordinates:
            if tile_area[x][y] != -1:
                spaces.append((x, y))
        return spaces

    def position_not_empty_excluding_stable(self, position, is_forest):
        tile_area = self.forest_spaces if is_forest else self.cave_spaces
        x, y = position
        return tile_area[x][y] != -1

    def has_tile_named(self, tile_name):
        return self.get_tile_count(tile_name) > 0

    def all_actions_from_buildings(self):
        actions = []
        for column in self.cave_spaces:
            for building in column:
                if building in BUILDINGS_WITH_ACTIONS:
                    actions.extend(BUILDING_TILE_ACTIONS[building])
        return actions

    def get_locations_that_may_hold_animals(self):
        pass



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
        tile_area = self.forest_spaces if is_forest else self.cave_spaces
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
        tile_area = self.forest_spaces if is_forest else self.cave_spaces
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
        tile_area = self.forest_spaces if is_forest else self.cave_spaces
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
B.cave_spaces[2][3] = BT.Dwelling
print(A.get_dwarf_Capacity())
print(B.get_dwarf_Capacity())
