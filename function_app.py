import azure.functions as func
from weathers.forecast import get_weekly_forecast, get_daily_forecast


 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

 
@app.route(route='forecasts', methods=['GET'])
@app.function_name(name='get_weekly_forecast')
def _get_weekly_forecast(req: func.HttpRequest) -> func.HttpResponse:
    return get_weekly_forecast(req)


@app.route(route='forecasts/{date}', methods=['GET'])
@app.function_name(name='get_daily_forecast')
def _get_daily_forecast(req: func.HttpRequest) -> func.HttpResponse:
    return get_daily_forecast(req)
