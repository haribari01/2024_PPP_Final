import matplotlib.pyplot as plt

def main():
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
    plt.show()
    plt.savefig('2024_diff.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()