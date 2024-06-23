import pygame
import os
import requests
import matplotlib.pyplot as plt
import csv

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


#데이터 다운로드
def download(filename, URL):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8-sig") as f:
            res = requests.get(URL)
            f.write(res.text.replace("\r", ""))
#데이터 읽기
def read_col(filename, col_idx):
    dataset = []
    with open(filename, encoding="utf-8-sig") as f:
        lines = f.readlines()
        for line in lines[8:]:
            tokens = line.strip().split(",")
            if len(tokens) > col_idx and tokens[col_idx] != '':
                dataset.append(float(tokens[col_idx]))
            else:
                dataset.append(None)
    return dataset

def read_col_str(filename, col_idx):
    dataset = []
    with open(filename, encoding="utf-8-sig") as f:
        lines = f.readlines()
        for line in lines[8:]:
            tokens = line.strip().split(",")
            if tokens[col_idx] != '':
                dataset.append(tokens[col_idx])
            else:
                dataset.append(None)
    return dataset

def degree_600(tmax, dates, threshold, year):
    accum_temp = 0
    total_days = 0

    for temp, date in zip(tmax, dates):
        date_year = int(date.split('-')[0])    # date.split('-')은 ['2024', '06', '30'] 형태의 리스트
        date_month = int(date.split('-')[1])
        if date_year == year and date_month >= 2:
            total_days += 1
            if temp is not None:
                accum_temp += temp
            if accum_temp >= threshold:
                break                          # 초기화 하고 다시 계산
    return total_days

def degree_600_graph(start_year, end_year, tmax, dates):
    output_csv = "degree_600.csv"
    if os.path.exists(output_csv):
        # print(f"{output_csv} 이미 있음.")
        return   #이거 안하면 딜레이 후 실행됨.  이코드는 그냥 딜레이 없애주려고 넣은 코드임. 파일 다운과 무관함.

    threshold = 600
    years = []
    days = []

    for year in range(start_year, end_year + 1):
        accum_days = degree_600(tmax, dates, threshold, year)
        years.append(year)
        days.append(accum_days)

    with open('degree_600.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'total_day'])  #한줄 쓰는 작업
        for year, day in zip(years, days):
            writer.writerow([year, day])

    plt.rcParams['font.family'] = ['NanumGothic']
    plt.figure(figsize=(10, 6))                                        # 10 * 6 인치 그래프
    plt.plot(years, days, marker='o', linestyle='-', color='m')  # marker : 데이터 o로 표현 / '-'는 선으로 표현 )
    plt.title('<2월 1일부터 누적 최고 기온이 600을 넘는 날짜>')
    plt.xlabel('연도')
    plt.ylabel('누적 날짜 수 (일)')
    plt.grid(True)                                                     #가로, 세로 격자 추가
    plt.xticks(range(start_year, end_year + 1, 5))                     # 5년 단위로 눈금 설정
    plt.tight_layout()                                                 #간격 최적화
    plt.show()
    plt.savefig('degree_600.png', dpi=300, bbox_inches='tight')  #bbox_inches='tight : 불필요한 여백제거
    plt.close()

# 그래프 이미지를 로드
def load_graph(filename):
    graph_img = pygame.image.load(filename)
    return pygame.transform.scale(graph_img, (1000, 630))

def main():
    global screen
    global background

    start_year = 1919
    end_year = 2024

    URL = (f"https://data.kma.go.kr/stcs/grnd/downloadGrndTaList.do?fileType=csv&pgmNo=70&menuNo=432&serviceSe=F00101&stdrMg=99999&startDt={start_year}0101&endDt={end_year}0531&taElement=MIN&taElement=AVG&taElement=MAX&stnGroupSns=&selectType=1&mddlClssCd=SFC01&dataFormCd=F00501&dataTypeCd=standard&startDay={start_year}0101&startYear={start_year}&endDay={end_year}0531&endYear={end_year}&startMonth=01&endMonth=12&sesnCd=0&txtStnNm=%EC%A0%84%EC%A3%BC&stnId=146&areaId=&gFontSize=")
    filename = "weather(146)_1919-2024.csv"
    download(filename, URL)

    dates = read_col_str(filename, 0)
    tmax = read_col(filename, 4)

    # 이벤트루프
    running = True  # 게임이 진행중인지 확인하기
    show_text = True
    show_graph = False


    while running:
        for event in pygame.event.get(): # running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
            if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는지
                running = False # 게임이 진행중이 아님
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # 마우스의 포지션(위치) x, y 값을 튜플로 반환한다.
                if button1.click(pos):
                    print("버튼 1 클릭")
                    degree_600_graph(start_year, end_year, tmax, dates)
                    graph_img = load_graph('degree_600.png')
                    pygame.display.set_caption('Graph')  # 창 제목
                    show_text = False
                    show_graph = True
                elif button2.click(pos):
                    print("버튼 2 클릭")
                elif button3.click(pos):
                    print("버튼 3 클릭")

        screen.blit(background, (0, 0)) # 배경 그리기(background 가 표시되는 위치) (0,0 은 좌측상단)

        if show_graph:
            graph_rect = graph_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
            screen.blit(graph_img, graph_rect)

        else:
            if show_text:
                # 메인화면 텍스트를 위치 조절
                text_rect = text.get_rect(center=(screen.get_width() // 2, 250))
                screen.blit(text, text_rect)
                # 버튼그리기
                button1.draw(screen)
                button2.draw(screen)
                button3.draw(screen)

        pygame.display.update()  # 게임화면을 지속적으로 그리기(for문도는동안 계속)

    pygame.quit()

if __name__ == '__main__':
    main()