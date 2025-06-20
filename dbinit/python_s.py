import psycopg2
import pandas as pd

# CSV読み込み
df = pd.read_csv('s_20240401_20250401.csv')

# 英語列名 → カタカナ銘柄名
eng_to_jp = {
    'pale_ale': 'ペールエール',
    'lager': 'ラガー',
    'ipa': 'IPA',
    'white_beer': 'ホワイトビール',
    'dark_beer': '黒ビール',
    'fruit_beer': 'フルーツビール'
}

# カタカナ銘柄名 → beer_id
jp_to_id = {
    'ホワイトビール': 1,
    'ラガー': 2,
    'ペールエール': 3,
    'フルーツビール': 4,
    '黒ビール': 5,
    'IPA': 6
}

# 単価
unit_prices = {
    1: 900,
    2: 800,
    3: 1000,
    4: 1000,
    5: 1200,
    6: 900
}

conn = psycopg2.connect(
    dbname='postgres',
    user='hopcast',
    password='Hc123456',
    host='hopcast.postgres.database.azure.com',
    port=5432,
    sslmode='require'
)
cur = conn.cursor()

df = df.drop(columns=['weekday', 'month'], errors='ignore')

for _, row in df.iterrows():
    sale_date = row['date']
    for eng_name, jp_name in eng_to_jp.items():
        quantity = int(row[eng_name])
        if quantity > 0:
            beer_id = jp_to_id[jp_name]
            total_sales = quantity * unit_prices[beer_id]
            cur.execute(
                """
                INSERT INTO sale_records (sale_date, beer_id, quantity, total_sales, comment)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (sale_date, beer_id, quantity, total_sales, None)
            )

conn.commit()
cur.close()
conn.close()

 