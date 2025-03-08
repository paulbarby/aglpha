class UIComponent:
    def __init__(self, id, component_type, position, size):
        self.id = id
        self.component_type = component_type  # e.g., "button", "menu", "tooltip"
        self.position = position
        self.size = size
        self.visible = True

    # Consider adding a base render method for consistency
    def render(self, screen):
        """Base render method to be overridden by subclasses."""
        pass