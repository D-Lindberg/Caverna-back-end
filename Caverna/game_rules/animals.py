class Total_Animals:
    def __init__(self, **kwargs):
        self.cows = kwargs.get('cows', 0)
        self.dogs = kwargs.get('dogs', 0)
        self.donkeys = kwargs.get('donkeys', 0)
        self.pigs = kwargs.get('pigs', 0)
        self.sheep = kwargs.get('sheep', 0)
        #locations should be (x, y, tile_type)
        self.locations = kwargs.get('locations', [])