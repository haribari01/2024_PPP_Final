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

#버튼 클래스
class Button:
    def __init__(self, x, y, width, height, text=None, text_color=None, button_color=None, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.image = image
        self.font = pygame.font.Font(None, 40)
    #버튼 그리기
    def draw(self, screen):
            pygame.draw.rect(screen, self.button_color, self.rect)
            text_surf = self.font.render(self.text, True, self.text_color) #render 하면 text가 이미지화 됨
            text_rect = text_surf.get_rect(center=self.rect.center) #get.rect는 (center, topleft - 위치 / 크기)
            screen.blit(text_surf, text_rect)
    # 버튼 클릭
    def click(self, pos):
        return self.rect.collidepoint(pos)  #pos는 (x,y) collidepoint는 해당영역에 pos가 있으면 True반환

# 버튼 기본 세팅
button_width = 200
button_height = 50
button_x = (screen.get_width() - button_width) // 2
#[클래스 사용해서 버튼 생성하기]
button1 = Button(button_x, 400, button_width, button_height, "Graph", (255, 105, 180), (255, 192, 203))
button2 = Button(button_x, 500, button_width, button_height, "Forecast", (255, 105, 180), (255, 192, 203))
button3 = Button(button_x, 600, button_width, button_height, "Date", (255, 105, 180), (255, 192, 203))

running = True # 게임이 진행중인지 확인하기
while running:
    for event in pygame.event.get(): # running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는지
            running = False # 게임이 진행중이 아님
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()  # 마우스의 포지션(위치) x, y 값을 튜플로 반환한다.
            if button1.click(pos):
                print("버튼 1 클릭")
            elif button2.click(pos):
                print("버튼 2 클릭")
            elif button3.click(pos):
                print("버튼 3 클릭")

    screen.blit(background, (0, 0)) # 배경 그리기(background 가 표시되는 위치) (0,0 은 좌측상단)

    # 텍스트
    text_rect = text.get_rect(center=(screen.get_width() // 2, 250))  #텍스트 위치
    screen.blit(text, text_rect)  # 이게 그리는거임 text 를 text_rect 위치로

    button1.draw(screen)
    button2.draw(screen)
    button3.draw(screen)

    pygame.display.update()  # 게임화면을 지속적으로 그리기(for문도는동안 계속)

pygame.quit()