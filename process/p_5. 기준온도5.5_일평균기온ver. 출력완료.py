import os
import requests

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


def gdd_ver1(tavg, dates, ref_temp, threshold, year):
    total_gdd = 0
    accum_days = 0
    flowering_date = None

    for temp, date in zip(tavg, dates):
        date_year = int(date.split('-')[0])  # date.split('-')은 ['2024', '06', '30'] 형태의 리스트
        date_month = int(date.split('-')[1])
        if date_year == year and date_month >= 2:
            accum_days += 1
            if temp is not None:
                eff_temp = temp - ref_temp
                if eff_temp < 0:
                    eff_temp = 0
                total_gdd += eff_temp
            if total_gdd >= threshold:
                flowering_date = date
                break
    return flowering_date, accum_days

def main():
    start_year = 1919
    end_year = 2024
    ref_temp = 5.5
    threshold = 106.2

    URL = (f"https://data.kma.go.kr/stcs/grnd/downloadGrndTaList.do?fileType=csv&pgmNo=70&menuNo=432&serviceSe=F00101&stdrMg=99999&startDt={start_year}0101&endDt={end_year}0531&taElement=MIN&taElement=AVG&taElement=MAX&stnGroupSns=&selectType=1&mddlClssCd=SFC01&dataFormCd=F00501&dataTypeCd=standard&startDay={start_year}0101&startYear={start_year}&endDay={end_year}0531&endYear={end_year}&startMonth=01&endMonth=12&sesnCd=0&txtStnNm=%EC%A0%84%EC%A3%BC&stnId=146&areaId=&gFontSize=")
    filename = "weather(146)_1919-2024.csv"
    download(filename, URL)

    dates = read_col_str(filename, 0)
    tavg = read_col(filename, 2)

    for year in range(start_year, end_year + 1):
        flowering_date = gdd_ver1(tavg, dates, ref_temp, threshold, year)
        if flowering_date:
            print(f"{year}년 2월 1일부터 누적일평균온도가 106.2를 넘는 날짜는 {flowering_date}입니다.")
        else:
            print(f"{year}년 2월 1일부터 누적일평균온도가 106.2를 넘는 날짜는 없습니다.")

if __name__ == "__main__":
    main()