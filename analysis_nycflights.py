import pandas as pd

#data 불러오기
flights_data = pd.read_csv("./data/nycflights.csv")
flights_data.head()

pd.unique(flights_data["carrier"]) 
#항공사 코드
# 'VX', 'DL', '9E', 'AA', 'WN', 'B6', 'EV', 'FL', 'UA', 'US', 'MQ','F9', 'YV', 'AS', 'HA', 'OO'

pd.unique(flights_data["tailnum"])
#항공기 등록번호(꼬리번호)
# array(['N626VA', 'N3760C', 'N712TW', ..., 'N720WN', 'N534US', 'N924WN'],shape=(3490,), dtype=object)

pd.unique(flights_data["flight"])
#항공편 번호
# array([ 407,  329,  422, ...,  552, 3986,  819], shape=(2951,))

pd.unique(flights_data["origin"])
#출발 공항 코드
#array(['JFK', 'LGA', 'EWR'], dtype=object)

pd.unique(flights_data["dest"])
# array(['LAX', 'SJU', 'TPA', 'ORF', 'ORD', 'HOU', 'IAD', 'MIA', 'JAX',
#        'ROC', 'RSW', 'DAY', 'ATL', 'BTV', 'BUF', 'DCA', 'FLL', 'SFO',
#        'PIT', 'PBI', 'DEN', 'CLT', 'CMH', 'LAS', 'DTW', 'BNA', 'PHL',
#        'MKE', 'DFW', 'SNA', 'CLE', 'MCO', 'BQN', 'ABQ', 'BOS', 'IAH',
#        'OMA', 'SYR', 'EGE', 'PWM', 'AUS', 'STT', 'MSY', 'CVG', 'RDU',
#        'MDW', 'IND', 'TYS', 'STL', 'TUL', 'JAC', 'SEA', 'MSP', 'BWI',
#        'SAT', 'CRW', 'BUR', 'SLC', 'CHS', 'RIC', 'SAN', 'XNA', 'MEM',
#        'SRQ', 'PHX', 'MCI', 'CAK', 'SAV', 'SDF', 'TVC', 'OAK', 'GSP',
#        'ALB', 'BDL', 'DSM', 'LGB', 'PDX', 'MSN', 'SMF', 'GRR', 'GSO',
#        'BGR', 'ACK', 'SJC', 'AVL', 'OKC', 'PVD', 'MHT', 'HNL', 'MTJ',
#        'BHM', 'PSE', 'ILM', 'MVY', 'HDN', 'BZN', 'CHO', 'CAE', 'EYW',
#        'ANC', 'MYR', 'PSP'], dtype=object), shape=(102,)



flights_data.loc[:,:].info()
#결측치 X



grouped_by_origin = flights_data.groupby("origin")
jfk_flights = grouped_by_origin.get_group("JFK") #총 10897개 
jfk_flights
jfk_flights_destinations = jfk_flights["dest"].unique() #JFK <-> 도착지(66개)
jfk_flights_destinations
# array(['LAX', 'SJU', 'TPA', 'IAD', 'ROC', 'BTV', 'FLL', 'SFO', 'DEN',
#        'CLT', 'LAS', 'PHL', 'DCA', 'JAX', 'HOU', 'ABQ', 'BUF', 'EGE',
#        'AUS', 'STT', 'MSY', 'IAH', 'RDU', 'IND', 'DTW', 'SEA', 'RSW',
#        'MSP', 'BNA', 'BOS', 'BWI', 'SAT', 'ATL', 'MIA', 'BUR', 'SLC',
#        'ORD', 'CHS', 'PBI', 'PIT', 'PHX', 'MCO', 'OAK', 'CLE', 'LGB',
#        'SAN', 'SMF', 'CMH', 'RIC', 'CVG', 'SYR', 'SRQ', 'PWM', 'DFW',
#        'ORF', 'ACK', 'SJC', 'BQN', 'MKE', 'HNL', 'PDX', 'PSE', 'MVY',
#        'MCI', 'PSP', 'SDF'], dtype=object,shape=(66,))

# JFK 출발 / 도착지 기준 상위 10개
jfk_top10_dest = jfk_flights["dest"].value_counts().head(10)
jfk_top10_dest_list = jfk_top10_dest.index
# JFK 출발 / 도착지 지연정보
jfk_delay_info = (jfk_flights[jfk_flights["dest"].isin(list(jfk_top10_dest_list))]
                  .groupby("dest")[["arr_time", "arr_delay"]]
                  .mean()
                  .sort_values("arr_delay",ascending=False)
                )   
jfk_delay_info


lga_flights = grouped_by_origin.get_group("LGA") #총 10067개 
lga_flights
lga_flights_destinations = lga_flights["dest"].unique() #LGA <-> 도착지(83개)
lga_flights_destinations
# array(['ORF', 'ORD', 'MIA', 'RSW', 'ATL', 'PIT', 'PBI', 'CLT', 'CMH',
#        'DTW', 'BNA', 'DEN', 'DFW', 'CLE', 'MCO', 'BOS', 'IAH', 'SYR',
#        'MDW', 'IND', 'STL', 'ROC', 'FLL', 'RDU', 'CRW', 'TPA', 'XNA',
#        'MEM', 'SRQ', 'CAK', 'MKE', 'TVC', 'MSP', 'MSY', 'DCA', 'SAV',
#        'PHL', 'CVG', 'CHS', 'IAD', 'GSO', 'BGR', 'BTV', 'TYS', 'PWM',
#        'BUF', 'MCI', 'GRR', 'DSM', 'RIC', 'OMA', 'MHT', 'HOU', 'BHM',
#        'DAY', 'ILM', 'SDF', 'MSN', 'JAX', 'GSP', 'CHO', 'EYW', 'AVL',
#        'BWI', 'CAE'], dtype=object, shape=(65,))

# LGA 출발 비행편에서 도착지 기준 상위 10개
lga_top10_dest = lga_flights["dest"].value_counts().head(10)
lga_top10_dest_list = lga_top10_dest.index
# LGA 출발 / 도착지 지연정보
lga_delay_info = (lga_flights[lga_flights["dest"].isin(list(lga_top10_dest_list))]
                  .groupby("dest")[["arr_time", "arr_delay"]]
                  .mean()
                  .sort_values("arr_delay",ascending=False)
                )   
lga_delay_info


ewr_flights = grouped_by_origin.get_group("EWR") #총 11771개 
ewr_flights
ewr_flights_destinations = ewr_flights["dest"].unique() #EWR <-> 도착지(83개)
ewr_flights_destinations
# array(['HOU', 'JAX', 'DAY', 'BUF', 'DCA', 'ORD', 'PBI', 'MKE', 'SNA',
#        'TPA', 'LAS', 'CLT', 'DTW', 'BQN', 'CLE', 'OMA', 'MCO', 'PWM',
#        'IAD', 'ATL', 'CVG', 'FLL', 'RDU', 'DEN', 'DFW', 'LAX', 'BOS',
#        'TYS', 'STL', 'TUL', 'JAC', 'IAH', 'MIA', 'RIC', 'SAN', 'BNA',
#        'SAT', 'MDW', 'PHX', 'MCI', 'MEM', 'SEA', 'SAV', 'SDF', 'CMH',
#        'SFO', 'MSP', 'AUS', 'RSW', 'GSP', 'ALB', 'BDL', 'DSM', 'PDX',
#        'MSN', 'CHS', 'GRR', 'MSY', 'IND', 'GSO', 'BWI', 'SJU', 'XNA',
#        'ROC', 'AVL', 'OKC', 'PVD', 'SYR', 'MHT', 'BTV', 'ORF', 'MTJ',
#        'STT', 'SLC', 'PIT', 'HNL', 'EGE', 'HDN', 'BZN', 'TVC', 'CAE',
#        'ANC', 'MYR'], dtype=object, shape=(83,))

# EWR 출발 비행편에서 도착지 기준 상위 10개
ewr_top10_dest = ewr_flights["dest"].value_counts().head(10)
ewr_top10_dest_list = ewr_top10_dest.index
# EWR 출발 / 도착지 지연정보
ewr_delay_info = (ewr_flights[ewr_flights["dest"].isin(list(ewr_top10_dest_list))]
                  .groupby("dest")[["arr_time", "arr_delay"]]
                  .mean()
                  .sort_values("arr_delay",ascending=False)
                )   
ewr_delay_info