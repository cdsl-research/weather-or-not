# Weather Or Not

OpenWeather API を使用して過去の天気データを取得し,温度変化をグラフ化するプログラムです.

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

`.env`ファイルを編集し,OpenWeather API キーを設定してください.

## 使用方法

### 天気データの取得とグラフ化（推奨）

Python スクリプトから自動的にデータ取得とグラフ化を行います：

```bash
# 今日のデータを取得・グラフ化
python plot_temperature.py

# 特定の日付のデータを取得・グラフ化
python plot_temperature.py 2025-01-05
```

<img width="612" height="416" alt="image" src="https://github.com/user-attachments/assets/7a95ccd7-b9dd-4276-a587-c4cc25a40485" />

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

<img width="307" height="932" alt="image" src="https://github.com/user-attachments/assets/9ec380c0-db87-4b76-b713-c6933e8382b7" />

- `outputs/YYYY-MM-DD/temperature_graph_YYYY-MM-DD.png` - 温度変化グラフ

<img width="1202" height="797" alt="image" src="https://github.com/user-attachments/assets/56b86672-d4af-476a-a101-b4e37efb515f" />

- `outputs/YYYY-MM-DD/weather_details_YYYY-MM-DD.png` - 詳細天気グラフ（オプション）

<img width="1500" height="908" alt="image" src="https://github.com/user-attachments/assets/0a1538f4-95a5-45f0-ae02-07a851e6158e" />


## API 制限事項

- API キーに応じたレート制限あり
- 過去 5 日間のデータのみ取得可能
