import pygame
import math


ROAD = (70, 70, 70)
GRASS = (120, 180, 80)
WALL = (220, 220, 220)
START = (255, 255, 255)
BOOST = (0, 200, 255)


class Track:

    def __init__(self, width, height):

        self.width = 3000
self.height = 3000

self.surface = pygame.Surface((self.width, self.height))
self.mask = pygame.Surface((self.width, self.height))


        self.start_rect = pygame.Rect(120, 235, 12, 70)
        self.boost_pads = []

        self.create()

    def create(self):

    self.surface.fill(GRASS)
    self.mask.fill((0,0,0))

    pygame.draw.rect(
        self.surface,
        ROAD,
        (200,200,2600,2600),
        border_radius=250
    )

    pygame.draw.rect(
        self.mask,
        (255,255,255),
        (200,200,2600,2600),
        border_radius=250
    )

    pygame.draw.rect(
        self.surface,
        GRASS,
        (700,700,1600,1600),
        border_radius=180
    )

    pygame.draw.rect(
        self.mask,
        (0,0,0),
        (700,700,1600,1600),
        border_radius=180
    )

    self.start_rect = pygame.Rect(600,1450,15,120)

    pygame.draw.rect(
        self.surface,
        START,
        self.start_rect
    )

    self.boost_pads = [
        pygame.Rect(1450,250,120,30),
        pygame.Rect(1450,2720,120,30),
        pygame.Rect(250,1450,30,120),
        pygame.Rect(2720,1450,30,120),
    ]

    for pad in self.boost_pads:
        pygame.draw.rect(
            self.surface,
            BOOST,
            pad,
            border_radius=8
        )

   def draw(self, screen, camera):

    screen.blit(
        self.surface,
        (-camera.x, -camera.y)
    )

        ix = int(x)
        iy = int(y)

        if ix < 0 or iy < 0 or ix >= self.width or iy >= self.height:
            return False

        color = self.mask.get_at((ix, iy))
        return color.r > 200

    def apply_collision(self, kart):

        wheel_distance = 12

        rad = math.radians(kart.angle)

        front_x = kart.x + math.sin(rad) * wheel_distance
        front_y = kart.y - math.cos(rad) * wheel_distance

        back_x = kart.x - math.sin(rad) * wheel_distance
        back_y = kart.y + math.cos(rad) * wheel_distance

        front_ok = self.on_road(front_x, front_y)
        back_ok = self.on_road(back_x, back_y)

        if front_ok and back_ok:
            return

        kart.vx *= -0.35
        kart.vy *= -0.35
        kart.speed *= 0.45

        kart.x += kart.vx * 2
        kart.y += kart.vy * 2

    def apply_boost(self, kart):

        point = (int(kart.x), int(kart.y))

        for pad in self.boost_pads:
            if pad.collidepoint(point):

                angle = math.radians(kart.angle)

                kart.vx += math.sin(angle) * 3.2
                kart.vy -= math.cos(angle) * 3.2

                kart.speed += 1.8

    def crossed_start(self, previous_pos, current_pos):

        x1, y1 = previous_pos
        x2, y2 = current_pos

        if self.start_rect.collidepoint(int(x2), int(y2)):
            if x1 > self.start_rect.centerx >= x2:
                return True

        return False
