import os
import sys
import yaml
import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from catboost import CatBoostRegressor



config_file = sys.argv[1]
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

assert (
    config['model'] == 'RandomForestRegressor' or 
    config['model'] == 'CatBoostRegressor' or 
    config['model'] == 'SVR'
)

df = pd.read_csv('data/20240401_20250401.csv')
targets = ['pale_ale', 'lager', 'ipa', 'white_beer', 'dark_beer', 'fruit_beer']
x = df[config['independent_variables']]
y = df[targets]

log = {}
for target in targets:
    print(f'\n=== {target} ===')
    if config['model'] == 'RandomForestRegressor':
        model = RandomForestRegressor(random_state=42)
    if config['model'] == 'CatBoostRegressor':
        model = CatBoostRegressor(verbose=0, random_seed=42)
    if config['model'] == 'SVR':
        model = SVR(kernel='rbf')
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(
        model, # type: ignore
        config['grid_params'],
        cv=cv,
        scoring=config['scoring'],
        refit=config['refit'],
        n_jobs=-1, # may not be fully reproducible when using parallel processing (n_jobs ≠ 1)
        return_train_score=True
    )
    grid.fit(x, y[target])

    results = grid.cv_results_
    best_index = grid.best_index_
    print('Best Params:', grid.best_params_)
    log_scores = {}
    for metric in config['scoring']:
        train_score = results[f'mean_train_{metric}'][best_index]
        val_score = results[f'mean_test_{metric}'][best_index]
        log_scores[metric] = {'train': float(train_score), 'val': float(val_score)}
        print(f'{metric}: train={train_score:.4f} val={val_score:.4f}')
    log[target] = {'best_params': grid.best_params_, 'scores': log_scores}
    
    best_model = grid.best_estimator_
    os.makedirs(config['savedir'], exist_ok=True)
    joblib.dump(best_model, os.path.join(config['savedir'], f'model_{target}.joblib'))

with open(os.path.join(config['savedir'], 'config.yaml'), 'w') as f:
    yaml.dump({**config, **{'log': log}}, f, default_flow_style=False, sort_keys=False)
