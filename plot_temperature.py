import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, date
import numpy as np
import sys
import os
import subprocess

# 日本語フォントの設定
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

def load_weather_data(filename):
    """JSONファイルから天気データを読み込む"""
    try:
        # 既存の出力構造をチェック
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 古い形式のファイルパスも試す（後方互換性のため）
            old_path = os.path.basename(filename)
            if os.path.exists(old_path):
                with open(old_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                raise FileNotFoundError(filename)
    except FileNotFoundError:
        print(f"エラー: ファイル '{filename}' が見つかりません。")
        print("まず fetch_historical_weather.js を実行してデータを取得してください。")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"エラー: ファイル '{filename}' の形式が正しくありません。")
        sys.exit(1)

def plot_temperature(weather_data):
    """Plot temperature data"""
    # Extract hourly temperature data
    hourly_data = weather_data['hourly_data']
    hours = []
    temps = []
    
    for data in hourly_data:
        hours.append(data['hour'])
        temps.append(data['temp'])
    
    # Get statistics
    stats = weather_data['daily_statistics']['temperature']
    
    # Create graph
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot temperature
    ax.plot(hours, temps, 'b-', linewidth=2, marker='o', markersize=6, label='Temperature')
    
    # Max/Min/Average lines
    ax.axhline(y=stats['max'], color='red', linestyle=':', alpha=0.5, label=f'Max: {stats["max"]:.1f}°C')
    ax.axhline(y=stats['min'], color='blue', linestyle=':', alpha=0.5, label=f'Min: {stats["min"]:.1f}°C')
    ax.axhline(y=stats['avg'], color='green', linestyle=':', alpha=0.5, label=f'Average: {stats["avg"]:.1f}°C')
    
    # Graph decoration
    ax.set_xlabel('Time', fontsize=24)
    ax.set_ylabel('Temperature (°C)', fontsize=24)
    # ax.set_title(f'Temperature on {weather_data["requested_date"]}', fontsize=16, fontweight='bold')
    
    # X-axis settings
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f'{h}:00' for h in range(0, 24, 2)])
    ax.grid(True, alpha=0.3)
    
    # Legend
    ax.legend(loc='best', fontsize=20)
    
    # Y-axis range starting from 0
    y_max = max(temps) + 5
    ax.set_ylim(0, y_max)
    
    ax.tick_params(labelsize=20)
    
    # 枠線を削除（上と右のみ削除、下と左の軸は残す）
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Time zone background colors
    # ax.axvspan(0, 6, alpha=0.1)
    # ax.axvspan(6, 12, alpha=0.1)
    # ax.axvspan(12, 18, alpha=0.1)
    # ax.axvspan(18, 24, alpha=0.1)
    
    plt.tight_layout()
    
    # グラフの保存（背景透過）
    # 出力ディレクトリの作成
    output_dir = os.path.join('outputs', weather_data["requested_date"])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_filename = f'temperature_graph_{weather_data["requested_date"]}.png'
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f"グラフを '{output_path}' に保存しました。")
    
    # グラフの表示
    plt.show()

def plot_weather_details(weather_data):
    """Create detailed weather data graphs"""
    hourly_data = weather_data['hourly_data']
    hours = [data['hour'] for data in hourly_data]
    
    # Create 4 subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'Weather Details on {weather_data["requested_date"]}', fontsize=20, fontweight='bold')
    
    # 1. Temperature with weather conditions
    temps = [data['temp'] for data in hourly_data]
    ax1.plot(hours, temps, 'b-', linewidth=2, marker='o', label='Temperature')
    
    # Add weather conditions as text annotations for all hours
    for i, data in enumerate(hourly_data):
        # Get weather main description in English
        weather_main = data['weather']['main']  # This gives main weather type in English
        # Position text slightly above the temperature point
        ax1.annotate(weather_main, 
                    xy=(data['hour'], data['temp']), 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    ha='center',
                    fontsize=7,
                    rotation=45,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_title('Temperature with Weather Conditions')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(0, 24, 3))
    ax1.set_xticklabels([f'{h}:00' for h in range(0, 24, 3)])
    ax1.set_ylim(0, max(temps) + 10)  # Extra space for annotations
    
    # 2. Humidity
    humidity = [data['humidity'] for data in hourly_data]
    ax2.plot(hours, humidity, 'g-', linewidth=2, marker='o')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Humidity (%)')
    ax2.set_title('Humidity')
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(range(0, 24, 3))
    ax2.set_xticklabels([f'{h}:00' for h in range(0, 24, 3)])
    ax2.set_ylim(0, 100)
    
    # 3. Pressure
    pressure = [data['pressure'] for data in hourly_data]
    ax3.plot(hours, pressure, 'm-', linewidth=2, marker='o')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Pressure (hPa)')
    ax3.set_title('Atmospheric Pressure')
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(range(0, 24, 3))
    ax3.set_xticklabels([f'{h}:00' for h in range(0, 24, 3)])
    
    # 4. Wind Speed
    wind_speed = [data['wind_speed'] for data in hourly_data]
    ax4.plot(hours, wind_speed, 'c-', linewidth=2, marker='o')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Wind Speed (m/s)')
    ax4.set_title('Wind Speed')
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(range(0, 24, 3))
    ax4.set_xticklabels([f'{h}:00' for h in range(0, 24, 3)])
    ax4.set_ylim(0, max(wind_speed) + 2 if wind_speed else 10)
    
    # 各サブプロットの枠線を削除
    for ax in [ax1, ax2, ax3, ax4]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # グラフの保存（背景透過）
    # 出力ディレクトリの作成
    output_dir = os.path.join('outputs', weather_data["requested_date"])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_filename = f'weather_details_{weather_data["requested_date"]}.png'
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f"詳細グラフを '{output_path}' に保存しました。")
    
    plt.show()

def fetch_weather_data(date_str):
    """fetch_historical_weather.jsを実行してデータを取得"""
    print(f"{date_str} のデータを取得中...")
    
    # fetch_historical_weather.jsのパスを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    js_file = os.path.join(script_dir, 'fetch_historical_weather.js')
    
    # Node.jsスクリプトを実行
    try:
        result = subprocess.run(['node', js_file, date_str], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        print(result.stdout)
        if result.stderr:
            print("警告:", result.stderr)
        return os.path.join('outputs', date_str, f'daily_weather_{date_str}.json')
    except subprocess.CalledProcessError as e:
        print(f"エラー: データの取得に失敗しました")
        print(f"エラー出力: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("エラー: Node.jsがインストールされていないか、fetch_historical_weather.jsが見つかりません")
        sys.exit(1)

def main():
    # コマンドライン引数の処理
    filename = None
    
    if len(sys.argv) < 2:
        # 引数がない場合は今日の日付を使用
        date_str = date.today().strftime('%Y-%m-%d')
        print(f"日付が指定されていないため、今日の日付 ({date_str}) を使用します。")
        filename = fetch_weather_data(date_str)
    else:
        # 引数がJSONファイル名か日付かを判断
        arg = sys.argv[1]
        if arg.endswith('.json'):
            # JSONファイル名が指定された場合
            filename = arg
        else:
            # 日付が指定された場合
            date_str = arg
            # 日付の形式をチェック
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                print("エラー: 日付は YYYY-MM-DD 形式で指定してください")
                print("例: python plot_temperature.py 2025-01-05")
                sys.exit(1)
            
            # データを取得
            filename = fetch_weather_data(date_str)
    
    # データの読み込み
    weather_data = load_weather_data(filename)
    
    # データが正常に取得されているかチェック
    if not weather_data.get('hourly_data') or len(weather_data['hourly_data']) == 0:
        print("エラー: 時間ごとのデータが含まれていません。")
        sys.exit(1)
    
    print(f"データ読み込み完了: {weather_data['requested_date']}")
    print(f"データポイント数: {weather_data['data_points']}")
    
    # グラフの作成
    plot_temperature(weather_data)
    
    # 詳細グラフも作成するか確認
    create_details = input("\nCreate detailed weather graphs? (y/n): ")
    if create_details.lower() == 'y':
        plot_weather_details(weather_data)

if __name__ == "__main__":
    main()