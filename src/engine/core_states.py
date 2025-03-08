from enum import Enum, auto

# High-level game flow
class GameState(Enum):
    MAIN_MENU = auto()
    NEW_GAME = auto()
    LOAD_GAME = auto()  # Added missing enum value
    IN_GAME = auto()
    PAUSED = auto()
    GAME_OVER = auto()

# Unit behavior and actions
class UnitState(Enum):
    IDLE = auto()
    MOVING = auto()
    ATTACKING = auto()
    DEFENDING = auto()
    SELECTED = auto()
    DESTROYED = auto()

# City condition and status
class CityStatus(Enum):
    PEACEFUL = auto()
    UNDER_ATTACK = auto()
    DEVELOPING = auto()
    AT_WAR = auto()

# AI behavior patterns
class AIState(Enum):
    IDLE = auto()
    EXPANDING = auto()
    ATTACKING = auto()
    DEFENSIVE = auto()
    DIPLOMATIC = auto()

# Animation phases for visual feedback
class AnimationState(Enum):
    IDLE = auto()
    WALKING = auto()
    ATTACKING = auto()
    DYING = auto()
    SPAWNING = auto()
