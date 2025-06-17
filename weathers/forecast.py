import azure.functions as func
import json
from datetime import datetime, timedelta
import logging
import traceback
from weathers.openmeteo import OpenMeteoClient
import calendar
 
weather_code_map = {
    0: "晴れ", 1: "主に晴れ", 2: "曇りがち", 3: "曇り", 45: "霧", 48: "霧（霧氷）",
    51: "弱い霧雨", 53: "中程度の霧雨", 55: "強い霧雨",
    61: "弱い雨", 63: "中程度の雨", 65: "強い雨",
    71: "弱い雪", 73: "中程度の雪", 75: "強い雪",
    80: "弱いにわか雨", 81: "にわか雨", 82: "激しいにわか雨"
}
#一週間の天気
def get_weekly_forecast(req: func.HttpRequest) -> func.HttpResponse:
    try:
        omc = OpenMeteoClient()
        today = datetime.today().date()
        end_day = today + timedelta(days=6)
 
        params = {
            'start_date': today,
            'end_date': end_day,
            'daily': [
                'weathercode',
                'temperature_2m_max', 'temperature_2m_min',
                'windspeed_10m_max'
                #'temperature_2m_mean',
                #'apparent_temperature_max', 'apparent_temperature_min', 'apparent_temperature_mean',
                #'sunshine_duration', 'shortwave_radiation_sum',
                #'uv_index_max', 'et0_fao_evapotranspiration',
                #'rain_sum', 'precipitation_hours',
                #'cloud_cover_min', 'cloud_cover_max', 'cloud_cover_mean',
                #'windgusts_10m_max',
                #'relative_humidity_2m_mean'
            ]
        }
 
        raw = omc.forecast(**params)
        days = raw['daily']
 
        result = []
        for i in range(len(days['time'])):
            date = days['time'][i]
            code = days['weathercode'][i]
            weather = weather_code_map.get(code, "不明")
 
            result.append({
                "date": date,
                "weather": weather,
                "temperature_max": f"{days['temperature_2m_max'][i]}℃",
                "temperature_min": f"{days['temperature_2m_min'][i]}℃",
                "windspeed_10m_max": f"{days['windspeed_10m_max'][i]} km/h"
                #"apparent_temperature_mean": f"{days['apparent_temperature_mean'][i]}℃",
                #"apparent_temperature_max": f"{days['apparent_temperature_max'][i]}℃",
                #"apparent_temperature_min": f"{days['apparent_temperature_min'][i]}℃",
                #"humidity": f"{days['relative_humidity_2m_mean'][i]}%",
                #"sunshine_duration": f"{days['sunshine_duration'][i]} 分",
                #"shortwave_radiation_sum": f"{days['shortwave_radiation_sum'][i]} MJ/m²",
                #"uv_index_max": days['uv_index_max'][i],
                #"et0_fao_evapotranspiration": f"{days['et0_fao_evapotranspiration'][i]} mm",
                #"rain_sum": f"{days['rain_sum'][i]} mm",
                #"precipitation_hours": f"{days['precipitation_hours'][i]} 時間",
                #"cloud_cover_min": f"{days['cloud_cover_min'][i]}%",
                #"cloud_cover_max": f"{days['cloud_cover_max'][i]}%",
                #"cloud_cover_mean": f"{days['cloud_cover_mean'][i]}%",
                #"temperature_mean": f"{days['temperature_2m_mean'][i]}℃",
                #"windgusts_10m_max": f"{days['windgusts_10m_max'][i]} km/h"
            })
 
        return func.HttpResponse(
            body=json.dumps(result, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype='application/json'
        )
   
    except Exception as e:
        logging.error(f'Exception occured in {traceback.format_exc()}: {e}')
        return func.HttpResponse(str(e), status_code=500)
 
#一日の天気
def get_daily_forecast(req: func.HttpRequest) -> func.HttpResponse:
    try:
        input_date_str = req.params.get("date")
        if not input_date_str:
            return func.HttpResponse("日付パラメータが必要です", status_code=400)
 
        input_date = datetime.strptime(input_date_str, "%Y-%m-%d").date()
        omc = OpenMeteoClient()
 
        params = {
            'start_date': input_date,
            'end_date': input_date,
            'daily': [
                'weathercode',
                'temperature_2m_max', 'temperature_2m_min',
                'windspeed_10m_max'
            ]
        }
 
        raw = omc.forecast(**params)
        days = raw['daily']
 
        if not days['time']:
            return func.HttpResponse("指定日の天気データが見つかりません", status_code=404)
 
        i = 0  # 1日分しかないはず
        date = days['time'][i]
        code = days['weathercode'][i]
        weather = weather_code_map.get(code, "不明")
 
        result = {
            "date": date,
            "weather": weather,
            "temperature_max": f"{days['temperature_2m_max'][i]}℃",
            "temperature_min": f"{days['temperature_2m_min'][i]}℃",
            "windspeed_10m_max": f"{days['windspeed_10m_max'][i]} km/h"
        }
 
        return func.HttpResponse(
            body=json.dumps(result, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype='application/json'
        )
 
    except Exception as e:
        logging.error(f'Exception occurred: {traceback.format_exc()}')
        return func.HttpResponse(str(e), status_code=500)
 
#瞬間の天気
def get_hourly_forecast(req: func.HttpRequest) -> func.HttpResponse:
    try:
        omc = OpenMeteoClient()
 
        datetime_str = req.params.get('datetime')  # 例: "2025-06-16T15:00"
        if not datetime_str:
            return func.HttpResponse("Missing 'datetime' parameter", status_code=400)
 
        dt = datetime.fromisoformat(datetime_str)
        date_str = dt.date().isoformat()
        hour_index = dt.hour
 
        params = {
            'start_date': date_str,
            'end_date': date_str,
            'hourly': [
                'weathercode',
                'temperature_2m',
                'apparent_temperature',
                'relative_humidity_2m',
                'rain',                      # 降水量（mm）
                'precipitation_probability', # 降水確率（%）
                'cloud_cover',               # 雲量（%）
                'windspeed_10m',             # 風速（10m）
                'windgusts_10m',             # 最大瞬間風速（10m）
                'shortwave_radiation',       # 日射量（W/m²）
                'uv_index'                   # UV指数
            ]
        }
 
        raw = omc.forecast(**params)
        hours = raw['hourly']
 
        # 時刻インデックスから該当データを抽出
        result = {
            "datetime": datetime_str,
            "weather": weather_code_map.get(hours['weathercode'][hour_index], "不明"),
            "temperature": f"{hours['temperature_2m'][hour_index]}℃",
            "apparent_temperature": f"{hours['apparent_temperature'][hour_index]}℃",
            "humidity": f"{hours['relative_humidity_2m'][hour_index]}%",
            "rain": f"{hours['rain'][hour_index]}mm",
            "precipitation_probability": f"{hours.get('precipitation_probability', [None])[hour_index]}%",
            "cloud_cover": f"{hours['cloud_cover'][hour_index]}%",
            "windspeed": f"{hours['windspeed_10m'][hour_index]}m/s",
            "windgusts": f"{hours['windgusts_10m'][hour_index]}m/s",
            "solar_radiation": f"{hours.get('shortwave_radiation', [None])[hour_index]}W/m²",
            "uv_index": f"{hours.get('uv_index', [None])[hour_index]}"
        }
 
        return func.HttpResponse(
            body=json.dumps(result, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype='application/json'
        )
 
    except Exception as e:
        logging.error(f'Exception occurred in {traceback.format_exc()}: {e}')
        return func.HttpResponse(str(e), status_code=500)
 
#1っか月の天気（販売実績カレンダーの天気表示）
#・現在の月をカレンダー表示する場合
#　今日より前の天気だけ表示（例：6月16日表示時 → 6月1日〜6月15日）
#・完全に過去の月を表示する場合
#　その月の1日〜末日まで全日分を取得して表示（例：5月表示 → 5月1日〜5月31日）
def get_monthly_history(req: func.HttpRequest) -> func.HttpResponse:
    try:
        omc = OpenMeteoClient(historical=True)
        input_date_str = req.route_params.get("date")  
        input_date = datetime.strptime(input_date_str, "%Y-%m-%d").date()
 
        # 対象月の1日と末日
        first_day = input_date.replace(day=1)
        last_day = input_date.replace(
            day=calendar.monthrange(input_date.year, input_date.month)[1]
        )
        today = datetime.today().date()
 
        # ロジック分岐
        if input_date.year == today.year and input_date.month == today.month:
            # 今月 → 今日の前日まで
            end_day = today - timedelta(days=1)
        elif input_date < today:
            # 完全に過去の月 → 末日まで取得
            end_day = last_day
        else:
            # 未来の月 → エラー
            return func.HttpResponse("未来の天気履歴は取得できません", status_code=400)
 
        params = {
            "start_date": first_day,
            "end_date": end_day,
            "daily": ["weathercode"],
            "timezone": "Asia/Tokyo"
        }
 
        raw = omc.forecast(**params)
        days = raw["daily"]
 
        result = []
        for i in range(len(days['time'])):
            date = days['time'][i]
            code = days['weathercode'][i]
            weather = weather_code_map.get(code, "不明")
 
            result.append({
                "date": date,
                "weather": weather
            })
 
        return func.HttpResponse(
            body=json.dumps(result, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype='application/json'
        )
 
    except Exception as e:
        logging.error(f"Exception in get_monthly_history: {traceback.format_exc()}")
        return func.HttpResponse(str(e), status_code=500)
 
 
 
 
 
 
 
# import azure.functions as func
# import json
# from datetime import datetime
# import logging
# import traceback
# from weathers.openmeteo import OpenMeteoClient
 
 
 
# def get_weekly_forecast(req: func.HttpRequest) -> func.HttpResponse:
#     try:
#         omc = OpenMeteoClient()
#         params = {
#             # the range of start_date and end_date will be set 7 days from today
#             'daily': ['weathercode', 'temperature_2m_mean', 'relative_humidity_2m_mean']
#         }
#         res = omc.forecast(**params)
#         return func.HttpResponse(
#             body=json.dumps(res, ensure_ascii=False, default=str),
#             status_code=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         logging.error(f'Exception occured in {traceback.format_exc()}: {e}')
#         return func.HttpResponse(str(e), status_code=500)
 
 
# def get_daily_forecast(req: func.HttpRequest) -> func.HttpResponse:
#     try:
#         omc = OpenMeteoClient()
#         date = datetime.strptime(req.route_params.get('date'), '%Y-%m-%d').date() # type: ignore
#         params = {
#             'start_date': date,
#             'end_date': date,
#             'hourly': ['weathercode', 'temperature_2m', 'relative_humidity_2m']
#         }
#         res = omc.forecast(**params)
#         return func.HttpResponse(
#             body=json.dumps(res, ensure_ascii=False, default=str),
#             status_code=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         logging.error(f'Exception occured in {traceback.format_exc()}: {e}')
#         return func.HttpResponse(str(e), status_code=500)