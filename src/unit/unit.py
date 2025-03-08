class Unit:
    def __init__(self, id, unit_type, position):
        self.id = id
        self.unit_type = unit_type  # e.g., "Spearmen", "Cavalry"
        self.position = position    # (x, y) coordinate
        self.state = UnitState.IDLE
        self.health = 100
        self.attack_power = 10
        self.defense = 5
        self.move_range = 3
        self.current_animation = None  # Link to an Animation instance if active
