from attrdict import AttrDict
from constants import RESOURCE_TYPES as RT


class AnimalInventory:
    def __init__(self, **kwargs):
        self.cows = kwargs.get('cows', 0)
        self.dogs = kwargs.get('dogs', 0)
        self.donkeys = kwargs.get('donkeys', 0)
        self.pigs = kwargs.get('pigs', 0)
        self.sheep = kwargs.get('sheep', 0)
        self.locations = kwargs.get('locations', [])

class AnimalContainer:
    def __init__(self,**kwargs):
        self._board_type = kwargs.get('board_type')
        self._is_forest = self._board_type == 'forest'
        self._tile_type = kwargs.get('tile_type')
        self._position = kwargs.get('position')
        self._animals = AttrDict({'cows': 0, 'dogs': 0, 'donkeys': 0, 'pigs': 0, 'sheep': 0})
        self._capacity = AttrDict({
            'cows': kwargs.get('cows', 0), 
            'dogs': 100, 
            'donkeys': kwargs.get('donkeys', 0), 
            'pigs': kwargs.get('pigs', 0), 
            'sheep': kwargs.get('sheeps', 0),
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