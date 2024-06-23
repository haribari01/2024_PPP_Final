import os
import requests
import matplotlib.pyplot as plt
import csv

def download(filename, URL):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8-sig") as f:
            res = requests.get(URL)
            f.write(res.text.replace("\r", ""))

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
    flowering_date = None

    for temp, date in zip(tmax, dates):
        date_year = int(date.split('-')[0])    #date.split('-')은 ['2024', '06', '30'] 리스트형태
        date_month = int(date.split('-')[1])
        if date_year == year and date_month >= 2:
            total_days += 1
            if temp is not None:
                accum_temp += temp
            if accum_temp >= threshold:
                flowering_date = date
                break    #초기화 하고 다시 계산하기 위해

    # return flowering_date , total_days
    return total_days

def main():
    start_year = 1919
    end_year = 2024
    threshold = 600

    URL = (f"https://data.kma.go.kr/stcs/grnd/downloadGrndTaList.do?fileType=csv&pgmNo=70&menuNo=432&serviceSe=F00101&stdrMg=99999&startDt={start_year}0101&endDt={end_year}0531&taElement=MIN&taElement=AVG&taElement=MAX&stnGroupSns=&selectType=1&mddlClssCd=SFC01&dataFormCd=F00501&dataTypeCd=standard&startDay={start_year}0101&startYear={start_year}&endDay={end_year}0531&endYear={end_year}&startMonth=01&endMonth=12&sesnCd=0&txtStnNm=%EC%A0%84%EC%A3%BC&stnId=146&areaId=&gFontSize=")
    filename = "weather(146)_1919-2024.csv"
    download(filename, URL)

    dates = read_col_str(filename, 0)
    tmax = read_col(filename, 4)

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
    plt.savefig('degree_600.png', dpi=300, bbox_inches='tight')  #저장 / #bbox_inches='tight : 불필요한 여백제거
    plt.close()

if __name__ == "__main__":
    main()