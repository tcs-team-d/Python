import azure.functions as func
from modules.weather import get_daily_forecast_wrapper, get_hourly_forecast_wrapper
from modules.predictions import get_demand


 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

 
@app.route(route='forecasts/daily', methods=['GET'])
@app.function_name(name='get_daily_forecast')
def _get_daily_forecast(req: func.HttpRequest) -> func.HttpResponse:
    return get_daily_forecast_wrapper(req)


@app.route(route='forecasts/hourly', methods=['GET'])
@app.function_name(name='get_hourly_forecast')
def _get_hourly_forecast(req: func.HttpRequest) -> func.HttpResponse:
    return get_hourly_forecast_wrapper(req)


@app.route(route='demands', methods=['GET'])
@app.function_name(name='get_demand')
def _get_demand (req: func.HttpRequest) -> func.HttpResponse:
    return get_demand(req)