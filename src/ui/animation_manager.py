class AnimationManager:
    def __init__(self):
        self.animations = {}  # {animation_id: Animation}

    def add_animation(self, animation):
        self.animations[animation.id] = animation

    def update_animations(self):
        # Iterate and update all active animations
        for animation in self.animations.values():
            animation.update(1)  # '1' is a placeholder for delta time