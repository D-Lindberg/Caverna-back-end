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
    TILE_TYPES, 
)


class Tile_Manager:
    def __init__(self):
        self._large_pastures = []
        self.tiles_to_place = []
        self.TILE_AREA_WIDTH = 3
        self.TILE_AREA_HEIGHT = 4
        #1st quadrant view 
        #access with coordinates (X, Y) with (0, 0) at bottom left
        self.cave_spaces = [[-1 for _y in range(self.TILE_AREA_HEIGHT)] for _x in range(self.TILE_AREA_WIDTH)]
        self.forest_spaces = [[-1 for _y in range(self.TILE_AREA_HEIGHT)] for _x in range(self.TILE_AREA_WIDTH)]
        self.stable_spaces = [[-1 for _y in range(self.TILE_AREA_HEIGHT)] for _X in range(self.TILE_AREA_WIDTH)]
        self.arrange_animals_triggered = False
        self._first_part_of_double = [-1, -1]
        self._is_placing_second_part_of_tile = False
        self.cave_spaces[0][0] = TILE_TYPES.Starting_Tile
        self.cave_spaces[0][1] = TILE_TYPES.Cavern

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
        clearings = self.get_matching_forest_tile_spaces(TILE_TYPES.Meadow)
        for i, pos_1 in enumerate(clearings):
            for j in range(i + 1, len(clearings)):
                pos_2 = clearings[j]
                if self.is_adjacent(pos_1, pos_2):
                    return True
        return False

    def get_matching_forest_tile_spaces(self, tile_to_match):
        results = []
        for x in range(self.TILE_AREA_WIDTH):
            for y in range(self.TILE_AREA_HEIGHT):
                if self.forest_spaces[x][y] == tile_to_match:
                    results.append((x, y))
        return results
    
    def get_matching_cave_tile_spaces(self, tile_to_match):
        results = []
        for x in range(self.TILE_AREA_WIDTH):
            for y in range(self.TILE_AREA_HEIGHT):
                if self.cave_spaces[x][y] == tile_to_match:
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

    def set_building_tile_at(self, position, bulding_type):
        self.cave_spaces[position[0]][position[1]] = bulding_type

    def has_adjacent_tile(self, position, is_forest):
        if is_forest:
            tile_area = self.forest_spaces
        else:
            tile_area = self.cave_spaces
        x, y = position
        if x > 0 and tile_area[x - 1][y] != -1:
            return True
        if x < self.TILE_AREA_WIDTH -1 and tile_area[x + 1][y] != -1:
            return True
        if y > 0 and tile_area[x][y - 1] != -1:
            return True
        if y < self.TILE_AREA_HEIGHT - 1 and tile_area[x][y + 1] != -1:
            return True
        return False

    def get_valid_single_empty_tile_spaces(self, is_forest):
        if is_forest:
            tile_area = self.forest_spaces
        else:
            tile_area = self.cave_spaces
        result = []
        xx, yy = self._first_part_of_double
        for x in range(self.TILE_AREA_WIDTH):
            for y in range(self.TILE_AREA_HEIGHT):
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
        for x in range(self.TILE_AREA_WIDTH):
            for y in range(self.TILE_AREA_HEIGHT):
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
            result.append(TILE_TYPES.Stable)

    def set_tile_at(self, position, is_forest, is_expedition):
        food_gain = 0
        pig_gain = 0
        ruby_gain = 0

        return [food_gain, pig_gain, ruby_gain]






A = Tile_Manager()
A.forest_spaces[0][0] = TILE_TYPES.Meadow
A.forest_spaces[0][1] = TILE_TYPES.Meadow
print(A.can_build_large_pasture())
B = Tile_Manager()
B.forest_spaces[0][0] = TILE_TYPES.Meadow
B.forest_spaces[0][2] = TILE_TYPES.Meadow
print(B.can_build_large_pasture())