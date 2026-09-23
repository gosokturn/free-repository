import math
import random
from kart import Kart


class AIKart(Kart):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)

        self.speed = random.uniform(5.2, 6.5)
        self.max_speed = random.uniform(6.5, 8.0)
        self.target = 0

    def update_ai(self, checkpoints, track, width, height):

        tx, ty = checkpoints[self.target]

        dx = tx - self.x
        dy = ty - self.y

        target_angle = math.degrees(math.atan2(dx, -dy))

        diff = (target_angle - self.angle + 180) % 360 - 180

        self.left = diff > 3
        self.right = diff < -3

        self.accelerating = True
        self.braking = False

        if abs(diff) > 35:
            self.drift = True
        else:
            self.drift = False

        self.boost = False

        if self.speed < self.max_speed:
            self.speed += 0.03

        super().update(width, height)

        track.apply_collision(self)
        track.apply_boost(self)

        if math.hypot(dx, dy) < 35:
            self.target = (self.target + 1) % len(checkpoints)
