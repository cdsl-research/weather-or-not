const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const API_KEY = process.env.OPENWEATHER_API_KEY;

if (!API_KEY) {
  console.error('エラー: 環境変数 OPENWEATHER_API_KEY が設定されていません。');
  console.error('.envファイルを作成し、APIキーを設定してください。');
  process.exit(1);
}

// UNIXタイムスタンプを日本時間の文字列に変換する関数
function convertToJapaneseTime(timestamp) {
  const date = new Date(timestamp * 1000); // ミリ秒に変換
  return date.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });
}

// 日付文字列をUNIXタイムスタンプに変換する関数
function dateToUnixTimestamp(dateString) {
  const date = new Date(dateString);
  return Math.floor(date.getTime() / 1000);
}

async function fetchDailyHistoricalWeatherData(dateString) {
  try {
    // 指定された日付の開始時刻（0:00）を取得
    const startDate = new Date(dateString);
    startDate.setHours(0, 0, 0, 0);
    
    const dailyData = [];
    const errors = [];
    
    console.log(`${dateString} の1日分のデータを取得中...`);
    
    // 1時間ごとに24回データを取得
    for (let hour = 0; hour < 24; hour++) {
      const currentDate = new Date(startDate);
      currentDate.setHours(hour);
      const timestamp = Math.floor(currentDate.getTime() / 1000);
      
      const URL = `https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=35.656&lon=139.324&dt=${timestamp}&appid=${API_KEY}&lang=ja&units=metric`;
      
      try {
        console.log(`${hour}:00 のデータを取得中...`);
        const response = await axios.get(URL);
        const data = response.data.data[0];
        
        dailyData.push({
          hour: hour,
          time: convertToJapaneseTime(timestamp),
          unix_timestamp: timestamp,
          temp: data.temp,
          feels_like: data.feels_like,
          humidity: data.humidity,
          pressure: data.pressure,
          wind_speed: data.wind_speed,
          weather: data.weather[0],
          clouds: data.clouds,
          visibility: data.visibility,
          dew_point: data.dew_point,
          uvi: data.uvi
        });
        
        // API制限を避けるため少し待機
        await new Promise(resolve => setTimeout(resolve, 1000));
        
      } catch (hourError) {
        console.error(`${hour}:00 のデータ取得に失敗:`, hourError.message);
        errors.push({ hour, error: hourError.message });
      }
    }
    
    // 日の出・日の入り時刻を最初のデータから取得
    let sunInfo = {};
    if (dailyData.length > 0) {
      const firstDataTimestamp = dailyData[0].unix_timestamp;
      const sunURL = `https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=35.656&lon=139.324&dt=${firstDataTimestamp}&appid=${API_KEY}&lang=ja&units=metric`;
      
      try {
        const sunResponse = await axios.get(sunURL);
        const sunData = sunResponse.data.data[0];
        sunInfo = {
          sunrise: sunData.sunrise,
          sunrise_time: convertToJapaneseTime(sunData.sunrise),
          sunset: sunData.sunset,
          sunset_time: convertToJapaneseTime(sunData.sunset)
        };
      } catch (sunError) {
        console.error('日の出・日の入り情報の取得に失敗:', sunError.message);
      }
    }
    
    // 統計情報の計算
    const stats = calculateDailyStats(dailyData);
    
    const weatherInfo = {
      requested_date: dateString,
      data_points: dailyData.length,
      errors: errors,
      sun_info: sunInfo,
      daily_statistics: stats,
      hourly_data: dailyData
    };

    // 結果をJSONファイルに保存
    // 出力ディレクトリの作成
    const outputDir = path.join('outputs', dateString);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const filename = `daily_weather_${dateString}.json`;
    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(
      filepath,
      JSON.stringify(weatherInfo, null, 2)
    );
    console.log(
      `${dateString} の1日分の天気データを ${filepath} に保存しました。`
    );
    console.log(`取得成功: ${dailyData.length}件, エラー: ${errors.length}件`);
    
  } catch (error) {
    console.error('エラーが発生しました:', error.message);
    if (error.response) {
      console.error('レスポンスデータ:', error.response.data);
      if (error.response.status === 401) {
        console.error('APIキーが無効か、Time Machine APIへのアクセス権限がありません。');
      }
    }
  }
}

// 1日の統計情報を計算する関数
function calculateDailyStats(dailyData) {
  if (dailyData.length === 0) return {};
  
  const temps = dailyData.map(d => d.temp);
  const humidities = dailyData.map(d => d.humidity);
  const pressures = dailyData.map(d => d.pressure);
  const windSpeeds = dailyData.map(d => d.wind_speed);
  
  return {
    temperature: {
      max: Math.max(...temps),
      min: Math.min(...temps),
      avg: temps.reduce((a, b) => a + b, 0) / temps.length
    },
    humidity: {
      max: Math.max(...humidities),
      min: Math.min(...humidities),
      avg: humidities.reduce((a, b) => a + b, 0) / humidities.length
    },
    pressure: {
      max: Math.max(...pressures),
      min: Math.min(...pressures),
      avg: pressures.reduce((a, b) => a + b, 0) / pressures.length
    },
    wind_speed: {
      max: Math.max(...windSpeeds),
      min: Math.min(...windSpeeds),
      avg: windSpeeds.reduce((a, b) => a + b, 0) / windSpeeds.length
    }
  };
}

// コマンドライン引数から日付を取得
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('使用方法: node fetch_historical_weather.js "YYYY-MM-DD"');
  console.log('例: node fetch_historical_weather.js "2025-01-05"');
  process.exit(1);
}

const dateString = args[0];
fetchDailyHistoricalWeatherData(dateString);