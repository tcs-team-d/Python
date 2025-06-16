import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.ensemble import RandomForestRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os
import joblib



df = pd.read_csv('data/20240401_20250401.csv')
targets = ['pale_ale', 'lager', 'ipa', 'white_beer', 'dark_beer', 'fruit_beer']
x = df.drop(columns=targets+['date'])
y = df[targets]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# grid_params = {
#     'n_estimators': [100, 200],
#     'max_depth': [5, 10],
#     'max_features': [0.5, 0.75, 1],
#     'min_samples_leaf': [1, 3, 5]
# }
grid_params = {
    'depth': [4, 5, 6],
    'learning_rate': [0.05, 0.1, 0.3],
    'iterations': [100, 200, 300],
    'l2_leaf_reg': [3, 5, 10],
    'subsample': [0.7, 0.85, 1],
    'early_stopping_rounds': [50]
}
for target in targets:
    print(f'\n=== {target} ===')
    # model = RandomForestRegressor(random_state=42)
    model = CatBoostRegressor(verbose=0, random_seed=42)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(model, grid_params, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1)
    grid.fit(x_train, y_train[target])

    best_model = grid.best_estimator_
    os.makedirs('checkpoints', exist_ok=True)
    joblib.dump(best_model, f'checkpoints/model_{target}.joblib')

    y_train_pred = best_model.predict(x_train)
    y_test_pred = best_model.predict(x_test)
    train_mae = mean_absolute_error(y_train[target], y_train_pred)
    test_mae = mean_absolute_error(y_test[target], y_test_pred)
    train_r2 = r2_score(y_train[target], y_train_pred)
    test_r2 = r2_score(y_test[target], y_test_pred)

    print(f'Train MAE: {train_mae:.3f} R2: {train_r2:.3f}    Test MAE: {test_mae:.3f} R2: {test_r2:.3f}')
    print('Best Params:', grid.best_params_)
