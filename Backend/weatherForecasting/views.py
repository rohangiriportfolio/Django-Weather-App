from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from prophet import Prophet
import matplotlib.pyplot as plt
from io import StringIO

@csrf_exempt
def home_page(request):
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    if request.content_type != "application/json":
            return JsonResponse({"error": "Invalid content type. Use application/json"}, status=400)
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    startDate = data.get("startDate")
    endDate = data.get("endDate")
    lon = data.get("lon")
    lat = data.get("lat")
    if startDate is None or endDate is None or lon is None or lat is None:
        return JsonResponse({"error": "Missing required parameters"}, status=400)
    try:
        endDate = int(endDate) 
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return JsonResponse({"error": "Invalid number format"}, status=400)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2024-01-01",
        "end_date": startDate,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "rain", "snowfall", "surface_pressure", "cloud_cover", "wind_speed_100m", "wind_direction_100m"]
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    hourly_rain = hourly.Variables(4).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(6).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(7).ValuesAsNumpy()
    hourly_wind_speed_100m = hourly.Variables(8).ValuesAsNumpy()
    hourly_wind_direction_100m = hourly.Variables(9).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["rain"] = hourly_rain
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
    hourly_data["wind_direction_100m"] = hourly_wind_direction_100m

    df = pd.DataFrame(data = hourly_data)

    df["date"] = pd.to_datetime(df["date"])

    df["date"] = df["date"].dt.date

    mean_df = df.groupby("date").mean().reset_index()

    # mean_df.tail(3)
    mean_df_cpy=mean_df.copy()
    for col in ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "rain", "snowfall", "surface_pressure", "cloud_cover", "wind_speed_100m", "wind_direction_100m"]:
        col_mean = mean_df_cpy[mean_df_cpy[col] != 0][col].mean()  # Compute mean excluding zeros
        mean_df_cpy[col].fillna(col_mean, inplace=True)
    df=mean_df_cpy
    df.info()
    df["date"] = pd.to_datetime(df["date"], format = '%Y-%m-%d')
    df['year'] = df['date'].dt.year
    df["month"] = df["date"].dt.month
    # List of features to forecast
    features = ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "rain", "snowfall", "surface_pressure", "cloud_cover", "wind_speed_100m", "wind_direction_100m"]


    final_forecast = pd.DataFrame()

    for feature in features:
        forecast_data = df.rename(columns={"date": "ds", feature: "y"})
        
        model = Prophet()
        model.fit(forecast_data)
        
        future = model.make_future_dataframe(periods=endDate)
        predictions = model.predict(future)
        
        predictions = predictions.tail(endDate)[["ds", "yhat"]] 
        if final_forecast.empty:
            final_forecast["Date time"] = predictions["ds"]  # Add datetime column once

        final_forecast[feature] = predictions["yhat"]  # Store yhat for each feature

        final_forecast.to_csv("Final_forecast.csv", index=False)
        # print("Forecasting completed.")
        
        # Plot the forecast
        # fig = model.plot(predictions)
        # plt.title(f"Forecast for {feature}")
        # plt.show()

    print("Forecasting completed for all features.")
    final_forecast_json = final_forecast.to_dict(orient="records")
    return JsonResponse({"forecast": final_forecast_json}, safe=False)

