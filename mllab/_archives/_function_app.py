import azure.functions as func
import logging
 
import requests
import json
 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
 
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
 
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    # https://archive-api.open-meteo.com/v1/archive?latitude=35.68&longitude=139.76&start_date=2024-04-01&end_date=2025-03-31&daily=weathercode&timezone=Asia%2FTokyo
    # https://archive-api.open-meteo.com/v1/archive?latitude=35.68&longitude=139.76&start_date=2024-04-01&end_date=2025-03-31&daily=weathercode&timezone=Asia%252FTokyo
 
    daily_parameters = [
        'temperature_2m_max',              # 日最高気温（°C）
        'temperature_2m_min',              # 日最低気温（°C）
        'apparent_temperature_max',        # 日最高体感温度（°C）
        'apparent_temperature_min',        # 日最低体感温度（°C）
        'precipitation_sum',               # 降水量合計（mm）
        'rain_sum',                        # 雨量合計（mm）
        'snowfall_sum',                    # 降雪量合計（cm）
        'precipitation_hours',             # 降水があった時間（時間）
        # 'sunrise',                         # 日の出時刻（ISO 8601形式）
        # 'sunset',                          # 日の入り時刻（ISO 8601形式）
        'windspeed_10m_max',               # 最大風速（10m高度、km/h）
        'windgusts_10m_max',               # 最大瞬間風速（10m高度、km/h）
        # 'winddirection_10m_dominant',      # 優勢風向（度）
        'shortwave_radiation_sum',         # 日射量（MJ/m²）
        'et0_fao_evapotranspiration',      # 参照作物の蒸発散量（mm）
        # 'uv_index_max',                    # 最大UV指数
        # 'uv_index_clear_sky_max',          # 最大UV指数（晴天時）
        'weathercode',                     # 天気コード（例：晴れ・雨など）
        'sunshine_duration'                # 日照時間（分）
    ]

    url = 'https://archive-api.open-meteo.com/v1/archive'
    params = {
        'latitude': 35.68,
        'longitude': 139.76,
        'start_date': '2024-04-01',
        'end_date': '2025-03-31',
        'daily': ",".join(daily_parameters),
        'timezone': 'Asia/Tokyo',
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return func.HttpResponse(
            body=json.dumps(res.json()),
            status_code=200,
            mimetype='application/json'
        )
    except requests.exceptions.RequestException as e:
        print(e)
        return func.HttpResponse(f'{e}')
   
 
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
 