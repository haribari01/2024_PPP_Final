import pygame
import random

# Pygame 초기화
pygame.init()

#메인화면 크기 설정
screen = pygame.display.set_mode((533, 800))
screen_width, screen_height = 533, 800
pygame.display.set_caption('벚꽃 보러 갈래?')

#메인 배경화면
background = pygame.image.load('cherry_blossom.jpg')
background_rect = pygame.transform.scale(background, (533, 800))  #크기 커졌다가 다시 돌아갈 때 사용

# 벚꽃잎 이미지
cherry_blossom_img = pygame.image.load('small_cherry_blossom.png')
cherry_blossom_img = pygame.transform.scale(cherry_blossom_img, (30, 30))

# 벚꽃잎 객체 정의
class CherryPetals:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-100, 0)  # 화면 상단 부근에서 시작 ->  뭉탱이로 떨어짐. (짜침)
        self.speed = random.uniform(0.2, 0.3)  # 떨어지는 속도 랜덤 설정 (수정된 부분)
        self.rotation = random.randint(0, 15)  # 벚꽃잎 회전
        # self.rotation_speed = random.randint(0.01, 0.02)
        #random.randint는 정수받아야함    random.uniform => float
        self.rotation_speed = random.uniform(0.1, 0.2)

    def update(self):
        self.y += self.speed
        self.rotation = (self.rotation + self.rotation_speed) % 360  #떨어지는 동안 회전 (360넘지 않게 세팅하라는데 별 차이 못느낌)

        # 화면을 벗어난 벚꽃잎은 화면 상단에서 재사용
        if self.y > screen_height:
            self.x = random.randint(0, screen_width)
            self.y = random.randint(-100, 0)
            self.speed = random.uniform(0.2, 0.3)
            self.rotation = random.randint(0, 15)
            self.rotation_speed = random.uniform(0.1, 0.2)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(cherry_blossom_img, self.rotation)
        screen.blit(rotated_image, (self.x, self.y))

# 벚꽃잎 객체 리스트 생성
petals = []
for _ in range(100):  # 100개의 벚꽃잎 생성
    petals.append(CherryPetals())

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))  # 배경 그리기

    # 벚꽃잎 업데이트 및 그리기
    for petal in petals:
        petal.update()
        petal.draw(screen)

    pygame.display.update()

pygame.quit()
