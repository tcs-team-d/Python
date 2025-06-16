import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os
import sys
import yaml
import joblib



config_file = sys.argv[1]
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

df = pd.read_csv('data/20240401_20250401.csv')
targets = ['pale_ale', 'lager', 'ipa', 'white_beer', 'dark_beer', 'fruit_beer']
x = df[config['independent_variables']]
y = df[targets]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

for target in targets:
    print(f'\n=== {target} ===')
    assert config['model'] == 'RandomForestRegressor' or config['model'] == 'CatBoostRegressor' or config['model'] == 'SVR'
    if config['model'] == 'RandomForestRegressor':
        model = RandomForestRegressor(random_state=42)
    if config['model'] == 'CatBoostRegressor':
        model = CatBoostRegressor(verbose=0, random_seed=42)
    if config['model'] == 'SVR':
        model = SVR(kernel='rbf')
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(model, config['grid_params'], cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1) # type: ignore
    grid.fit(x_train, y_train[target])

    best_model = grid.best_estimator_
    os.makedirs(config['savedir'], exist_ok=True)
    joblib.dump(best_model, os.path.join(config['savedir'], f'model_{target}.joblib'))
    with open(os.path.join(config['savedir'], 'config.yaml'), 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    y_train_pred = best_model.predict(x_train) # type: ignore
    y_test_pred = best_model.predict(x_test) # type: ignore
    train_mae = mean_absolute_error(y_train[target], y_train_pred)
    test_mae = mean_absolute_error(y_test[target], y_test_pred)
    train_r2 = r2_score(y_train[target], y_train_pred)
    test_r2 = r2_score(y_test[target], y_test_pred)

    print(f'Train MAE: {train_mae:.3f} R2: {train_r2:.3f}    Test MAE: {test_mae:.3f} R2: {test_r2:.3f}')
    print('Best Params:', grid.best_params_)
