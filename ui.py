import pygame
import math
import time


class GameUI:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("malgungothic", 24)
        self.big = pygame.font.SysFont("malgungothic", 72, bold=True)
        self.small = pygame.font.SysFont("malgungothic", 18)

        self.start_time = time.time()
        self.countdown = 3

    def update(self):

        elapsed = time.time() - self.start_time
        self.countdown = max(0, 3 - int(elapsed))

    def race_time(self):

        t = time.time() - self.start_time
        minute = int(t // 60)
        second = int(t % 60)
        ms = int((t * 100) % 100)

        return f"{minute:02d}:{second:02d}.{ms:02d}"

    def draw_speedometer(self, screen, speed):

        cx = self.width - 120
        cy = self.height - 120
        radius = 70

        pygame.draw.circle(screen, (35,35,35), (cx,cy), radius)
        pygame.draw.circle(screen, (110,110,110), (cx,cy), radius, 5)

        for i in range(0,181,15):

            ang = math.radians(180-i)

            x1 = cx + math.cos(ang)*(radius-5)
            y1 = cy + math.sin(ang)*(radius-5)

            x2 = cx + math.cos(ang)*(radius-15)
            y2 = cy + math.sin(ang)*(radius-15)

            pygame.draw.line(screen,(230,230,230),(x1,y1),(x2,y2),2)

        meter = min(speed,200)/200*180
        ang = math.radians(180-meter)

        x = cx + math.cos(ang)*(radius-18)
        y = cy + math.sin(ang)*(radius-18)

        pygame.draw.line(screen,(255,60,60),(cx,cy),(x,y),4)
        pygame.draw.circle(screen,(255,255,255),(cx,cy),6)

        txt = self.font.render(f"{speed} km/h",True,(255,255,255))
        screen.blit(txt, txt.get_rect(center=(cx,cy+42)))

    def draw_nitro(self, screen, value):

        x = 20
        y = self.height - 50

        pygame.draw.rect(screen,(40,40,40),(x,y,220,20),border_radius=8)
        pygame.draw.rect(screen,(0,255,255),(x,y,int(value*2.2),20),border_radius=8)

        txt = self.small.render("NITRO",True,(255,255,255))
        screen.blit(txt,(x,y-22))

    def draw_lap(self, screen, lap, maxlap):

        txt = self.font.render(
            f"LAP {lap}/{maxlap}",
            True,
            (255,255,0)
        )
        screen.blit(txt,(20,15))

    def draw_rank(self, screen, rank, total):

        txt = self.font.render(
            f"순위 {rank}/{total}",
            True,
            (255,255,255)
        )
        screen.blit(txt,(20,48))

    def draw_timer(self, screen):

        txt = self.font.render(
            self.race_time(),
            True,
            (255,255,255)
        )

        screen.blit(
            txt,
            txt.get_rect(center=(self.width//2,24))
        )

    def draw_countdown(self, screen):

        if self.countdown > 0:

            text = str(self.countdown)

        else:

            if time.time()-self.start_time < 4:
                text = "GO!"
            else:
                return

        color = (255,255,255)

        if text == "GO!":
            color = (0,255,120)

        img = self.big.render(text,True,color)

        screen.blit(
            img,
            img.get_rect(center=(self.width//2,self.height//2))
        )

    def draw_minimap(self, screen, player, ai_list):

        map_size = 170
        px = self.width - map_size - 15
        py = 15

        pygame.draw.rect(
            screen,
            (20,20,20),
            (px,py,map_size,map_size),
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (120,120,120),
            (px+10,py+10,map_size-20,map_size-20),
            width=2,
            border_radius=8
        )

        def convert(x,y):

    mx = px + 10 + x/3000*(map_size-20)
    my = py + 10 + y/3000*(map_size-20)

    return int(mx), int(my)

        pygame.draw.circle(
            screen,
            (255,60,60),
            convert(player.x,player.y),
            5
        )

        for ai in ai_list:

            pygame.draw.circle(
                screen,
                ai.color,
                convert(ai.x,ai.y),
                4
            )

        title = self.small.render("MINIMAP",True,(255,255,255))
        screen.blit(title,(px+8,py-18))
