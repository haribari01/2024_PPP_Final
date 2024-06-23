import pygame

pygame.init()     #초기화 해줘야함  (무조건)

#메인화면 크기 설정
screen = pygame.display.set_mode((533, 800))
pygame.display.set_caption('벚꽃 보러 갈래?')
#메인 배경화면
background = pygame.image.load('cherry_blossom.jpg')
#메인 폰트
font = pygame.font.Font(None, 70)
text = font.render('Cherry Blossom', True, (255, 105, 180))

running = True # 게임이 진행중인지 확인하기
while running:
    for event in pygame.event.get(): # running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는지
            running = False # 게임이 진행중이 아님

    screen.blit(background, (0, 0)) # 배경 그리기(background 가 표시되는 위치) (0,0 은 좌측상단)

    # 텍스트 
    text_rect = text.get_rect(center=(screen.get_width() // 2, 250))  #텍스트 위치
    screen.blit(text, text_rect)  # 이게 그리는거임 text 를 text_rect 위치로

    pygame.display.update()  # 게임화면을 지속적으로 그리기(for문도는동안 계속)

pygame.quit()