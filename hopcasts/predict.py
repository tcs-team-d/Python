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
 


targets = ['pale_ale', 'lager', 'ipa', 'white_beer', 'dark_beer', 'fruit_beer']
checkpoinds_path = os.path.join('hopcasts', 'catboost_default')
models = {
    target: joblib.load(os.path.join(checkpoinds_path, f'model_{target}.joblib'))
    for target in targets
}
with open(os.path.join(checkpoinds_path, 'config.yaml'), 'r') as file:
    config = yaml.safe_load(file)


def get_weekly_demands(req: func.HttpRequest) -> func.HttpResponse:
    try:           
        omc = OpenMeteoClient()
        start_date = datetime.strptime(req.params.get('start_date'), '%Y-%m-%d').date() # type: ignore
        end_date = datetime.strptime(req.params.get('end_date'), '%Y-%m-%d').date() # type: ignore
        params = {
            'start_date': start_date,
            'end_date': end_date,
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
            **{col: res['daily'][col][i] for col in config['independent_variables'][2:]} # type:ignore
        }
        for i, date in enumerate(res['daily']['time']) # type:ignore
    ])

    predictions = {target: models[target].predict(x) for target in targets}
    res = [
        {
            'date': date,
            **{target: predictions[target][i] for target in targets}
        } for i, date in enumerate(res['daily']['time']) # type: ignore
    ]
    print(res)
    return func.HttpResponse(
        body=json.dumps(res, ensure_ascii=False, indent=2),
        status_code=200,
        mimetype='application/json'      
    )