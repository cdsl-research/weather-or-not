# Weather Or Not

OpenWeather API を使用して過去の天気データを取得し、温度変化をグラフ化するプログラムです。

## 機能

- 指定日の 1 時間ごとの天気データを取得（24 時間分）
- 温度変化のグラフを自動生成
- 湿度、気圧、風速などの詳細データの可視化
- 日本語対応

## 必要な環境

- Node.js (v14 以降)
- Python 3.7 以降
- 必要なパッケージ：
  - Node.js: axios
  - Python: matplotlib, numpy

## セットアップ

1. リポジトリをクローン

```bash
git clone [repository-url]
cd fetch_visualyze_weather
```

2. Node.js パッケージのインストール

```bash
npm install
```

3. Python パッケージのインストール

```bash
pip install matplotlib numpy
```

4. 環境変数の設定

```bash
cp .env.example .env
```

`.env`ファイルを編集し、OpenWeather API キーを設定してください。

## 使用方法

### 天気データの取得とグラフ化（推奨）

Python スクリプトから自動的にデータ取得とグラフ化を行います：

```bash
# 今日のデータを取得・グラフ化
python plot_temperature.py

# 特定の日付のデータを取得・グラフ化
python plot_temperature.py 2025-01-05
```

### データ取得のみ

```bash
node fetch_historical_weather.js "2025-01-05"
```

### 既存データのグラフ化

```bash
python plot_temperature.py daily_weather_2025-01-05.json
```

## 出力ファイル

- `outputs/YYYY-MM-DD/daily_weather_YYYY-MM-DD.json` - 取得した天気データ
- `outputs/YYYY-MM-DD/temperature_graph_YYYY-MM-DD.png` - 温度変化グラフ
- `outputs/YYYY-MM-DD/weather_details_YYYY-MM-DD.png` - 詳細天気グラフ（オプション）

## API 制限事項

- OpenWeather API の Time Machine 機能を使用
- API キーに応じたレート制限あり
- 過去 5 日間のデータのみ取得可能

## ライセンス

MIT License
