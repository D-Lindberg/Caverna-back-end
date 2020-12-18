from typing import Dict, List, Set, Tuple
from constants import DISCARD_ACTIONS as DA, TRADES_TO_FOOD as TTF


class AnimalInventory:
    def __init__(self, **kwargs):
        self.cows: int = kwargs.get('cows', 0)
        self.dogs: int = kwargs.get('dogs', 0)
        self.donkeys: int = kwargs.get('donkeys', 0)
        self.pigs: int = kwargs.get('pigs', 0)
        self.sheep: int = kwargs.get('sheep', 0)
        self.generic: int = kwargs.get('generic', 0)

    @property
    def total_farm_animals(self) -> int:
        return self.cows + self.donkeys + self.pigs + self.sheep

    def total_farm_animals_excluding(self, animal_name: str) -> int:
        total = self.total_farm_animals
        qty_of_current_animal = getattr(self, animal_name, 0)
        return total - qty_of_current_animal

    @property
    def total_all_animals(self) -> int:
        return self.total_farm_animals + self.dogs

    def set_animal(self, animal_name: str, qty: int) -> None:
        setattr(self, animal_name, qty)

    def increment_animal(self, animal_name: str, qty: int) -> None:
        current_value = getattr(self, animal_name, 0)
        new_value = current_value + qty
        setattr(self, animal_name, new_value)

    def decrement_animal(self, animal_name: str, qty: int) -> None:
        adjusted_qty = qty * -1
        self.increment_animal(animal_name, adjusted_qty)

    def extract_as_dict(self) -> Dict[str, int]:
        d = {'cows': self.cows, 'dogs': self.dogs, 'donkeys': self.donkeys,
            'pigs': self.pigs, 'sheep': self.sheep, 'generic': self.generic}
        return d


class AnimalContainer:
    def __init__(self,**kwargs):
        self._board_type = kwargs['board_type']
        self._is_forest = self._board_type == 'forest'
        self._tile_type = kwargs['tile_type']
        self.position = kwargs['position']
        self._animals = AnimalInventory()
        self._capacity = AnimalInventory(**{
            'cows': kwargs.get('cows', 0), 
            'dogs': 100, 
            'donkeys': kwargs.get('donkeys', 0), 
            'pigs': kwargs.get('pigs', 0), 
            'sheep': kwargs.get('sheep', 0),
            'generic': kwargs.get('generic',0)
        })

    def update_sheep_capacity(self) -> None:
        if self._is_forest:
            self._capacity.sheep = self._animals.dogs + 1

    def fill_animals(self, animal: str, qty_requested: int) -> int:
        animals = self._animals
        capacity = self.remaining_capacity(animal)
        qty_filled = min(capacity, qty_requested)
        animals.increment_animal(animal, qty_filled)
        self.update_sheep_capacity()
        return qty_requested - qty_filled

    def add_single_dog(self, reference_qty: int) -> int:
        if reference_qty < 1:
            return reference_qty
        self._animals.increment_animal('dogs', 1)
        self.update_sheep_capacity()
        reference_qty -= 1
        return reference_qty

    def remaining_capacity(self, animal: str) -> int:
        if animal == 'dogs':
            return 100
        qty_other_animals = self._animals.total_farm_animals_excluding(animal)
        if qty_other_animals > 0:
            return 0
        generic_capacity = self._capacity.generic
        specific_capacity = getattr(self._capacity, animal, 0)
        animal_qty = getattr(self._animals, animal, 0)
        if self._tile_type == 'Starting_Tile':
            return generic_capacity - animal_qty
        return max(generic_capacity, specific_capacity) - animal_qty

    def is_unfilled_container_of(self, animal: str) -> bool:
        capacity = getattr(self._capacity, animal, 0)
        amount_placed = getattr(self._animals, animal, 0)
        return capacity > amount_placed

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

    @property
    def farm_animal_count(self):
        return self._animals.total_farm_animals


class AnimalManager:
    def __init__(self, **kwargs):
        self.not_all_animals_placed = True
        self.inventory = kwargs.get('inventory', AnimalInventory())
        self.number_of_dwarves = kwargs.get('number_of_dwarves', 2)
        self.is_breeding_phase = kwargs.get('is_breeding_phase', False)
        self.has_slaughtering_cave = kwargs.get('has_slaughtering_cave', False)
        self.set_or_reset_animal_manager_locations(**kwargs)
        self.options = []
        self.message = ''
        self.unplaced_animals = {}

    def _create_containers(self) -> List[AnimalContainer]:
        containers = []
        for board, b_type in [(self.caves, 'caves'), (self.forest, 'forest')]:
            for tile, positions in board.items():
                if tile == 'board_type':
                    continue
                for pos in positions:
                    new_container = self._build_container(b_type, tile, pos)
                    containers.append(new_container)
        return containers

    def _build_container(self, board_type: str, tile: str, position: Tuple[int, int]):
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

    def get_containers_by_tile_type(self, tile_name_includes: str) -> List[AnimalContainer]:
        locations = list(filter(lambda x: tile_name_includes in x._tile_type, self.containers))
        locations.sort(key=lambda x: x.generic_capacity)
        return locations

    def _assign_dogs(self, dog_qty: int) -> int:
        meadows = self.get_containers_by_tile_type('Meadow')
        pastures = self.get_containers_by_tile_type('pasture')
        starting_tiles = self.get_containers_by_tile_type('Starting')
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

    def _get_containers_for(self, animal: str) -> List[AnimalContainer]:
        containers = self.containers
        filtered_containers = list(filter(lambda x: x.is_unfilled_container_of(animal) and x.remaining_capacity(animal) > x.generic_capacity, containers))
        filtered_containers.sort(key=lambda x: x.generic_capacity)
        return filtered_containers

    def fill_animal_specific_locations(self, animals: Dict[str, int]) -> Dict[str, int]:
        for name, qty in animals.items():
            if name == 'dogs':
                continue
            while qty > 0:
                locations = self._get_containers_for(name)
                if len(locations) > 0:
                    qty = locations[0].fill_animals(name, qty)
                    continue
                break
            animals[name] = qty
        return animals

    def locations_with_capacity_for(self,animal: str) -> List[AnimalContainer]:
        locations = list(filter(lambda x: x.remaining_capacity(animal) > 0, self.containers))
        locations.sort(key=lambda x: x.remaining_capacity(animal), reverse=True)
        return locations

    def empty_containers(self) -> List[AnimalContainer]:
        containers = list(filter(lambda x: x.farm_animal_count == 0, self.containers))
        return containers

    def fill_generic_locations(self, qty_of: Dict[str, int]) -> Dict[str, int]:
        unplaced_animals: Set[str] = set()
        for animal, qty in qty_of.items():
            if qty > 0:
                unplaced_animals.add(animal)
        unfilled_count = len(self.empty_containers())
        animals_placed = True
        while animals_placed:
            animals_placed = False
            if len(unplaced_animals) == unfilled_count:
                empty_containers = self.empty_containers()
                for container in empty_containers:
                    animal = unplaced_animals.pop()
                    qty_of[animal] = container.fill_animals(animal, qty_of[animal])
                break
            largest_qty = max(qty_of.values())
            for a in ['cows', 'pigs', 'donkeys', 'sheep']:
                if qty_of[a] > 0 and qty_of[a] == largest_qty:
                    locations = self.locations_with_capacity_for(a)
                    if len(locations) > 0:
                        qty_of[a] = locations[0].fill_animals(a, qty_of[a])
                        unplaced_animals.discard(a)
                        unfilled_count -= 1
                        animals_placed = True
                        break
        return qty_of

    def _create_message(self, animals: Dict[str, int]) -> str:
        tmp = "Unassigned animals:"
        for name, qty in animals.items():
            if qty > 0:
                tmp += f" {qty} {name},"
        message = tmp[:-1] + '.'
        return message

    def _build_options(self, animals: Dict[str, int]) -> List[str]:
        options = [DA.Discard_All_Unassigned_Animals]
        if self.is_breeding_phase:
            if animals['cows'] > 0:
                options.append(DA.Discard_Cow)
            if animals['donkeys'] > 0:
                options.append(DA.Discard_Donkey)
            if animals['pigs'] > 0:
                options.append(DA.Discard_Pig)
            if animals['sheep'] > 0:
                options.append(DA.Discard_Sheep)
        else:
            if self.has_slaughtering_cave:
                if animals['cows'] > 0:
                    options.append(TTF.Slaughtering_Cave_Convert_Cow)
                if animals['donkeys'] > 1:
                    options.append(TTF.Slaughtering_Cave_Convert_Donkey_Pair)
                if animals['donkeys'] > 0:
                    options.append(TTF.Slaughtering_Cave_Convert_Donkey)
                if animals['pigs'] > 0:
                    options.append(TTF.Slaughtering_Cave_Convert_Pig)
                if animals['sheep'] > 0:
                    options.append(TTF.Slaughtering_Cave_Convert_Sheep)
            else:
                if animals['cows'] > 0:
                    options.append(TTF.Convert_Cow)
                if animals['donkeys'] > 1:
                    options.append(TTF.Convert_Donkey_Pair)
                if animals['donkeys'] > 0:
                    options.append(TTF.Convert_Donkey)
                if animals['pigs'] > 0:
                    options.append(TTF.Convert_Pig)
                if animals['sheep'] > 0:
                    options.append(TTF.Convert_Sheep)
        return options

    def auto_placement(self, inventory: AnimalInventory, discard_excess: bool=False, create_options: bool=False) -> bool:
        animals = inventory.extract_as_dict()
        animals.dogs = self._assign_dogs(animals.dogs)
        animals = self.fill_animal_specific_locations(animals)
        animals = self.fill_generic_locations(animals)
        self.not_all_animals_placed = False
        if sum(animals.values()) == 0:
            return True
        self.unplaced_animals = animals
        if discard_excess:
            for name, qty in animals.items():
                self.inventory.decrement_animal(name, qty)
            return True
        self.not_all_animals_placed = True
        if not create_options:
            return False
        self.message = self._create_message(animals)
        self.options = self._build_options(animals)
        return False

    def set_breeding_phase_to(self, true_or_false: bool) -> None:
        self.is_breeding_phase = true_or_false
        return

    def add_animals(self, name: str, qty: int) -> bool:
        self.inventory.increment_animal(name, qty)
        valid_placement = self.auto_placement(self.inventory, False, True)
        return valid_placement

    def discard_animal(self, name: str, qty: int) -> bool:
        self.inventory.decrement_animal(name, qty)
        valid_placement = self.auto_placement(self.inventory, False, True)
        return valid_placement

    def discard_all_excess(self) -> bool:
        valid_placement = self.auto_placement(self.inventory, True, False)
        return valid_placement

    def will_pass_next_breeding_phase(self) -> Tuple[bool, Dict[str, int]]:
        inventory = self.inventory.extract_as_dict()
        for animal in inventory.keys():
            if animal == 'dogs':
                continue
            if inventory[animal] > 2:
                inventory[animal] +=1
        future_inventory = AnimalInventory(**inventory)
        viable_future = self.auto_placement(future_inventory)
        return viable_future, self.unplaced_animals

    def set_or_reset_animal_manager_locations(self, **kwargs) -> None:
        self.caves = kwargs['caves']
        self.forest = kwargs['forest']
        self.containers = self._create_containers()

    def extract_animal_locations_as_dict(self) -> Tuple[Dict[Tuple[int,int], Dict[str, int]], Dict[str, int]]:
        # structure of animal_dict: {'location coords': {'animal_name': qty}}
        self.auto_placement(self.inventory, False, False)
        animal_layer = {}
        for container in self.containers:
            animal_layer[container.position] = container._animals.extract_as_dict()
        return animal_layer, self.unplaced_animals

    def breeding(self) -> Tuple[bool, Dict[str, int]]:
        inventory = self.inventory.extract_as_dict()
        for animal in inventory.keys():
            if animal == 'dogs':
                continue
            if inventory[animal] > 2:
                inventory[animal] +=1
        future_inventory = AnimalInventory(**inventory)
        valid_placement = self.auto_placement(future_inventory, True, False)
        return valid_placement, self.unplaced_animals

