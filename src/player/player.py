from src.engine.core_states import AIState

class Player:
    def __init__(self, id, name, color=(255, 255, 255), is_ai=False):
        self.id = id
        self.name = name
        self.color = color  # RGB tuple for player's color
        self.is_ai = is_ai
        
        # AI-specific attributes
        if is_ai:
            self.ai_state = AIState.IDLE
            self.strategy = "balanced"  # e.g., "aggressive", "defensive", "economic"
        
        # Player resources and stats
        self.resources = {
            "food": 0,
            "wood": 0,
            "stone": 0,
            "gold": 0
        }
        
        # Discovered technology and progress
        self.researched_techs = []
        self.current_research = None
        self.research_progress = 0
        
        # References to owned entities
        self.controlled_units = []  # List of unit IDs
        self.controlled_cities = []  # List of city IDs
