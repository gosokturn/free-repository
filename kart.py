import pygame
import math
from physics import PhysicsEngine


class Kart:

    WIDTH = 34
    HEIGHT = 18

    def __init__(self, x, y, color=(255, 60, 60)):

        self.x = float(x)
        self.y = float(y)

        self.angle = 0.0

        self.speed = 0.0
        self.vx = 0.0
        self.vy = 0.0

        self.accelerating = False
        self.braking = False
        self.left = False
        self.right = False

        self.drift = False
        self.boost = False

        self.nitro = 100.0
        self.drift_time = 0

        self.color = color

        self.physics = PhysicsEngine(self)

    def update(self, width, height):

        self.physics.update()
        self.physics.bounce(width, height)
        self.physics.drift_charge()

    def handle_input(self, keys):

        self.accelerating = keys[pygame.K_UP] or keys[pygame.K_w]
        self.braking = keys[pygame.K_DOWN] or keys[pygame.K_s]

        self.left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        self.drift = keys[pygame.K_LSHIFT]
        self.boost = keys[pygame.K_LCTRL]

    def draw(self, surface, camera):

    kart = pygame.Surface(
        (self.WIDTH, self.HEIGHT),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        kart,
        self.color,
        (0,0,self.WIDTH,self.HEIGHT),
        border_radius=6
    )

    pygame.draw.rect(kart,(25,25,25),(3,2,8,14),border_radius=3)
    pygame.draw.rect(kart,(25,25,25),(23,2,8,14),border_radius=3)

    pygame.draw.rect(kart,(180,220,255),(9,4,16,10),border_radius=3)

    rotated = pygame.transform.rotate(kart,self.angle)

    draw_x, draw_y = camera.apply(self.x,self.y)

    rect = rotated.get_rect(center=(draw_x,draw_y))
    surface.blit(rotated,rect)

    if self.drift and abs(self.speed) > 4:
        self.draw_skid(surface,camera)

    def draw_skid(self,surface,camera):

    import math

    rad = math.radians(self.angle)

    back_x = self.x - math.sin(rad)*10
    back_y = self.y + math.cos(rad)*10

    left_x = back_x + math.cos(rad)*6
    left_y = back_y + math.sin(rad)*6

    right_x = back_x - math.cos(rad)*6
    right_y = back_y - math.sin(rad)*6

    lx,ly = camera.apply(left_x,left_y)
    rx,ry = camera.apply(right_x,right_y)

    pygame.draw.circle(surface,(35,35,35),(int(lx),int(ly)),2)
    pygame.draw.circle(surface,(35,35,35),(int(rx),int(ry)),2)

    def speed_kmh(self):

        return int(abs(self.speed) * 22)

    def reset(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.angle = 0
        self.speed = 0

        self.vx = 0
        self.vy = 0

        self.nitro = 100
        self.drift_time = 0
