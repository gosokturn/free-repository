class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y, world_width, world_height):

        self.x = target_x - self.screen_width // 2
        self.y = target_y - self.screen_height // 2

        self.x = max(0, min(self.x, world_width - self.screen_width))
        self.y = max(0, min(self.y, world_height - self.screen_height))

    def apply(self, x, y):
        return x - self.x, y - self.y
