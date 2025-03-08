class AIPlayer:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.state = AIState.IDLE
        self.controlled_units = []  # List of unit IDs
        self.controlled_cities = [] # List of city IDs
        self.strategy = "balanced"  # e.g., "aggressive", "defensive"

    def make_decision(self):
        # Placeholder: implement decision logic based on current state and surroundings
        pass