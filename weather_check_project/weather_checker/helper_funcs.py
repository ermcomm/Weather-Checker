from datetime import datetime, timezone, timedelta
import requests
from weather_checker.models import api_configs


def convert_time(unix_time, timezone_seconds):
    '''convert unix timestamps returned by api to time, applies appropriate timezone (received offset is in seconds)'''
    return datetime.fromtimestamp(
        unix_time, tz=timezone(timedelta(hours=timezone_seconds/3600))).time()


def convert_date_time(unix_time, timezone_seconds):
    '''returns date_time with timzone from provided unix time.  Use this to avoid timezone mismatches with django's auto timezone in templates'''
    return datetime.fromtimestamp(
        unix_time, tz=timezone(timedelta(hours=timezone_seconds/3600)))


def get_coordinates(searched_address):
    '''convert an address to lat and lon via mapbox api'''
    # get mapbox api key
    mapbox_api_key = api_configs.objects.get(
        api='mapbox').api_token  # TODO: raise entryu not found exception and redirect if api key is not loaded
    # make api call with address
    api_call = f"""https://api.mapbox.com/geocoding/v5/mapbox.places/{searched_address}.json?proximity=-73.990593%2C40.740121&types=place%2Cpostcode%2Caddress&access_token={mapbox_api_key}"""
    mapbox_result = requests.get(api_call).json()
    print('nnnnnnnnnnnnnnnnnn', mapbox_result)
    # grab coords of first set rteturned.
    coords = mapbox_result['features'][0]['center']
    address_name = mapbox_result['features'][0]['place_name']
    # get next best guesses provided by mapbox incase the address provided is not correct or incomplete
    next_best_guesses = [('Select an address here....', '')] + [(address['place_name'], address['place_name'])
                                                                for address in mapbox_result['features'][1:]]
    return coords, address_name, next_best_guesses, mapbox_api_key


def get_weather_info(coords, units):
    '''Get weather info for a set of coordinates'''
    open_weather_api_key = api_configs.objects.get(api='openweather').api_token
    current_weather_api_call = f"""https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={open_weather_api_key}&units=metric"""
    open_weather_results_current = requests.get(
        current_weather_api_call).json()
    hourly_forecast_weather_api_call = f"""https://api.openweathermap.org/data/2.5/forecast?lat={coords[0]}&lon={coords[1]}&appid={open_weather_api_key}&units=metric"""
    open_weather_results_forecast_hourly = requests.get(
        hourly_forecast_weather_api_call).json()
    # set timezone var
    forecast_timezone = open_weather_results_forecast_hourly['city']['timezone']
    # 5 day 3-hourly forecast for line chart
    five_day_forecast = open_weather_results_forecast_hourly['list']
    # convert all times to timestamp (date and time) with timezone
    for forecast in five_day_forecast:
        forecast['dt'] = convert_date_time(forecast['dt'], forecast_timezone)
    # grab only the first 8 predictions (=24 hours) for 24 H forecast
    open_weather_results_forecast_hourly = open_weather_results_forecast_hourly['list'][:12]
    # for forecast in open_weather_results_forecast_hourly:
    #     print(forecast)
    #     forecast['dt'] = convert_date_time(forecast['dt'], forecast_timezone)
    # convert sunrise/sunset times from unix to local (grab address timezone and adjust)
    open_weather_results_current['sys']['sunrise'] = convert_time(
        open_weather_results_current['sys']['sunrise'], open_weather_results_current['timezone'])
    open_weather_results_current['sys']['sunset'] = convert_time(
        open_weather_results_current['sys']['sunset'], open_weather_results_current['timezone'])
    return open_weather_results_current, open_weather_results_forecast_hourly, five_day_forecast


def reverse_geocode(coords):
    """Get address from coords received from map drag/drop"""
    print(coords, type(coords))
    # convert from str received from js to list
    coords = coords.replace('[', '').replace(']', '').split(",")
    print(coords)
    mapbox_api_key = api_configs.objects.get(
        api='mapbox').api_token
    api_call = f'''https://api.mapbox.com/geocoding/v5/mapbox.places/{coords[0].replace("'", "").strip()},{coords[1].replace("'", "").strip()}.json?types=place%2Cpostcode%2Caddress&limit=1&access_token={mapbox_api_key}'''
    address = requests.get(api_call).json()['features'][0]['place_name']
    print(api_call)
    print(address)
    print('xxxxxxxxxxx')

    return(address)
