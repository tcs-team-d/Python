import json
import pandas as pd

# JSONファイルを読み込む
with open(r'C:\Users\Admin\workspace\Python\mllab\weatherdata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# dailyの部分をDataFrameにする
df = pd.DataFrame(data['daily'])

df = df[[
    'time', "temperature_2m_max","temperature_2m_min", 
    "apparent_temperature_max", "apparent_temperature_min", 
    "precipitation_sum", "rain_sum", "snowfall_sum", 
    "precipitation_hours", "windspeed_10m_max", 
    "windgusts_10m_max", "shortwave_radiation_sum", 
    "et0_fao_evapotranspiration", "weathercode", "sunshine_duration"
    ]]
df.columns = ['Date', "temperature_2m_max","temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours", "windspeed_10m_max", "windgusts_10m_max", "shortwave_radiation_sum", "et0_fao_evapotranspiration", "weathercode", "sunshine_duration"]

df.to_csv('20240401_20250331_weather_data.csv', index=False)