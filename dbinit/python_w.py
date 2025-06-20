import pandas as pd
import psycopg2

# CSV読み込み
df = pd.read_csv('w_20240401_20250619.csv')  # ファイル名は適宜変更

# DB接続情報
conn = psycopg2.connect(
    dbname='postgres',
    user='hopcast',
    password='Hc1234567',
    host='hopcast.postgres.database.azure.com',
    port=5432,
    sslmode='require'
)
cur = conn.cursor()

# INSERT
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO weather_records (
            record_date, weathercode,
            temperature_2m_min, temperature_2m_max, temperature_2m_mean,
            apparent_temperature_min, apparent_temperature_max, apparent_temperature_mean,
            relative_humidity_2m_mean,
            sunshine_duration, shortwave_radiation_sum, uv_index_max, et0_fao_evapotranspiration,
            rain_sum, precipitation_hours, cloud_cover_min, cloud_cover_max, cloud_cover_mean,
            windspeed_10m_max, windgusts_10m_max
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['record_date'], row['weathercode'],
        row['temperature_2m_min'], row['temperature_2m_max'], row['temperature_2m_mean'],
        row['apparent_temperature_min'], row['apparent_temperature_max'], row['apparent_temperature_mean'],
        row['relative_humidity_2m_mean'],
        row['sunshine_duration'], row['shortwave_radiation_sum'], row['uv_index_max'], row['et0_fao_evapotranspiration'],
        row['rain_sum'], row['precipitation_hours'], row['cloud_cover_min'], row['cloud_cover_max'], row['cloud_cover_mean'],
        row['windspeed_10m_max'], row['windgusts_10m_max']
    ))

# コミット & クローズ
conn.commit()
cur.close()
conn.close()
