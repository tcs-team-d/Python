import azure.functions as func
import os
import json
import logging
import traceback
from datetime import datetime
import yaml
import joblib
import numpy as np
from modules import weather

 

targets = ['pale_ale', 'lager', 'ipa', 'white_beer', 'dark_beer', 'fruit_beer']

_loaded_models = None
_loaded_config = None

def load_models():
    global _loaded_models
    global _loaded_config
    
    checkpoinds_path = os.path.join('checkpoints', 'randomforest_default')
    if _loaded_models is None:
        _loaded_models = {
            target: joblib.load(os.path.join(checkpoinds_path, f'model_{target}.joblib'))
            for target in targets
        }
    if _loaded_config is None:
        with open(os.path.join(checkpoinds_path, 'config.yaml'), 'r') as file:
            _loaded_config = yaml.safe_load(file)
    return _loaded_models, _loaded_config


def get_demand(req: func.HttpRequest) -> func.HttpResponse:
    models, config = load_models()
    
    try:           
        start_date = datetime.strptime(req.params.get('start_date'), '%Y-%m-%d').date() # type: ignore
        end_date = datetime.strptime(req.params.get('end_date'), '%Y-%m-%d').date() # type: ignore
        res = weather.get_daily_forecast(start_date, end_date, config['independent_variables'][2:])
    except Exception as e:
        logging.error(traceback.format_exc())
        return func.HttpResponse(str(e), status_code=500)

    try:
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
        return func.HttpResponse(
            body=json.dumps(res, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype='application/json'      
        )
    except Exception as e:
        logging.error(traceback.format_exc())
        return func.HttpResponse(str(e), status_code=500)