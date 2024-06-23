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
background_rect = pygame.transform.scale(background, (533, 800))  #특정 크기로 변환
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
        if self.image:
            screen.blit(self.image, self.rect.topleft)   #이미지복사 : screen.blit(복사할 이미지, 복사할대상)
        else:
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
# 화살표 버튼
arrow_img = pygame.image.load('arrow.png')
arrow_img = pygame.transform.scale(arrow_img, (50, 50))
back_button = Button(7, 7, 50, 50, image=arrow_img)
# 목록 버튼
graph_list_button = Button(900, 7, 80, 50, "List", (0, 0, 0), (255, 255, 255))
# 그래프 선택 버튼
graph1_button = Button(840, 70, 150, 35, "600", (255, 255, 255), (255, 192, 203))
graph2_button = Button(840, 110, 150, 35, "5.5 Tavg", (255, 255, 255), (255, 192, 203))
graph3_button = Button(840, 150, 150, 35, "5.5 GDD", (255, 255, 255), (255, 192, 203))
graph4_button = Button(840, 190, 150, 35, "0.74 Tavg", (255, 255, 255), (255, 192, 203))
graph5_button = Button(840, 230, 150, 35, "0.74 GDD", (255, 255, 255), (255, 192, 203))

graph6_button = Button(840, 70, 150, 35, "2023", (255, 255, 255), (255, 192, 203))
graph7_button = Button(840, 110, 150, 35, "2024", (255, 255, 255), (255, 192, 203))
graph8_button = Button(840, 150, 150, 35, "2025", (255, 255, 255), (255, 192, 203))

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

def gdd_ver1(tavg, dates, ref_temp, threshold, year):
    total_gdd = 0
    accum_days = 0

    for temp, date in zip(tavg, dates):
        date_year = int(date.split('-')[0])                 # date.split('-')은 ['2024', '06', '30'] 형태의 리스트
        date_month = int(date.split('-')[1])
        if date_year == year and date_month >= 2:
            accum_days += 1
            if temp is not None:
                eff_temp = temp - ref_temp
                if eff_temp < 0:
                    eff_temp = 0
                total_gdd += eff_temp
            if total_gdd >= threshold:
                break
    return accum_days

def gdd_ver1_graph(start_year, end_year, tavg, dates):
    output_png = "5.5_tavg.csv"
    if os.path.exists(output_png):
        return

    ref_temp = 5.5
    threshold = 106.2
    years = []
    days = []

    for year in range(start_year, end_year + 1):
        accum_days = gdd_ver1(tavg, dates, ref_temp, threshold, year)
        years.append(year)
        days.append(accum_days)

    with open('5.5_tavg.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'total_day'])
        for year, day in zip(years, days):
            writer.writerow([year, day])

    plt.rcParams['font.family'] = ['NanumGothic']
    plt.figure(figsize=(10, 6))
    plt.plot(years, days, marker='o', linestyle='-')
    plt.title('<2월 1일부터 누적 일평균온도가 106.2를 넘는 날짜> - 기준온도 5.5')
    plt.xlabel('연도')
    plt.ylabel('누적 날짜 수 (일)')
    plt.grid(True)
    plt.xticks(range(start_year, end_year + 1, 5))
    plt.tight_layout()
    plt.savefig('5.5_tavg.png', dpi=300, bbox_inches='tight')
    plt.close()

def gdd_ver1_graph_2(start_year, end_year, tgdd, dates):
    output_png = "5.5_GDD.csv"
    if os.path.exists(output_png):
        return

    ref_temp = 5.5
    threshold = 106.2
    years = []
    days = []

    for year in range(start_year, end_year + 1):
        accum_days = gdd_ver1(tgdd, dates, ref_temp, threshold, year)
        years.append(year)
        days.append(accum_days)

    with open('5.5_GDD.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'total_day'])
        for year, day in zip(years, days):
            writer.writerow([year, day])

    plt.rcParams['font.family'] = ['NanumGothic']
    plt.figure(figsize=(10, 6))
    plt.plot(years, days, marker='o', linestyle='--')
    plt.title('<2월 1일부터 누적 GDD가 106.2를 넘는 날짜> - 기준온도 5.5')
    plt.xlabel('연도')
    plt.ylabel('누적 날짜 수 (일)')
    plt.grid(True)
    plt.xticks(range(start_year, end_year + 1, 5))
    plt.tight_layout()
    plt.savefig('5.5_GDD.png', dpi=300, bbox_inches='tight')
    plt.close()

def gdd_ver2(tavg, dates, ref_temp, threshold, year):
    total_gdd = 0
    accum_days = 0

    for temp, date in zip(tavg, dates):
        date_year = int(date.split('-')[0])  # date.split('-')은 ['2024', '06', '30'] 형태의 리스트
        date_month = int(date.split('-')[1])
        date_day = int(date.split('-')[2])
        if date_year == year and (date_month > 2 or (date_month == 2 and date_day >= 27)):
            accum_days += 1
            if temp is not None:
                eff_temp = temp - ref_temp
                if eff_temp < 0:
                    eff_temp = 0
                total_gdd += eff_temp
            if total_gdd >= threshold:
                break
    return accum_days

def gdd_ver2_graph(start_year, end_year, tavg, dates):
    output_png = "0.74_tavg.csv"
    if os.path.exists(output_png):
        return

    ref_temp = 0.74
    threshold = 223.16
    years = []
    days = []

    for year in range(start_year, end_year + 1):
        accum_days = gdd_ver2(tavg, dates, ref_temp, threshold, year)
        years.append(year)
        days.append(accum_days)

    with open('0.74_tavg.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'total_day'])
        for year, day in zip(years, days):
            writer.writerow([year, day])

    plt.rcParams['font.family'] = ['NanumGothic']
    plt.figure(figsize=(10, 6))
    plt.plot(years, days, marker='o', linestyle='-', color='b')
    plt.title('<2월 27일부터 누적 일평균온도가 223.16를 넘는 날짜> - 기준온도 0.74')
    plt.xlabel('연도')
    plt.ylabel('누적 날짜 수 (일)')
    plt.grid(True)
    plt.xticks(range(start_year, end_year + 1, 5))
    plt.tight_layout()
    plt.savefig('0.74_tavg.png', dpi=300, bbox_inches='tight')
    plt.close()

def gdd_ver2_graph_2(start_year, end_year, tgdd, dates):
    output_png = "0.74_GDD.csv"
    if os.path.exists(output_png):
        return

    ref_temp = 0.74
    threshold = 223.16
    years = []
    days = []

    for year in range(start_year, end_year + 1):
        accum_days = gdd_ver2(tgdd, dates, ref_temp, threshold, year)
        years.append(year)
        days.append(accum_days)

    with open('0.74_GDD.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'total_day'])
        for year, day in zip(years, days):
            writer.writerow([year, day])

    plt.rcParams['font.family'] = ['NanumGothic']
    plt.figure(figsize=(10, 6))
    plt.plot(years, days, marker='o', linestyle='--', color='b')
    plt.title('<2월 27일부터 누적 GDD가 223.16를 넘는 날짜> - 기준온도 0.74')
    plt.xlabel('연도')
    plt.ylabel('누적 날짜 수 (일)')
    plt.grid(True)
    plt.xticks(range(start_year, end_year + 1, 5))
    plt.tight_layout()
    plt.savefig('0.74_GDD.png', dpi=300, bbox_inches='tight')
    plt.close()

def diff_check_2023():
    actual_flowering_dates = ['03-24', '03-25'] # 실제 개화일
    predicted_days = ['03-21', '03-22', '03-21', '03-23', '03-22'] # 예측 개화일

    # 날짜 범위 설정
    start_date = int(min(actual_flowering_dates).split('-')[1]) - 4
    end_date = int(max(actual_flowering_dates).split('-')[1]) + 2

    #그래프그리기
    plt.rcParams['font.family'] = ['NanumGothic']
    plt.figure(figsize=(10, 6))
    plt.ylim(end_date, start_date) # y축 범위 설정 (오름차순으로)
    # 23일부터 24일 사이 범위를 색칠 (연분홍색)  #ashspan : 수평  / asvspan : 수직
    plt.axhspan(int(actual_flowering_dates[0].split('-')[1]), int(actual_flowering_dates[1].split('-')[1]), color='magenta', alpha=0.2, label='실제 개화 시기')   #alpha : 투명도
    # 예측된 개화일 점으로 표시 (산점도 그리기)
    plt.scatter(range(1, len(predicted_days) + 1), [int(day.split('-')[1]) for day in predicted_days], color='Red', label='예측일자', s=100)   #s=100 : 점크기
    plt.xticks(range(1, len(predicted_days) + 1), ['600', '5.5_Tavg', '5.5_GDD', '0.74_Tavg', '0.74_GDD'], fontsize=12)      # x축 레이블 설정
    plt.yticks(range(start_date, end_date + 1), [f'03-{day}' for day in range(start_date, end_date + 1)])    #레이블 설정
    plt.xlabel('예측함수')
    plt.ylabel('개화일자')
    plt.title('<2023 오차범위>', fontsize=15)
    plt.grid(True)
    plt.legend(loc='lower left', fontsize='12')
    plt.tight_layout()
    plt.savefig('2023_diff.png', dpi=300, bbox_inches='tight')
    plt.close()

def diff_check_2024():
    actual_flowering_dates = ['03-23', '03-24']  # 실제 개화일
    predicted_days = ['03-24', '03-27', '03-25', '03-30', '03-28']  # 예측 개화일

    # 날짜 범위 설정
    start_date = int(min(actual_flowering_dates).split('-')[1]) - 2
    end_date = int(max(actual_flowering_dates).split('-')[1]) + 7

    # 그래프 그리기
    plt.rcParams['font.family'] = ['NanumGothic']
    plt.figure(figsize=(10, 6))
    plt.ylim(end_date, start_date)  # y축 범위 설정 (오름차순으로)
    plt.axhspan(int(actual_flowering_dates[0].split('-')[1]), int(actual_flowering_dates[1].split('-')[1]),color='magenta', alpha=0.2, label='실제 개화 시기')
    plt.scatter(range(1, len(predicted_days) + 1), [int(day.split('-')[1]) for day in predicted_days], color='Red', label='예측일자', s=100)
    plt.xticks(range(1, len(predicted_days) + 1), ['600', '5.5_Tavg', '5.5_GDD', '0.74_Tavg', '0.74_GDD'], fontsize=12)
    plt.yticks(range(start_date, end_date + 1), [f'03-{day}' for day in range(start_date, end_date + 1)])  # 레이블 설정
    plt.xlabel('예측함수')
    plt.ylabel('개화일자')
    plt.title('<2024 오차범위>', fontsize=15)
    plt.grid(True)
    plt.legend(loc='lower left', fontsize='12')
    plt.tight_layout()
    plt.savefig('2024_diff.png', dpi=300, bbox_inches='tight')
    plt.close()

def forecast_2025():
    predicted_days = ['03-27', '03-28', '03-25', '03-28', '03-26']  # 2025 예측 개화일

    # 날짜 범위 설정
    start_date = int(min(predicted_days).split('-')[1]) - 2
    end_date = int(max(predicted_days).split('-')[1]) + 2

    # 그래프 그리기
    plt.rcParams['font.family'] = ['NanumGothic']
    plt.figure(figsize=(10, 6))
    plt.ylim(end_date, start_date)  # y축 범위 설정 (오름차순으로)
    plt.axhspan(int(sorted(predicted_days)[0].split('-')[1]), int(sorted(predicted_days)[-1].split('-')[1]), color='magenta', alpha=0.2, label='예측 개화 시기')
    plt.scatter(range(1, len(predicted_days) + 1), [int(day.split('-')[1]) for day in predicted_days], color='Red', label='예측일자', s=100)
    plt.xticks(range(1, len(predicted_days) + 1), ['600', '5.5_Tavg', '5.5_GDD', '0.74_Tavg', '0.74_GDD'], fontsize=12)
    plt.yticks(range(start_date, end_date + 1), [f'03-{day}' for day in range(start_date, end_date + 1)])
    plt.xlabel('예측함수')
    plt.ylabel('개화일자')
    plt.title('<2025 예측 개화일자>', fontsize=15)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('2025_forecast.png', dpi=300, bbox_inches='tight')
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
    tavg = read_col(filename, 2)
    tmin = read_col(filename, 3)
    tmax = read_col(filename, 4)
    tgdd = [(tm + tx) / 2 if tm is not None and tx is not None else None for tm, tx in zip(tmin, tmax)]

    # 이벤트루프
    running = True  # 게임이 진행중인지 확인하기
    show_text = True  # 기본적으로 메인화면 활성
    show_graph = False  # 기본적으로 그래프화면 비활성
    show_predict = False
    menu_open = False  # 기본적으로 메뉴창 비활성

    degree_600_graph(start_year, end_year, tmax, dates)
    gdd_ver1_graph(start_year, end_year, tavg, dates)
    gdd_ver1_graph_2(start_year, end_year, tgdd, dates)
    gdd_ver2_graph(start_year, end_year, tavg, dates)
    gdd_ver2_graph_2(start_year, end_year, tgdd, dates)

    diff_check_2023()
    diff_check_2024()
    forecast_2025()

    while running:
        for event in pygame.event.get(): # running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
            if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는지
                running = False # 게임이 진행중이 아님
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # 마우스의 포지션(위치) x, y 값을 튜플로 반환한다.
                if show_graph:
                    if back_button.click(pos):
                        print("뒤로가기 버튼 클릭됨")
                        show_text = True       # 텍스트를 다시 표시하도록 설정
                        show_graph = False                                            #set_mode는 크기 설정하는 거
                        screen = pygame.display.set_mode(background_rect.get_size())  # 원래사이즈로 get_size() 폭, 높이 반환
                        background = pygame.image.load('cherry_blossom.jpg')
                        menu_open = False         # 나갈때 메뉴 닫아줘
                    elif graph_list_button.click(pos):
                        print("그래프 목록 버튼 클릭됨")
                        menu_open = not menu_open #값 반전 시켜서 True, False 반복

                    if show_graph and menu_open:
                        if graph1_button.click(pos):
                            print("그래프 1 선택됨")
                            graph_img = load_graph('degree_600.png')
                        elif graph2_button.click(pos):
                            print("그래프 2 선택됨")
                            graph_img = load_graph('5.5_tavg.png')
                        elif graph3_button.click(pos):
                            print("그래프 3 선택됨")
                            graph_img = load_graph('5.5_GDD.png')
                        elif graph4_button.click(pos):
                            print("그래프 4 선택됨")
                            graph_img = load_graph('0.74_tavg.png')
                        elif graph5_button.click(pos):
                            print("그래프 5 선택됨")
                            graph_img = load_graph('0.74_GDD.png')

                elif show_predict:
                    if back_button.click(pos):
                        print("뒤로가기 버튼 클릭됨")
                        show_text = True
                        show_predict = False
                        screen = pygame.display.set_mode(background_rect.get_size())  #원래사이즈로 get_size() 폭, 높이 반환
                        background = pygame.image.load('cherry_blossom.jpg')
                        menu_open = False
                    elif graph_list_button.click(pos):
                        print("그래프 목록 버튼 클릭됨")
                        menu_open = not menu_open      #값 반전 시켜서 True, False 반복 (토글형태)

                    if show_predict and menu_open:
                        if graph6_button.click(pos):
                            print("그래프 6 선택됨")
                            graph_img = load_graph('2023_diff.png')
                        elif graph7_button.click(pos):
                            print("그래프 7 선택됨")
                            graph_img = load_graph('2024_diff.png')
                        elif graph8_button.click(pos):
                            print("그래프 8 선택됨")
                            graph_img = load_graph('2025_forecast.png')

                if button1.click(pos):
                    print("버튼 1 클릭")
                    degree_600_graph(start_year, end_year, tmax, dates)
                    graph_img = load_graph('degree_600.png')
                    screen = pygame.display.set_mode((1000, 800))
                    background = pygame.image.load('cherry_blossom.jpg')
                    background = pygame.transform.scale(background, (1000, 800))
                    pygame.display.set_caption('Graph')  # 창 제목
                    show_text = False
                    show_graph = True
                elif button2.click(pos):
                    print("버튼 2 클릭")
                    graph_img = load_graph('2023_diff.png')
                    screen = pygame.display.set_mode((1000, 800))
                    background = pygame.image.load('cherry_blossom.jpg')
                    background = pygame.transform.scale(background, (1000, 800))
                    pygame.display.set_caption('Forecast')
                    show_text = False
                    show_predict = True
                elif button3.click(pos):
                    print("버튼 3 클릭")

        screen.blit(background, (0, 0)) # 배경 그리기(background 가 표시되는 위치) (0,0 은 좌측상단)

        if show_graph:
            graph_rect = graph_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
            screen.blit(graph_img, graph_rect)
            back_button.draw(screen)
            graph_list_button.draw(screen)

            if menu_open:
                graph1_button.draw(screen)
                graph2_button.draw(screen)
                graph3_button.draw(screen)
                graph4_button.draw(screen)
                graph5_button.draw(screen)

        elif show_predict:
            graph_rect = graph_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 10))
            screen.blit(graph_img, graph_rect)
            back_button.draw(screen)
            graph_list_button.draw(screen)

            if menu_open:
                graph6_button.draw(screen)
                graph7_button.draw(screen)
                graph8_button.draw(screen)

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