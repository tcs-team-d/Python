import azure.functions as func
from modules.weather import get_daily_forecast_wrapper, get_hourly_forecast_wrapper, post_daily_forecast
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


@app.function_name(name='post_daily_forecast')
@app.schedule(
    schedule='0 0 14 * * *', # JST 23:00 = UTC 14:00
    arg_name='mytimer',
    use_monitor=False,
    run_on_startup=False
    # run_on_startup=True # for debug
)
def _post_daily_forecast(mytimer: func.TimerRequest) -> None:
    post_daily_forecast(mytimer)