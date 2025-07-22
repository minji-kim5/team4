import pandas as pd
import numpy as np
import nycflights13 as flights
df_flights = flights.flights
df_airlines = flights.airlines
df_airports = flights.airports
df_planes = flights.planes
df_weather = flights.weather
df_flights.head()
df_airlines
np.unique(df_flights['origin'])
np.unique(df_flights['carrier'])  #항공사: 16개
len(np.unique(df_flights['dest']))  #도착지: 105개


# 항공사별 운행 횟수 구하기
total=df_flights.groupby('carrier').size()

# 항공사별 지연 총 횟수 구하기
arr_del=df_flights[df_flights['arr_delay']>0].groupby('carrier').size()

# 운행횟수 대비 지연횟수 
summary=pd.DataFrame({'total_flights':total, 'delayed_flights': arr_del})

# 지연기록이 없는 항공사는 0처리
summary['delayed_flights']=summary['delayed_flights'].fillna(0)

# 지연률 (%)
summary['delay_rate(%)']=(summary['delayed_flights'])/summary['total_flights']*100

summary.sort_values('delay_rate(%)')

#소규모 항공사는 데이터가 너무 적어서 운행횟수의 평균을 구하고, 그 이상인 항공사만 추출 
flights_mean=summary['total_flights'].mean()
filtered_summary=summary[summary['total_flights']>flights_mean]

filtered_summary.sort_values('delay_rate(%)')
# 상위 6개의 항공사 중 AA 항공사가 가장 지연율이 적음
#  or 상위 3개 항공사 중에는 UA 항공사가 가장 지연율이 적음
# 상위 3개 항공사 추출할 거면
# top3=summary.nlargest(3,'total_flights')

