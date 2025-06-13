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
 
    url = 'https://archive-api.open-meteo.com/v1/archive'
    params = {
        'latitude': 35.68,
        'longitude': 139.76,
        'start_date': '2024-04-01',
        'end_date': '2025-03-31',
        'daily': 'temperature_2m_mean,relative_humidity_2m_mean,weathercode',
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
 