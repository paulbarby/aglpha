class City:
    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position  # (x, y)
        self.status = CityStatus.PEACEFUL
        self.population = 1
        self.resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}
        self.buildings = []         # List of building names or objects (e.g., Granaries, Workshops)
        self.production_queue = []  # Units/buildings being produced
