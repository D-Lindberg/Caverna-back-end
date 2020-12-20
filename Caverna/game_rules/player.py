from player_resources import PlayerResources
from board import Board
from animals import AnimalManager, AnimalInventory
from dwarves import Dwarf
from constants import  BUILDING_TYPES as BT


class CavernaPlayer:
    def __init__(self, new_player=False, food: int=0, **kwargs):
        self.animal_inventory = kwargs.get('animals', AnimalInventory())
        self.board = kwargs.get('board', {})
        self.resources = kwargs.get('resources', PlayerResources())
        self._dwarves = kwargs.get('dwarves', [])
        self._active_dwarf_index = kwargs.get('active_dwarf_index', 0)
        self._expedtion_level = kwargs.get('expedition_level', 0)
        self._expedition_actions_used = kwargs.get('expedition_actions_used', [])
        self.new_round_bonuses = kwargs.get('bonuses', [[]])
        self._harvest_food_requirements
        self.is_breeding_phase = kwargs.get('is_breeding_phase', False)
        self.caves = self.create_sub_board('caves')
        self.forest = self.create_sub_board('forest')
        self.animal_manager = self.setup_animal_manager()
        if new_player:
            self.resources.food = food
            self._dwarves.extend([Dwarf(False, 1), Dwarf(False, 2)])
        self.player_score = kwargs.get('player_score', -100)

    def create_sub_board(self, board_type):
        new_board = {'board_type': board_type}
        if self.board:
            new_board['board'] = {}
            squares = list(filter(lambda x: x.board_type == board_type, self.board))
            for square in squares:
                tiles = set([square.tile_type])
                if square.has_stable:
                    tiles.add('Stable')
                location = (square.pos_x, square.pos_y)
                new_board['board'][location] = tiles
                if board_type == 'caves':
                    new_board['has_work_room'] = square.tile_type == BT.Work_Room
                    new_board['has_stuble_room'] = square.tile_type == BT.Stuble_Room
                    new_board['has_office_room'] = square.tile_type == BT.Office_Room
                else:
                    new_board['has_work_room'] = self.caves.has_tile_named(BT.Work_Room)
                    new_board['has_stuble_room'] = self.caves.has_tile_named(BT.Stuble_Room)
                    new_board['has_office_room'] = self.caves.has_tile_named(BT.Office_Room)
        return Board(**new_board)

    def setup_animal_manager(self):
        manager_requirements = {
            'inventory': self.animal_inventory, 
            'number_of_dwarfs': len(self._dwarves),
            'is_breeding_phase': self.is_breeding_phase,
            'caves': self.caves.extract_animal_locations,
            'forest': self.forest.extract_animal_locations,
            'has_slaughtering_cave': self.caves.has_tile_named(BT.Slaughtering_Cave)
        }
        return AnimalManager(**manager_requirements)


