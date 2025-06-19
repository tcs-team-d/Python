import pandas as pd
from openmeteoclient import OpenMeteoClient



'''
import sales data
'''
dfs = pd.read_csv('data/クラフトビール専門店_売上データ_2024年4月-2025年4月 (曜日ありデータ).csv')
columns_jp = ['日付', '曜日', 'ペールエール(本)', 'ラガー(本)', 'IPA(本)', 'ホワイトビール(本)', '黒ビール(本)', 'フルーツビール(本)']
columns_en = ['date', 'weekday', 'pale_ale', 'lager', 'ipa', 'white_beer', 'dark_beer', 'fruit_beer']
dfs = dfs[columns_jp]
dfs = dfs[~dfs.apply(lambda row: all(row == columns_jp), axis=1)]
dfs.rename(columns={jp: en for jp, en in zip(columns_jp, columns_en)}, inplace=True)

dfs = dfs.replace('-', 0).fillna(0) # ignore: type
dfs[columns_en[2:]] = dfs[columns_en[2:]].astype(int)
dfs['date'] = pd.to_datetime(dfs['date'])
dfs['weekday'] = dfs['weekday'].map({'土': 0, '日': 1, '月': 2, '火': 3, '水': 4, '木': 5, '金': 6})
dfs['month'] = dfs['date'].dt.month
# print(dfs.info())
# print(dfs.head())
# print(dfs.isnull().sum())
# print(dfs.describe())
# dfs.to_csv('data/s_20240401_20250401.csv', index=False)


'''
get weather data from open-meteo
'''
openmeteo = OpenMeteoClient()
weather_params = [
    'weathercode',
    'temperature_2m_min',
    'temperature_2m_max',
    'temperature_2m_mean',
    'apparent_temperature_min',
    'apparent_temperature_max',
    'apparent_temperature_mean',
    'sunshine_duration',
    'shortwave_radiation_sum',
    'uv_index_max',
    'et0_fao_evapotranspiration',
    'rain_sum',
    'precipitation_hours',
    'cloud_cover_min',
    'cloud_cover_max',
    'cloud_cover_mean',
    'windspeed_10m_max',
    'windgusts_10m_max',
]
params = {
    'daily': weather_params,
    'start_date': '2024-04-01',
    'end_date': '2025-04-01',
}
res = openmeteo.forecast(**params) # should be .archive(), but forecast() is more compatible
dfw = pd.DataFrame(res['daily']) # type: ignore
dfw['date'] = pd.to_datetime(dfw['time'])
dfw = dfw.drop(columns='time')
# print(dfw.info())
# print(dfw.head())
# print(dfw.isnull().sum())
# print(dfw.describe())
# dfs.to_csv('data/w_20240401_20250401.csv', index=False)


'''
merge sales and weather data
'''
df = pd.merge(dfs, dfw, on='date')
print(df.info())
print(df.head())
print(df.isnull().sum())
print(df.describe())
df.to_csv('data/20240401_20250401.csv', index=False)