# 機械学習モデル

## 前提条件

過去1年分の売上データ```クラフトビール専門店_売上データ_2024年4月-2025年4月 (曜日ありデータ).csv```を```data/```ディレクトリ内に配置する

## 環境設定

仮想環境作成 (python version = 3.11 推奨)

```cmd
cd mllab
python -m venv .mlvenv
source .mlvenv/Scripts/activate
pip install -r requirements.txt
```

## データ前処理

売上データの整形、天気データの取得、機械学習用の整形済データを保存

```cmd
python preprocess.py
```

## データ分析

説明変数間にはいくつか相関の高いものがある(e.g. rain_sum と precipitation_hours など)
学習時に適宜取捨選択する

今回は特に説明変数と目的変数間の相関関係をプロットして確かめる

```cmd
python analyze.py
```

いくつか相関がみられるが、全体的にデータの関係が線形でない(プロットがあまり比例の関係になく、広がっている)
したがって、学習モデルは非線形をモデリングできるDecitoin Treeのようなものをベースにする

## 学習

学習時にconfigファイルを引数に指定することで、使用する学習モデルやGridSearchのパラメータを指定する

e.g. RandomForestRegressor

```cmd
python train.py train_configs/randomforest_default.yaml
```

checkpointsディレクトリに学習済モデルが保存される

このとき、学習済モデルはtargetごとに計6つ保存される

モデルごとのbest paramsや検証スコアは同ディレクトリ内にconfig.yamlとして保存される
