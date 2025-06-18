import azure.functions as func
import os
import json
import logging
import traceback
from datetime import datetime, timedelta
import yaml
import joblib
import numpy as np
from weathers.openmeteo import OpenMeteoClient

 

targets = ['pale_ale', 'lager', 'ipa', 'white_beer', 'dark_beer', 'fruit_beer']

_loaded_models = None
_loaded_config = None

def load_models():
    global _loaded_models
    global _loaded_config
    
    checkpoinds_path = os.path.join('hopcasts', 'checkpoints', 'randomforest_default')
    if _loaded_models is None:
        _loaded_models = {
            target: joblib.load(os.path.join(checkpoinds_path, f'model_{target}.joblib'))
            for target in targets
        }
    if _loaded_config is None:
        with open(os.path.join(checkpoinds_path, 'config.yaml'), 'r') as file:
            _loaded_config = yaml.safe_load(file)
    return _loaded_models, _loaded_config


def get_weekly_demands(req: func.HttpRequest) -> func.HttpResponse:
    models, config = load_models()
    print(config['model'])
    
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

    x = np.array([
        [
            datetime.fromisoformat(date).weekday(),
            datetime.fromisoformat(date).month,
            *[res['daily'][col][i] for col in config['independent_variables'][2:]]  # type: ignore
        ]
        for i, date in enumerate(res['daily']['time'])  # type: ignore
    ])
    predictions = {target: models[target].predict(x) for target in targets}
    res = [
        {
            'date': date,
            **{target: predictions[target][i] for target in targets}
        } for i, date in enumerate(res['daily']['time']) # type: ignore
    ]
    # print(res)
    return func.HttpResponse(
        body=json.dumps(res, ensure_ascii=False, indent=2),
        status_code=200,
        mimetype='application/json'      
    )