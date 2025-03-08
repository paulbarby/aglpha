class Animation:
    def __init__(self, id, object_id, animation_state, frames, duration, loop=True):
        self.id = id
        self.object_id = object_id            # Reference to the associated game object (unit, city, etc.)
        self.animation_state = animation_state  # From AnimationState enum
        self.frames = frames                  # List of image frames
        self.duration = duration              # Total duration of the animation
        self.current_frame = 0
        self.loop = loop

    def update(self, delta_time):
        # Update the current frame based on elapsed time (delta_time)
        pass