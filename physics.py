import math

ACCEL = 0.25
BRAKE = 0.18
MAX_FORWARD = 9.0
MAX_REVERSE = -3.0

FRICTION = 0.04
ROLLING = 0.985

STEER = 2.6
DRIFT_STEER = 4.2

SIDE_GRIP = 0.20
DRIFT_GRIP = 0.05

BOOST_POWER = 1.65
BOOST_COST = 0.55
BOOST_RECOVER = 0.12


class PhysicsEngine:

    def __init__(self, kart):
        self.kart = kart

    def update(self):

        self.apply_engine()
        self.apply_rotation()
        self.apply_velocity()
        self.apply_friction()
        self.apply_boost()
        self.move()

    def apply_engine(self):

        if self.kart.accelerating:
            self.kart.speed += ACCEL

        if self.kart.braking:
            self.kart.speed -= BRAKE

        self.kart.speed = max(
            MAX_REVERSE,
            min(MAX_FORWARD, self.kart.speed)
        )

    def apply_rotation(self):

        if abs(self.kart.speed) < 0.05:
            return

        steer = DRIFT_STEER if self.kart.drift else STEER

        direction = 1 if self.kart.speed >= 0 else -1

        if self.kart.left:
            self.kart.angle += steer * direction

        if self.kart.right:
            self.kart.angle -= steer * direction

    def apply_velocity(self):

        angle = math.radians(self.kart.angle)

        forward_x = math.sin(angle)
        forward_y = math.cos(angle)

        target_vx = forward_x * self.kart.speed
        target_vy = -forward_y * self.kart.speed

        grip = DRIFT_GRIP if self.kart.drift else SIDE_GRIP

        self.kart.vx += (target_vx - self.kart.vx) * (1 - grip)
        self.kart.vy += (target_vy - self.kart.vy) * (1 - grip)

    def apply_friction(self):

        self.kart.vx *= ROLLING
        self.kart.vy *= ROLLING

        if not self.kart.accelerating:
            self.kart.speed *= (1 - FRICTION)

        if abs(self.kart.speed) < 0.02:
            self.kart.speed = 0

    def apply_boost(self):

        if self.kart.boost and self.kart.nitro > 0:

            angle = math.radians(self.kart.angle)

            self.kart.vx += math.sin(angle) * BOOST_POWER
            self.kart.vy -= math.cos(angle) * BOOST_POWER

            self.kart.nitro -= BOOST_COST

        else:

            self.kart.nitro = min(
                100,
                self.kart.nitro + BOOST_RECOVER
            )

    def move(self):

        self.kart.x += self.kart.vx
        self.kart.y += self.kart.vy

    def bounce(self, width, height):

        margin = 18

        if self.kart.x < margin:
            self.kart.x = margin
            self.kart.vx *= -0.35

        if self.kart.x > width - margin:
            self.kart.x = width - margin
            self.kart.vx *= -0.35

        if self.kart.y < margin:
            self.kart.y = margin
            self.kart.vy *= -0.35

        if self.kart.y > height - margin:
            self.kart.y = height - margin
            self.kart.vy *= -0.35

    def drift_charge(self):

        if self.kart.drift and abs(self.kart.speed) > 4:

            self.kart.drift_time += 1

            if self.kart.drift_time % 5 == 0:
                self.kart.nitro = min(
                    100,
                    self.kart.nitro + 0.35
                )

        else:

            self.kart.drift_time = 0
