# HOPCAST

## Prepare trained ML models for HOPCAST prediction API

mllab/ ディレクトリ内のREADMEに従い、機械学習を完了する。

その後、学習済モデルのフォルダをプロジェクトディレクトリ直下に移動する。

今回はRandomForestRegressorモデルをAzure Functonsにデプロイする。

```cmd
Python/ 
 - checkpoints/randomforest_default/
```

## Azure Functions

仮想環境を用意する。

```cmd
py -3.11 -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

デプロイが完了したら、以下のエンドポイントからAPIを呼び出せる。

### APIs' endpoints

#### Get daily forecast

start_dateとend_dateに適切な日付を入れて

```cmd
https://d-hopcast-func-f2csfuaaf3fpe9g7.japaneast-01.azurewebsites.net/api/forecasts/daily?start_date=2025-06-24&end_date=2025-06-30
```

#### Get hourly forecast

start_dateとend_dateに適切な日付を入れて

```cmd
https://d-hopcast-func-f2csfuaaf3fpe9g7.japaneast-01.azurewebsites.net/api/forecasts/hourly?start_date=2025-06-24&end_date=2025-06-30
```

#### Get demands of beers

start_dateとend_dateに適切な日付を入れて

```cmd
https://d-hopcast-func-f2csfuaaf3fpe9g7.japaneast-01.azurewebsites.net/api/demands?start_date=2025-06-24&end_date=2025-06-30
```

#### [TIMER] Automatically posts weather record to DB

毎日23:00(JST)に天気データがDBに追加される

no endpoint
