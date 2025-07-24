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

# 강희준 test


## test 2
import matplotlib.pyplot as plt

# ✅ 한글 폰트 설정 (Windows 기준: 'Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ✅ 파이차트 데이터
labels = [' ', ' ']
sizes = [2.45, 97.55]
colors = ['#ff9999', '#66b3ff']  # 결측치: 분홍 / 비결측치: 파랑
explode = (0.1, 0)  # 결측치 조각 강조

# ✅ 굵은 텍스트를 위한 함수
def make_autopct(labels):
    def inner_autopct(pct):
        label = labels[0] if pct < 50 else labels[1]
        return f'{label}\n{pct:.2f}%'
    return inner_autopct

# ✅ 파이차트 그리기
plt.figure(figsize=(6, 6))
wedges, texts, autotexts = plt.pie(
    sizes,
    labels=None,
    colors=colors,
    autopct=make_autopct(labels),
    startangle=90,
    explode=explode,
    shadow=True
)

# ✅ 텍스트 bold 처리
for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)


# ✅ 제목
plt.title('결측치 vs 비결측치 비율', fontsize=14, fontweight='bold')
plt.axis('equal')  # 원형 유지
plt.tight_layout()
plt.show()
