import pandas as pd
import nycflights13 as flights
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# macOS에서 한글 폰트 설정
mpl.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

flights_data = flights.flights
flights_data.head()
flights_data.info()

flights_data.isna().sum() # 결측치 확인
flights_data = flights_data.dropna() # 결측치 삭제
flights_data.info() 


flights_data['is_delayed'] = flights_data['arr_delay'] > 15 # 지연시간 15분 초과를 지연으로 간주

# 분기 변수 생성
conditions = [
    flights_data['month'].between(3, 5),    
    flights_data['month'].between(6, 8),    
    flights_data['month'].between(9, 11),   
    (flights_data['month'] == 12) | (flights_data['month'] <= 2)
]
choices = [1, 2, 3, 4]
flights_data['season'] = np.select(conditions, choices)
flights_data['season'].unique()

# 시간대 변수 생성
conditions = [
    (flights_data['hour'] >= 0) & (flights_data['hour'] < 5),
    (flights_data['hour'] >= 5) & (flights_data['hour'] < 8),
    (flights_data['hour'] >= 8) & (flights_data['hour'] < 11),
    (flights_data['hour'] >= 11) & (flights_data['hour'] < 14),
    (flights_data['hour'] >= 14) & (flights_data['hour'] < 17),
    (flights_data['hour'] >= 17) & (flights_data['hour'] < 20),
    (flights_data['hour'] >= 20) & (flights_data['hour'] < 24),
]

choices = [1, 2, 3, 4, 5, 6, 7]
flights_data['new_hour'] = np.select(conditions, choices)
flights_data['new_hour'].unique()

# 요일 변수 생성
flights_data['date'] = pd.to_datetime(flights_data[['year', 'month', 'day']])
flights_data['week'] = flights_data['date'].dt.weekday



grouped_by_origin = flights_data.groupby("origin") #공항을 기준으로 그룹


# JFK
jfk_flights = grouped_by_origin.get_group("JFK") #총 109079개 

# # JFK 출발 / 도착지 기준 상위 2개
jfk_dest = jfk_flights["dest"].value_counts()
jfk_top2_dest = jfk_flights["dest"].value_counts().head(2)

jfk_top2_dest_list = jfk_top2_dest.index


# JFK 상위 2개 노선 (LAX , SFO)
jfk_flights = jfk_flights[jfk_flights['dest'].isin(['LAX', 'SFO'])]

# JFK > LAX
jfk_flights_L = jfk_flights[jfk_flights['dest'].isin(['LAX'])]

# 각 변수별 지연률
jfk_flights_L.groupby('new_hour')['is_delayed'].sum() / jfk_flights_L.groupby('new_hour')['is_delayed'].count()
jfk_flights_L.groupby('week')['is_delayed'].sum() / jfk_flights_L.groupby('week')['is_delayed'].count()
jfk_flights_L.groupby('carrier')['is_delayed'].sum() / jfk_flights_L.groupby('carrier')['is_delayed'].count()

1 - jfk_flights_L.groupby('new_hour')['is_delayed'].mean()
1 - jfk_flights_L.groupby('week')['is_delayed'].mean()
1 - jfk_flights_L.groupby('carrier')['is_delayed'].mean()

# 변수별 조합의 지연률
result_L=jfk_flights_L.groupby(['new_hour','week','carrier'])['is_delayed'].sum() / jfk_flights_L.groupby(['new_hour','week','carrier'])['is_delayed'].count()
result_L = (
    jfk_flights_L
    .groupby(['new_hour', 'week', 'carrier'])['is_delayed']
    .agg(delay_count='sum', total_count='count')
    .assign(delay_rate=lambda x: x['delay_count'] / x['total_count'])
    .reset_index()
)
result_L.sort_values(by='delay_rate')  
result_L[result_L['total_count'] >= 30].sort_values(by='delay_rate') # 표본 수가 30이상만을 채택(정규성)

# JFK > SFO
jfk_flights_S = jfk_flights[jfk_flights['dest'].isin(['SFO'])]

# 각 변수별 지연률
jfk_flights_S.groupby('new_hour')['is_delayed'].sum() / jfk_flights_S.groupby('new_hour')['is_delayed'].count()
jfk_flights_S.groupby('week')['is_delayed'].sum() / jfk_flights_S.groupby('week')['is_delayed'].count()
jfk_flights_S.groupby('carrier')['is_delayed'].sum() / jfk_flights_S.groupby('carrier')['is_delayed'].count()

# 변수별 조합의 지연률
result_S=jfk_flights_S.groupby(['new_hour','week','carrier'])['is_delayed'].sum() / jfk_flights_S.groupby(['new_hour','week','carrier'])['is_delayed'].count()
result_S = (
    jfk_flights_S
    .groupby(['new_hour', 'week', 'carrier'])['is_delayed']
    .agg(delay_count='sum', total_count='count')
    .assign(delay_rate=lambda x: x['delay_count'] / x['total_count'])
    .reset_index()
)
result_S.sort_values(by='delay_rate')  
result_S[result_S['total_count'] >= 30].sort_values(by='delay_rate') # 표본 수가 30이상만을 채택(정규성)



# LGA
lga_flights = grouped_by_origin.get_group("LGA")
# LGA  상위 2개 노선(ATL , ORD)
lga_dest = lga_flights["dest"].value_counts()
lga_top2_dest = lga_flights["dest"].value_counts().head(2)

lga_top2_dest_list = lga_top2_dest.index

# LGA > ATL 
lga_flights = lga_flights[lga_flights['dest'].isin(['ATL', 'ORD'])]
lga_flights_A = lga_flights[lga_flights['dest'].isin(['ATL'])]

lga_flights_A.groupby('new_hour')['is_delayed'].sum() / lga_flights_A.groupby('new_hour')['is_delayed'].count()
lga_flights_A.groupby('week')['is_delayed'].sum() / lga_flights_A.groupby('week')['is_delayed'].count()
lga_flights_A.groupby('carrier')['is_delayed'].sum() / lga_flights_A.groupby('carrier')['is_delayed'].count()


result_A=lga_flights_A.groupby(['new_hour','week','carrier'])['is_delayed'].sum() / lga_flights_A.groupby(['new_hour','week','carrier'])['is_delayed'].count()
result_A = (
    lga_flights_A
    .groupby(['new_hour', 'week', 'carrier'])['is_delayed']
    .agg(delay_count='sum', total_count='count')
    .assign(delay_rate=lambda x: x['delay_count'] / x['total_count'])
    .reset_index()
)
result_A.sort_values(by='delay_rate')  
result_A[result_A['total_count'] >= 30].sort_values(by='delay_rate') # 표본 수가 30이상만을 채택(정규성)

# LGA > ORD,ATL
lga_flights_O = lga_flights[lga_flights['dest'].isin(['ORD'])]

lga_flights_O.groupby('new_hour')['is_delayed'].sum() / lga_flights_O.groupby('new_hour')['is_delayed'].count()
lga_flights_O.groupby('week')['is_delayed'].sum() / lga_flights_O.groupby('week')['is_delayed'].count()
lga_flights_O.groupby('carrier')['is_delayed'].sum() / lga_flights_O.groupby('carrier')['is_delayed'].count()

result_O = (
    lga_flights_O
    .groupby(['new_hour', 'week', 'carrier'])['is_delayed']
    .agg(delay_count='sum', total_count='count')
    .assign(delay_rate=lambda x: x['delay_count'] / x['total_count'])
    .reset_index()
)
result_O.sort_values(by='delay_rate')

result_O[result_O['total_count'] >= 30].sort_values(by='delay_rate')


# EWR
ewr_flights = grouped_by_origin.get_group("EWR")
# # EWR 기준 상위 2개 노선(ORD , BOS)
ewr_dest = ewr_flights["dest"].value_counts()
ewr_top2_dest = ewr_flights["dest"].value_counts().head(2)
ewr_top2_dest_list = ewr_top2_dest.index

# EWR > ORD 
ewr_flights = ewr_flights[ewr_flights['dest'].isin(['ORD','BOS'])]
ewr_flights_O = ewr_flights[ewr_flights['dest'].isin(['ORD'])]

ewr_flights_O.groupby('new_hour')['is_delayed'].sum() / ewr_flights_O.groupby('new_hour')['is_delayed'].count()
ewr_flights_O.groupby('week')['is_delayed'].sum() / ewr_flights_O.groupby('week')['is_delayed'].count()
ewr_flights_O.groupby('carrier')['is_delayed'].sum() / ewr_flights_O.groupby('carrier')['is_delayed'].count()

result_O = (
    ewr_flights_O
    .groupby(['new_hour', 'week', 'carrier'])['is_delayed']
    .agg(delay_count='sum', total_count='count')
    .assign(delay_rate=lambda x: x['delay_count'] / x['total_count'])
    .reset_index()
)

result_O.sort_values(by='delay_rate')
result_O[result_O['total_count'] >= 30].sort_values(by='delay_rate')


# EWR > BOS

ewr_flights_B = ewr_flights[ewr_flights['dest'].isin(['BOS'])]

ewr_flights_B.groupby('new_hour')['is_delayed'].sum() / ewr_flights_B.groupby('new_hour')['is_delayed'].count()
ewr_flights_B.groupby('week')['is_delayed'].sum() / ewr_flights_B.groupby('week')['is_delayed'].count()
ewr_flights_B.groupby('carrier')['is_delayed'].sum() / ewr_flights_B.groupby('carrier')['is_delayed'].count()

result_B = (
    ewr_flights_B
    .groupby(['new_hour', 'week', 'carrier'])['is_delayed']
    .agg(delay_count='sum', total_count='count')
    .assign(delay_rate=lambda x: x['delay_count'] / x['total_count'])
    .reset_index()
)

result_B.sort_values(by='delay_rate')
result_B[result_B['total_count'] >= 30].sort_values(by='delay_rate')

<<<<<<< HEAD
=======
#시각화
# index에 따라 시간대/요일/항공사별 정시 도착률 중 하나를 그림
def plot_JFK_LAX(index):
    """
    index: 1(시간대별), 2(요일별), 3(항공사별) 정시 도착률 플롯
    """
    # 데이터 준비
    on_time_hour = 1 - jfk_flights_L.groupby('new_hour')['is_delayed'].mean()
    on_time_week = 1 - jfk_flights_L.groupby('week')['is_delayed'].mean()
    on_time_carrier = 1 - jfk_flights_L.groupby('carrier')['is_delayed'].mean()

    if index == 1:
        # 시간대별 정시 도착률
        x = on_time_hour.index
        y = on_time_hour.values
        palette = 'Blues_d'
        title = "JFK→LAX 시간대별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.6, 0.92)
        yticks = np.arange(0.6, 0.92, 0.02)
        # 시간대 라벨
        time_labels = [
            "05-08(이른 출발)",
            "08-11(아침 러시)",
            "11-14(점심 이후)",
            "14-17(오후 출발)",
            "17-20(저녁 러시)",
            "20-00(야간 편)",
            "00-05(심야편)"
        ]
        xticklabels = time_labels
        xlabel = None
        rotation = 30
        ha = 'right'
    elif index == 2:
        # 요일별 정시 도착률
        x = on_time_week.index
        y = on_time_week.values
        palette = 'Greens_d'
        title = "JFK→LAX 요일별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.86)
        yticks = np.arange(0.7, 0.86, 0.02)
        weekday_labels = ['월', '화', '수', '목', '금', '토', '일']
        xticklabels = weekday_labels
        xlabel = None
        rotation = 0
        ha = 'center'
    elif index == 3:
        # 항공사별 정시 도착률
        x = on_time_carrier.index
        y = on_time_carrier.values
        palette = 'Reds_d'
        title = "JFK→LAX 항공사별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.85)
        yticks = np.arange(0.7, 0.85, 0.02)
        xticklabels = list(x)
        xlabel = None
        rotation = 0
        ha = 'center'
    else:
        raise ValueError("index must be 1(시간대), 2(요일), 3(항공사)")

    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    sns.barplot(x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold')
    # if xlabel:
    #     ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.set_xlabel("")  # Remove x-axis label for all plots
    ax.set_xticks(range(len(xticklabels)))
    ax.set_xticklabels(xticklabels, rotation=rotation, ha=ha)

    max_idx = y.argmax()
    for i, v in enumerate(y):
        color = 'red' if i == max_idx else 'black'
        weight = 'bold' if i == max_idx else 'normal'
        ax.text(i, v + 0.005, f"{v:.3f}", color=color, fontweight=weight, ha='center')
    plt.tight_layout()
    plt.show()
plot_JFK_LAX(1)
plot_JFK_LAX(2)
plot_JFK_LAX(3)

def plot_JFK_SFO(index):
    """
    index: 1(시간대별), 2(요일별), 3(항공사별) 정시 도착률 플롯 (JFK→SFO)
    """
    on_time_hour = 1 - jfk_flights_S.groupby('new_hour')['is_delayed'].mean()
    on_time_week = 1 - jfk_flights_S.groupby('week')['is_delayed'].mean()
    on_time_carrier = 1 - jfk_flights_S.groupby('carrier')['is_delayed'].mean()

    if index == 1:
        x = on_time_hour.index
        y = on_time_hour.values
        palette = 'Blues_d'
        title = "JFK→SFO 시간대별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.6, 0.92)
        yticks = np.arange(0.6, 0.92, 0.02)
        time_labels = [
            "05-08(이른 출발)", "08-11(아침 러시)", "11-14(점심 이후)",
            "14-17(오후 출발)", "17-20(저녁 러시)", "20-00(야간 편)", "00-05(심야편)"
        ]
        xticklabels = time_labels
        rotation = 30
        ha = 'right'
    elif index == 2:
        x = on_time_week.index
        y = on_time_week.values
        palette = 'Greens_d'
        title = "JFK→SFO 요일별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.86)
        yticks = np.arange(0.7, 0.86, 0.02)
        xticklabels = ['월', '화', '수', '목', '금', '토', '일']
        rotation = 0
        ha = 'center'
    elif index == 3:
        x = on_time_carrier.index
        y = on_time_carrier.values
        palette = 'Reds_d'
        title = "JFK→SFO 항공사별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.87)
        yticks = np.arange(0.7, 0.87, 0.02)
        xticklabels = list(x)
        rotation = 0
        ha = 'center'
    else:
        raise ValueError("index must be 1, 2, or 3")

    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    sns.barplot(x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.set_xlabel("")
    ax.set_xticks(range(len(xticklabels)))
    ax.set_xticklabels(xticklabels, rotation=rotation, ha=ha)
    max_idx = y.argmax()
    for i, v in enumerate(y):
        if v == 0:
            ax.text(i, ylim[0] + 0.01, "0.000", color='gray', fontweight='normal', ha='center')
            continue
        color = 'red' if i == max_idx else 'black'
        weight = 'bold' if i == max_idx else 'normal'
        ax.text(i, v + 0.005, f"{v:.3f}", color=color, fontweight=weight, ha='center')
    plt.tight_layout()
    plt.show()

plot_JFK_SFO(1)
plot_JFK_SFO(2)
plot_JFK_SFO(3)

def plot_LGA_ATL(index):
    """
    index: 1(시간대별), 2(요일별), 3(항공사별) 정시 도착률 플롯 (LGA→ATL)
    """
    on_time_hour = 1 - lga_flights_A.groupby('new_hour')['is_delayed'].mean()
    on_time_week = 1 - lga_flights_A.groupby('week')['is_delayed'].mean()
    on_time_carrier = 1 - lga_flights_A.groupby('carrier')['is_delayed'].mean()

    if index == 1:
        x = on_time_hour.index
        y = on_time_hour.values
        palette = 'Blues_d'
        title = "LGA→ATL 시간대별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.6, 0.86)
        yticks = np.arange(0.6, 0.86, 0.02)
        time_labels = [
            "05-08(이른 출발)", "08-11(아침 러시)", "11-14(점심 이후)",
            "14-17(오후 출발)", "17-20(저녁 러시)", "20-00(야간 편)", "00-05(심야편)"
        ]
        xticklabels = time_labels
        rotation = 30
        ha = 'right'
    elif index == 2:
        x = on_time_week.index
        y = on_time_week.values
        palette = 'Greens_d'
        title = "LGA→ATL 요일별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.84)
        yticks = np.arange(0.7, 0.84, 0.02)
        xticklabels = ['월', '화', '수', '목', '금', '토', '일']
        rotation = 0
        ha = 'center'
    elif index == 3:
        x = on_time_carrier.index
        y = on_time_carrier.values
        palette = 'Reds_d'
        title = "LGA→ATL 항공사별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.6, 0.82)
        yticks = np.arange(0.6, 0.82, 0.02)
        xticklabels = list(x)
        rotation = 0
        ha = 'center'
    else:
        raise ValueError("index must be 1, 2, or 3")

    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    sns.barplot(x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.set_xlabel("")
    ax.set_xticks(range(len(xticklabels)))
    ax.set_xticklabels(xticklabels, rotation=rotation, ha=ha)
    max_idx = y.argmax()
    for i, v in enumerate(y):
        if v == 0:
            ax.text(i, ylim[0] + 0.01, "0.000", color='gray', fontweight='normal', ha='center')  # Y=0.6보다 살짝 위
            continue
        color = 'red' if i == max_idx else 'black'
        weight = 'bold' if i == max_idx else 'normal'
        ax.text(i, v + 0.005, f"{v:.3f}", color=color, fontweight=weight, ha='center')
    plt.tight_layout()
    plt.show()
plot_LGA_ATL(1)
plot_LGA_ATL(2)
plot_LGA_ATL(3)

# LGA→ORD 시각화 함수 추가
def plot_LGA_ORD(index):
    """
    index: 1(시간대별), 2(요일별), 3(항공사별) 정시 도착률 플롯 (LGA→ORD)
    """
    on_time_hour = 1 - lga_flights_O.groupby('new_hour')['is_delayed'].mean()
    on_time_week = 1 - lga_flights_O.groupby('week')['is_delayed'].mean()
    on_time_carrier = 1 - lga_flights_O.groupby('carrier')['is_delayed'].mean()

    if index == 1:
        x = on_time_hour.index
        y = on_time_hour.values
        palette = 'Blues_d'
        title = "LGA→ORD 시간대별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.64, 0.94)
        yticks = np.arange(0.64, 0.942, 0.02)
        time_labels = [
            "05-08(이른 출발)", "08-11(아침 러시)", "11-14(점심 이후)",
            "14-17(오후 출발)", "17-20(저녁 러시)", "20-00(야간 편)", "00-05(심야편)"
        ]
        xticklabels = time_labels
        rotation = 30
        ha = 'right'
    elif index == 2:
        x = on_time_week.index
        y = on_time_week.values
        palette = 'Greens_d'
        title = "LGA→ORD 요일별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.93)
        yticks = np.arange(0.7, 0.93, 0.02)
        xticklabels = ['월', '화', '수', '목', '금', '토', '일']
        rotation = 0
        ha = 'center'
    elif index == 3:
        x = on_time_carrier.index
        y = on_time_carrier.values
        palette = 'Reds_d'
        title = "LGA→ORD 항공사별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.823)
        yticks = np.arange(0.7, 0.83, 0.02)
        xticklabels = list(x)
        rotation = 0
        ha = 'center'
    else:
        raise ValueError("index must be 1, 2, or 3")

    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    sns.barplot(x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.set_xlabel("")
    ax.set_xticks(range(len(xticklabels)))
    ax.set_xticklabels(xticklabels, rotation=rotation, ha=ha)
    max_idx = y.argmax()
    for i, v in enumerate(y):
        if v == 0:
            ax.text(i, ylim[0] + 0.01, "0.000", color='gray', fontweight='normal', ha='center')
            continue
        color = 'red' if i == max_idx else 'black'
        weight = 'bold' if i == max_idx else 'normal'
        ax.text(i, v + 0.005, f"{v:.3f}", color=color, fontweight=weight, ha='center')
    plt.tight_layout()
    plt.show()
plot_LGA_ORD(1)
plot_LGA_ORD(2)
plot_LGA_ORD(3)

def plot_EWR_ORD(index):
    """
    index: 1(시간대별), 2(요일별), 3(항공사별) 정시 도착률 플롯 (EWR→ORD)
    """
    on_time_hour = 1 - ewr_flights_O.groupby('new_hour')['is_delayed'].mean()
    on_time_week = 1 - ewr_flights_O.groupby('week')['is_delayed'].mean()
    on_time_carrier = 1 - ewr_flights_O.groupby('carrier')['is_delayed'].mean()

    if index == 1:
        x = on_time_hour.index
        y = on_time_hour.values
        palette = 'Blues_d'
        title = "EWR→ORD 시간대별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.6, 0.88)
        yticks = np.arange(0.6, 0.88, 0.02)
        time_labels = [
            "05-08(이른 출발)", "08-11(아침 러시)", "11-14(점심 이후)",
            "14-17(오후 출발)", "17-20(저녁 러시)", "20-00(야간 편)", "00-05(심야편)"
        ]
        xticklabels = time_labels
        rotation = 30
        ha = 'right'
    elif index == 2:
        x = on_time_week.index
        y = on_time_week.values
        palette = 'Greens_d'
        title = "EWR→ORD 요일별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.6, 0.88)
        yticks = np.arange(0.6, 0.88, 0.02)
        xticklabels = ['월', '화', '수', '목', '금', '토', '일']
        rotation = 0
        ha = 'center'
    elif index == 3:
        x = on_time_carrier.index
        y = on_time_carrier.values
        palette = 'Reds_d'
        title = "EWR→ORD 항공사별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.4, 0.8)
        yticks = np.arange(0.4, 0.8, 0.02)
        xticklabels = list(x)
        rotation = 0
        ha = 'center'
    else:
        raise ValueError("index must be 1, 2, or 3")

    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    sns.barplot(x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.set_xlabel("")
    ax.set_xticks(range(len(xticklabels)))
    ax.set_xticklabels(xticklabels, rotation=rotation, ha=ha)
    max_idx = y.argmax()
    for i, v in enumerate(y):
        if v == 0:
            ax.text(i, v + 0.01, "0.000", color='gray', fontweight='normal', ha='center')
            continue
        color = 'red' if i == max_idx else 'black'
        weight = 'bold' if i == max_idx else 'normal'
        ax.text(i, v + 0.005, f"{v:.3f}", color=color, fontweight=weight, ha='center')
    plt.tight_layout()
    plt.show()
plot_EWR_ORD(1)
plot_EWR_ORD(2)
plot_EWR_ORD(3)

# EWR→BOS 시각화 함수 추가
def plot_EWR_BOS(index):
    """
    index: 1(시간대별), 2(요일별), 3(항공사별) 정시 도착률 플롯 (EWR→BOS)
    """
    on_time_hour = 1 - ewr_flights_B.groupby('new_hour')['is_delayed'].mean()
    on_time_week = 1 - ewr_flights_B.groupby('week')['is_delayed'].mean()
    on_time_carrier = 1 - ewr_flights_B.groupby('carrier')['is_delayed'].mean()

    if index == 1:
        x = on_time_hour.index
        y = on_time_hour.values
        palette = 'Blues_d'
        title = "EWR→BOS 시간대별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.6, 0.96)
        yticks = np.arange(0.6, 0.96, 0.02)
        time_labels = [
            "05-08(이른 출발)", "08-11(아침 러시)", "11-14(점심 이후)",
            "14-17(오후 출발)", "17-20(저녁 러시)", "20-00(야간 편)", "00-05(심야편)"
        ]
        xticklabels = time_labels
        rotation = 30
        ha = 'right'
    elif index == 2:
        x = on_time_week.index
        y = on_time_week.values
        palette = 'Greens_d'
        title = "EWR→BOS 요일별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.92)
        yticks = np.arange(0.7, 0.92, 0.02)
        xticklabels = ['월', '화', '수', '목', '금', '토', '일']
        rotation = 0
        ha = 'center'
    elif index == 3:
        x = on_time_carrier.index
        y = on_time_carrier.values
        palette = 'Reds_d'
        title = "EWR→BOS 항공사별 정시 도착률"
        ylabel = "정시율 (1 - 지연률)"
        ylim = (0.7, 0.92)
        yticks = np.arange(0.7, 0.92, 0.02)
        xticklabels = list(x)
        rotation = 0
        ha = 'center'
    else:
        raise ValueError("index must be 1, 2, or 3")

    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    sns.barplot(x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.set_xlabel("")
    ax.set_xticks(range(len(xticklabels)))
    ax.set_xticklabels(xticklabels, rotation=rotation, ha=ha)
    max_idx = y.argmax()
    for i, v in enumerate(y):
        if v == 0:
            ax.text(i, ylim[0] + 0.01, "0.000", color='gray', fontweight='normal', ha='center')
            continue
        color = 'red' if i == max_idx else 'black'
        weight = 'bold' if i == max_idx else 'normal'
        ax.text(i, v + 0.005, f"{v:.3f}", color=color, fontweight=weight, ha='center')
    plt.tight_layout()
    plt.show()
plot_EWR_BOS(1)
plot_EWR_BOS(2)
plot_EWR_BOS(3)


result_L['on_time'] = 1 - result_L['delay_rate']
result_L
# 1. delay_rate 열 삭제
result_L = result_L.drop(columns=['delay_rate'])

# 2. 변수명 한글로 변경
result_L = result_L.rename(columns={
    'new_hour': '시간대',
    'week': '요일',
    'carrier': '항공사',
    'delay_count': '지연건수',
    'total_count': '전체운항',
    'on_time': '정시율'
})

# 3. 백분율로 변환 및 반올림result_L['정시율'] = (result_L['정시율'] * 100).round(2)
result_L['지연률'] = (result_L['지연건수'] / result_L['전체운항'] * 100).round(2)

# 인덱스 없이 출력
print(result_L.to_string(index=False))

hour_labels = {
    1: '0–5시',
    2: '5–8시',
    3: '8–11시',
    4: '11–14시',
    5: '14–17시',
    6: '17–20시',
    7: '20–24시'
}
result_L['시간대'] = result_L['시간대'].map(hour_labels)

week_labels = {
    0: '월요일',
    1: '화요일',
    2: '수요일',
    3: '목요일',
    4: '금요일',
    5: '토요일',
    6: '일요일'
}
result_L['요일'] = result_L['요일'].map(week_labels)


result_L = result_L.drop(columns=['지연률'])
result_L = result_L.reset_index(drop=True)
result_L[result_L['전체운항'] >= 30].sort_values(by='정시율',ascending=False).head(7)
>>>>>>> e7ed3cc116a06b36939f3ff57bd4c5a7303543df
