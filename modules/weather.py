import azure.functions as func
import json
import logging
import traceback
from datetime import datetime
import requests
from retry_requests import retry
from modules.openmeteoclient import OpenMeteoClient



_session = retry(requests.Session(), retries=3, backoff_factor=0.2)
openmeteo = OpenMeteoClient(session=_session)


def get_daily_forecast_wrapper(req: func.HttpRequest) -> func.HttpResponse:
    try:
        start_date = datetime.strptime(req.params.get('start_date'), '%Y-%m-%d').date() # type: ignore
        end_date = datetime.strptime(req.params.get('end_date'), '%Y-%m-%d').date() # type: ignore
        res = get_daily_forecast(start_date, end_date, OpenMeteoClient.DEFAULT_DAILY_PARAMS)
        
        daily = res['daily'] # type: ignore
        units = res['daily_units'] # type: ignore
        ret = []
        for i, date in enumerate(daily['time']):
            entry = {
                'date': date,
                'weather': OpenMeteoClient.WEATHERCODE_MSP.get(daily['weathercode'][i], '不明')
            }
            for key in OpenMeteoClient.DEFAULT_DAILY_PARAMS:
                entry[key] = f'{daily[key][i]}{units[key]}'
            ret.append(entry)
        return func.HttpResponse(
            body=json.dumps(ret, ensure_ascii=False, default=str),
            status_code=200,
            mimetype='application/json'
        )
    except Exception as e:
        logging.error(traceback.format_exc())
        return func.HttpResponse(str(e), status_code=500)


def get_hourly_forecast_wrapper(req: func.HttpRequest) -> func.HttpResponse:
    try:
        start_date = datetime.strptime(req.params.get('start_date'), '%Y-%m-%d').date() # type: ignore
        end_date = datetime.strptime(req.params.get('end_date'), '%Y-%m-%d').date() # type: ignore
        res = get_hourly_forecast(start_date, end_date, OpenMeteoClient.DEFAULT_HOURLY_PARAMS)

        hourly = res['hourly'] # type: ignore
        units = res['hourly_units'] # type: ignore
        ret = []
        for i, time in enumerate(hourly['time']):
            entry = {
                'time': time,
                'weather': OpenMeteoClient.WEATHERCODE_MSP.get(hourly['weathercode'][i], '不明')
            }
            for key in OpenMeteoClient.DEFAULT_HOURLY_PARAMS:
                entry[key] = f'{hourly[key][i]}{units[key]}'
            ret.append(entry)
        return func.HttpResponse(
            body=json.dumps(ret, ensure_ascii=False, default=str),
            status_code=200,
            mimetype='application/json'
        )
    except Exception as e:
        logging.error(traceback.format_exc())
        return func.HttpResponse(str(e), status_code=500)


def get_daily_forecast(start_date, end_date, daily_params):
    try:
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'daily': daily_params
        }
        return openmeteo.forecast(**params)
    except Exception as e:
        logging.error(traceback.format_exc())
        return None
    

def get_hourly_forecast(start_date, end_date, hourly_params):
    try:
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'hourly': hourly_params
        }
        return openmeteo.forecast(**params)
    except Exception as e:
        logging.error(traceback.format_exc())
        return None