import streamlit as st
import pygame
import numpy as np

from kart import Kart
from track import Track
from ai import AIKart
from ui import GameUI
from camera import Camera

# ==========================
# 게임 설정
# ==========================
WIDTH = 3000
HEIGHT = 3000
WORLD_WIDTH = 3000
WORLD_HEIGHT = 3000

FPS = 60
MAX_LAP = 3

pygame.init()
pygame.font.init()

screen = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

st.set_page_config(
    page_title="Kart Style Racing",
    page_icon="🏎️",
    layout="wide"
)

st.title("🏎️ Kart Style Racing")
frame = st.empty()

# ==========================
# 게임 객체 생성
# ==========================
track = Track(WIDTH, HEIGHT)
ui = GameUI(WIDTH, HEIGHT)
camera = Camera(WIDTH, HEIGHT)

player = Kart(600, 1500)

# AI가 따라가는 체크포인트
checkpoints = [
    (600,300),
    (1500,250),
    (2400,500),
    (2700,1500),
    (2400,2500),
    (1500,2700),
    (600,2500),
    (300,1500)
]

# AI 카트 색상
colors = [
    (0, 150, 255),
    (255, 200, 0),
    (0, 255, 120),
    (255, 0, 180),
    (180, 120, 255),
    (255, 120, 40),
    (40, 255, 255)
]

ai_karts = []

for i in range(7):
    ai_karts.append(
        AIKart(
            600 - i*30,
            1500 + i*28,
            colors[i]
        )
    )

lap = 1
finish = False

font = pygame.font.SysFont("malgungothic", 22)
big_font = pygame.font.SysFont("malgungothic", 60, bold=True)

# ==========================
# 게임 루프
# ==========================
running = True

while running:

    clock.tick(FPS)

    previous_position = (player.x, player.y)

    # ----------------------
    # 이벤트 처리
    # ----------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ----------------------
    # 플레이어 업데이트
    # ----------------------
    if not finish:

        player.handle_input(keys)
        player.update(WORLD_WIDTH, WORLD_HEIGHT)

        track.apply_collision(player)
        track.apply_boost(player)

        # 카메라 위치 갱신
        camera.update(
            player.x,
            player.y,
            WORLD_WIDTH,
            WORLD_HEIGHT
        )

        # AI 업데이트
        for ai in ai_karts:
            ai.update_ai(
                checkpoints,
                track,
                WORLD_WIDTH,
                WORLD_HEIGHT
            )

        # 랩 체크
        if track.crossed_start(
            previous_position,
            (player.x, player.y)
        ):
            lap += 1

            if lap > MAX_LAP:
                lap = MAX_LAP
                finish = True

    # ----------------------
    # 순위 계산
    # ----------------------
    racers = [player] + ai_karts

    ranking = sorted(
        racers,
        key=lambda kart: (kart.x, -kart.y),
        reverse=True
    )

    player_rank = ranking.index(player) + 1

    # ----------------------
    # UI 업데이트
    # ----------------------
    ui.update()

    # ----------------------
    # 화면 그리기
    # ----------------------
   track.draw(screen, camera)

   for ai in ai_karts:
    ai.draw(screen, camera)

player.draw(screen, camera)

    ui.draw_speedometer(screen, player.speed_kmh())
    ui.draw_nitro(screen, player.nitro)
    ui.draw_lap(screen, lap, MAX_LAP)
    ui.draw_rank(screen, player_rank, len(racers))
    ui.draw_timer(screen)
    ui.draw_minimap(screen, player, ai_karts)
    ui.draw_countdown(screen)

    # ----------------------
    # 조작법 표시
    # ----------------------
    controls = [
        "W / ↑ : 가속",
        "S / ↓ : 브레이크",
        "A,D / ←→ : 조향",
        "Shift : 드리프트",
        "Left Ctrl : 니트로"
    ]

    y = HEIGHT - 110

    for text in controls:
        img = font.render(text, True, (255, 255, 255))
        screen.blit(img, (20, y))
        y += 22

    # ----------------------
    # 경기 종료 화면
    # ----------------------
    if finish:

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        finish_text = big_font.render(
            "FINISH!",
            True,
            (255, 255, 255)
        )

        rank_text = font.render(
            f"최종 순위 : {player_rank}/8",
            True,
            (255, 255, 255)
        )

        restart_text = font.render(
            "R : 다시 시작    ESC : 종료",
            True,
            (255, 255, 255)
        )

        screen.blit(
            finish_text,
            finish_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 30)
            )
        )

        screen.blit(
            rank_text,
            rank_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 40)
            )
        )

        screen.blit(
            restart_text,
            restart_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 80)
            )
        )

        if keys[pygame.K_r]:

            player.reset(150, 260)

            ai_karts = []
            for i in range(7):
                ai_karts.append(
                    AIKart(
                        150 - i * 18,
                        260 + i * 16,
                        colors[i]
                    )
                )

            lap = 1
            finish = False
            ui = GameUI(WIDTH, HEIGHT)

        if keys[pygame.K_ESCAPE]:
            running = False

    # ----------------------
    # Streamlit 출력
    # ----------------------
    img = pygame.surfarray.array3d(screen)
    img = np.transpose(img, (1, 0, 2))

    frame.image(img, channels="RGB")

pygame.quit()
