from attrdict import AttrDict
from constants import RESOURCE_TYPES as RT, TILE_TYPES as TT


class AnimalInventory:
    def __init__(self, **kwargs):
        self.cows = kwargs.get('cows', 0)
        self.dogs = kwargs.get('dogs', 0)
        self.donkeys = kwargs.get('donkeys', 0)
        self.pigs = kwargs.get('pigs', 0)
        self.sheep = kwargs.get('sheep', 0)

class AnimalContainer:
    def __init__(self,**kwargs):
        self._board_type = kwargs['board_type']
        self._is_forest = self._board_type == 'forest'
        self._tile_type = kwargs['tile_type']
        self.position = kwargs['position']
        self._animals = AttrDict({'cows': 0, 'dogs': 0, 'donkeys': 0, 'pigs': 0, 'sheep': 0})
        self._capacity = AttrDict({
            'cows': kwargs.get('cows', 0), 
            'dogs': 100, 
            'donkeys': kwargs.get('donkeys', 0), 
            'pigs': kwargs.get('pigs', 0), 
            'sheep': kwargs.get('sheep', 0),
            'generic': kwargs.get('generic',0)
        })

    def fill_animals(self, animal, qty_requested):
        animals = self._animals
        capacity = 100 if animal == RT.Dogs else self.remaining_capacity(animal)
        qty_filled = min(capacity, qty_requested)
        animals[animal] += qty_filled

        if self._is_forest and animals.dogs > 0:
            self._capacity.sheep = animals.dogs + 1
        return qty_requested - qty_filled

    def add_single_dog(self, reference_qty):
        if reference_qty < 1:
            return reference_qty
        self.animals.dogs += 1
        if self.board_type == 'forest':
            self._capacity.sheep = self.animals.dogs + 1
        reference_qty -= 1
        return reference_qty

    def sum_of_farm_animals_excluding(self, animal_excluded):
        animals = ['cows', 'donkeys', 'pigs', 'sheep']
        qty = self._animals
        animal_sum = sum([qty[animal] for animal in animals if animal != animal_excluded])
        return animal_sum

    def remaining_capacity(self, animal):
        if self.sum_of_farm_animals_excluding(animal) > 0:
            return 0
        capacity = self._capacity
        qty = self._animals
        return max(capacity.generic, capacity[animal]) - qty[animal]

    def is_unfilled_container_of(self, animal):
        return self._capacity[animal] > self._animals[animal]

    @property
    def cows(self):
        return self._animals.cows

    @property
    def dogs(self):
        return self._animals.dogs

    @property
    def donkeys(self):
        return self._animals.donkeys

    @property
    def pigs(self):
        return self._animals.pigs
    
    @property
    def sheep(self):
        return self._animals.sheep

    @property
    def generic_capacity(self):
        return self._capacity.generic


class AnimalManager:
    def __init__(self, **kwargs):
        self.caves = kwargs['caves']
        self.forest = kwargs['forest']
        self.number_of_dwarves = kwargs.get('number_of_dwarves', 2)
        self.animal_inventory = kwargs.get('inventory', AnimalInventory())
        self.trigger_choice = kwargs.get('trigger_choice', False)
        self.discard_excess = kwargs.get('discard_excess', True)
        self.is_breeding_phase = kwargs.get('is_breeding_phase', True)
        self.animal_containers = self._create_containers()

    def _create_containers(self):
        containers = []
        for tile, positions in self.caves.items():
            if tile == 'board_type':
                continue
            for pos in positions:
                new_container = self._build_animal_container('caves', tile, pos)
                containers.append(new_container)
        for tile, positions in self.forest.items():
            if tile == 'board_type':
                continue
            for pos in positions:
                new_container = self._build_animal_container('forest', tile, pos)
                containers.append(new_container)
        return containers

    def _build_animal_container(self, board_type, tile, position):
        container = {
            'board_type': board_type, 
            'tile_type': tile, 
            'position': position
        }
        if tile == 'Large_pasture_2':
            container['generic'] = 16
        elif tile == 'Large_pasture_1':
            container['generic'] = 8
        elif tile == 'Large_pasture_0':
            container['generic'] = 4
        elif tile == 'Small_pasture_1':
            container['generic'] = 4
        elif tile == 'Small_pasture_0':
            container['generic'] = 2
        elif tile == 'Meadow_1':
            container['generic'] = 1
        elif tile == 'Meadow_0':
            container['generic'] = 0
        elif tile == 'Forest':
            container['pigs'] = 1
        elif tile == 'Field':
            container['generic'] = 1
        elif tile == 'Breakfast_Room':
            container['cows'] = 3
        elif tile == 'Cuddle_Room':
            container['sheep'] = self.number_of_dwarves
        elif tile == 'Mixed_Dwelling':
            container['generic'] = 2
        elif tile == 'Ore_Mine':
            container['donkeys'] = 1
        elif tile == 'Ruby_Mine':
            container['donkeys'] = 1
        elif tile == 'Starting_Tile':
            container['generic'] = 2
        animal_container = AnimalContainer(**container)
        return animal_container

    def _assign_dogs(self, dog_qty):
        meadows = list(filter(lambda x: 'Meadow' in x._tile_type, self.animal_containers))
        meadows.sort(key=lambda x: x.generic_capacity)
        pastures = list(filter(lambda x: 'pasture' in x._tile_type, self.animal_containers))
        pastures.sort(key=lambda x: x.generic_capacity)
        starting_tiles = list(filter(lambda x: x=='Starting_Tile', self.animal_containers))
        if len(meadows) > 0:
            while dog_qty > 0:
                for meadow in meadows:
                    dog_qty = meadow.add_single_dog(dog_qty)
        elif len(pastures) > 0:
            pasture = pastures[0]
            dog_qty = pasture.fill_animals('dogs', dog_qty)
        else:
            starting_tile = starting_tiles[0]
            dog_qty = starting_tile.fill_animals('dogs', dog_qty)
        return dog_qty

    def _get_containers_for(self, animal):
        inv = self.animal_inventory
        locations = list(filter(lambda x: x.is_unfilled_container_of(animal), inv))
        return locations

    def fill_animal_specific_locations(self, cows, donkeys, pigs, sheep):
        animals = [('cows', cows),('donkeys', donkeys),('pigs', pigs),('sheep', sheep)]
        updated_animals = []
        for name, qty in animals:
            while qty > 0:
                locations = self._get_containers_for(name)
                if len(locations) > 0:
                    qty = locations[0].fill_animals(name, qty)
                    continue
                break
            updated_animals.append(qty)
        cows = updated_animals[0]
        donkeys = updated_animals[1]
        pigs = updated_animals[2]
        sheep = updated_animals[3]
        return cows, donkeys, pigs, sheep

