import pandas as pd
import numpy as np

df_a = pd.read_csv(r'C:\Users\Admin\workspace\Python\mllab\20240401_20250331_weather_data.csv')
df_b = pd.read_csv(r'C:\Users\Admin\workspace\Python\mllab\20240401_20250331_sales.csv')

df_a['Date'] = pd.to_datetime(df_a['Date'])
df_b['Date'] = pd.to_datetime(df_b['Date'])

#merged_df = pd.merge(df_a, df_b, on='Date', how='left')

#merged_df.to_csv('20240401_20250331_data.csv', index=False)

df = pd.read_csv('20240401_20250331_data.csv')

# "-" を NaN に置き換える
df.replace("-", np.nan, inplace=True)

# 必要なら：数値に変換（"-" が入ってた列が文字列になってる場合）
df = df.apply(pd.to_numeric, errors='ignore')

# 'Date' を日付型に変換
df['Date'] = pd.to_datetime(df['Date'])

# 曜日ラベルの列を追加（例：Monday, Tuesday...）
df['Weekday'] = df['Date'].dt.day_name()

cols = df.columns.tolist()
cols.insert(1, cols.pop(cols.index('Weekday')))
df = df[cols]

df = df[df['Weekday'] != 'Sunday']

# 新しいCSVとして保存（上書きでもOK）
df.to_csv('20240401_20250331_weather_data_cleaned.csv', index=False)