import pandas as pd
import nycflights13 as flights
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def change(index):
    flights_data = flights.flights
    flights_data.head()
    flights_data.info()

    flights_data.isna().sum() # 결측치 확인
    flights_data = flights_data.dropna() # 결측치 삭제
    flights_data.info() 



    flights_data['is_delayed'] = flights_data['arr_delay'] > 15 # 지연시간 15분 초과를 지연으로 간주
    flights_data['is_delayed']

    # 계절 변수 생성
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

    result_L[result_L['total_count'] >= 30].sort_values(by='delay_rate').head(7)
    result_L[result_L['total_count'] >= 30].sort_values(by='delay_rate',ascending=False).head(20)

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
    result_L[result_L['전체운항'] >= 30].sort_values(by='정시율',ascending=False)


    filtered = result_L[(result_L['전체운항'] >= 30) & (result_L['정시율'] >= 0.95)]
    filtered['정시율'] = (filtered['정시율'] * 100).round(2)

    filtered = filtered.set_index('항공사').sort_values(by='정시율', ascending=False)

    if index =="DL":
        dl_filtered = filtered[filtered.index == 'DL']
        return dl_filtered
    elif index == "VX":
        dl_filtered = filtered[filtered.index == 'VX']
        return dl_filtered
    else:
        dl_filtered = filtered[filtered.index == 'UA']
        return dl_filtered

change("DL")