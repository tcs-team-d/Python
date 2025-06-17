import azure.functions as func
import os
import yaml
import joblib
import json
from datetime import datetime, timedelta
import logging
import traceback
from weathers.openmeteo import OpenMeteoClient
from datetime import datetime
import pandas as pd
 

 


weather_code_map = {
    0: "晴れ",
    1: "主に晴れ",
    2: "曇りがち",
    3: "曇り",
    45: "霧",
    48: "霧（霧氷）",
    51: "弱い霧雨",
    53: "中程度の霧雨",
    55: "強い霧雨",
    61: "弱い雨",
    63: "中程度の雨",
    65: "強い雨",
    71: "弱い雪",
    73: "中程度の雪",
    75: "強い雪",
    80: "弱いにわか雨",
    81: "にわか雨",
    82: "激しいにわか雨",
}
model_path = os.path.join('checkpoints', 'catboost_default', 'model_lager.joblib')
model = joblib.load(model_path)
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
def get_weekly_demands(req: func.HttpRequest) -> func.HttpResponse:
    try:           
        omc = OpenMeteoClient()
        date = datetime.strptime(req.route_params.get('date'), '%Y-%m-%d').date() # type: ignore
        params = {
            'start_date': date,
            'end_date': date,
            'daily': config['independent_variables'][2:] 
        }
        res = omc.forecast(**params)

    except Exception as e:
        logging.error(f'Exception occured in {traceback.format_exc()}: {e}')
        return func.HttpResponse(str(e), status_code=500)

    x = pd.DataFrame([
        {
            'weekday': datetime.fromisoformat(date).weekday(),
            'month': datetime.fromisoformat(date).month,
            **{col: res['daily'][col][i] for col in config['independent_variables'][2:]}
        }
        for i, date in enumerate(res['daily']['time'])
    ])



    prediction = model.predict(x) 
    print(prediction)
    return func.HttpResponse(
        body=json.dumps(prediction, ensure_ascii=False, indent=2),
        status_code=200,
        mimetype='application/json'      
    )



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
                'temperature_2m_max',
                'temperature_2m_min',
                'temperature_2m_mean',
                'relative_humidity_2m_mean'
            ]
        }
        raw = omc.forecast(**params)
        days = raw['daily']
 
        result = []
        for i in range(len(days['time'])):
            date = days['time'][i]
            code = days['weathercode'][i]
            weather = weather_code_map.get(code, "不明")
            max_temp = days['temperature_2m_max'][i]
            min_temp = days['temperature_2m_min'][i]
            mean_temp = days['temperature_2m_mean'][i]
            humidity = days['relative_humidity_2m_mean'][i]
 
            result.append({
                "date": date,
                "weather": weather,
                "temperature_mean": f"{mean_temp}℃",
                "temperature_max": f"{max_temp}℃",
                "temperature_min": f"{min_temp}℃",
                "humidity": f"{humidity}%"
            })
 
        return func.HttpResponse(
            body=json.dumps(result, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype='application/json'
        )
    except Exception as e:
        logging.error(f'Exception occured in {traceback.format_exc()}: {e}')
        return func.HttpResponse(str(e), status_code=500)
 
 
def get_daily_forecast(req: func.HttpRequest) -> func.HttpResponse:
    try:
        omc = OpenMeteoClient()
        date = datetime.strptime(req.route_params.get('date'), '%Y-%m-%d').date() # type: ignore
        params = {
            'start_date': date,
            'end_date': date,
            'hourly': ['weathercode', 'temperature_2m', 'relative_humidity_2m']
        }
        res = omc.forecast(**params)
        return func.HttpResponse(
            body=json.dumps(res, ensure_ascii=False, default=str),
            status_code=200,
            mimetype='application/json'
        )
    except Exception as e:
        logging.error(f'Exception occured in {traceback.format_exc()}: {e}')
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
