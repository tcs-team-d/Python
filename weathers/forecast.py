import azure.functions as func
import json
from datetime import datetime
import logging
import traceback
from weathers.openmeteo import OpenMeteoClient



def get_weekly_forecast(req: func.HttpRequest) -> func.HttpResponse:
    try:
        omc = OpenMeteoClient()
        params = {
            # the range of start_date and end_date will be set 7 days from today
            'daily': ['weathercode', 'temperature_2m_mean', 'relative_humidity_2m_mean']
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
