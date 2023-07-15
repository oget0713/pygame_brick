import pygame
from pygame.locals import *
import random
import sys

# 게임 화면 설정
screen_size = {
    'width': 800,
    'height': 500
}

FPS = 60

# 색깔 설정
Green = (127,255,0)
White = (255,255,255)
Gray = (222,226,230)


# 초기화
pygame.init()
screen = pygame.display.set_mode((screen_size['width'], screen_size['height']))
pygame.display.set_caption("벽돌깨기")
clock = pygame.time.Clock()

# Font 객체 생성

myFont = pygame.font.SysFont("arial", 30, True, False)

# Text를 surface에 그리기, 안티알리어싱, 검은색

text_Title = myFont.render("Press Any Key To START", True, White)

# Rect 생성

text_Rect = text_Title.get_rect()

# 가로 가운데, 세로 50 위치

text_Rect.centerx = screen_size['width'] // 2

text_Rect.y = screen_size['height'] // 2

# Text Surface SCREEN에 복사하기, Rect 사용

screen.blit(text_Title, text_Rect)

# 패들 설정
paddle_width = 80
paddle_height = 10
paddle_x = screen_size['width'] // 2 - paddle_width // 2
paddle_y = screen_size['height'] - paddle_height - 5
paddle_speed = 8

# 공 설정
ball_radius = 7
ball_x = screen_size['width'] // 2
ball_y = screen_size['height'] - paddle_height - 40
ball_speed_x = random.choice([-3, 3])
ball_speed_y = -3

# 벽돌 설정
brick_width = 60
brick_height = 20
brick_gap = 5
brick_rows = 5
brick_cols = 10

#screen_size['width'] /
# 벽돌 생성
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = (screen_size['width'] - (brick_cols * (brick_width + brick_gap))) // 2 + col * (brick_width + brick_gap)
        brick_y = row * (brick_height + brick_gap) + 50
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

running = True
game_started = False
# 게임 루프
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 키 입력 감지
            game_started = True

    if game_started:
        # 패들 이동
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            paddle_x -= paddle_speed
        if keys[K_RIGHT]:
            paddle_x += paddle_speed

        # 패들과 벽 충돌 검사
        if paddle_x < 0:
            paddle_x = 0
        if paddle_x > screen_size['width'] - paddle_width:
            paddle_x = screen_size['width'] - paddle_width

        # 벽돌과 충돌 검사
        for brick in bricks:
            if brick.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                bricks.remove(brick)
                ball_speed_y *= -1

        # 패들과 충돌 검사
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if paddle_rect.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
            ball_speed_y *= -1

        # 공 이동
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # 벽과 충돌 검사
        if ball_x - ball_radius < 0 or ball_x + ball_radius > screen_size['width']:
            ball_speed_x *= -1
        if ball_y - ball_radius < 0:
            ball_speed_y *= -1

        # 화면 업데이트
        screen.fill((0, 0, 0))

        # 바닥에 닿으면 게임 종료
        if ball_y + ball_radius > screen_size['height']:
            #pygame.quit()
            #continue
            running = False
            #game_started = False

    # 벽돌 그리기
    for brick in bricks:
        pygame.draw.rect(screen, Gray, brick)

    # 패들 그리기
    pygame.draw.rect(screen, White, (paddle_x, paddle_y, paddle_width, paddle_height))

    # 공 그리기
    pygame.draw.circle(screen, Green, (ball_x, ball_y), ball_radius)

    pygame.display.flip()

#running = True
pygame.quit()
