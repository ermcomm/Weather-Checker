from django.shortcuts import render
from weather_checker.forms import address_form
from weather_checker.models import weather_records
from django.views.generic.list import ListView
from django.contrib import messages
from datetime import datetime, timezone, timedelta
from weather_checker.helper_funcs import reverse_geocode, get_coordinates, get_weather_info
from django.http import HttpResponse
import json


def save_record(request):
    '''Ajax call to save record, return success/fail message'''
    if request.POST['save_record'] != '':
        results = json.loads(request.POST['save_record'])
        # create new record model object
        weather_records(
            time_of_search=results['time'],
            searched_address=results['address'],
            weather=results['weather_desc'],
            weather_icon=results['icon'],
            temp=results['weather']['temp'],
            feels_like_temp=results['weather']['feels_like'],
            wind_speed=results['weather_wind']['speed'],
            wind_direction=results['weather_wind']['deg'],
            humidity=results['weather']['humidity'],
            cloud_cover=results['weather_cloud']['all'],
            max_temp=results['weather']['temp_max'],
            min_temp=results['weather']['temp_min'],
        ).save()
        message = 'Succesfully saved record!'
    else:
        message = 'Can not save empty record.'
    return HttpResponse(message)


class view_records(ListView):
    '''show model view of all records'''
    model = weather_records


def landing(request):
    context = {}
    # TODO:  Add metric/imperial toggle to FE to set units, for now hardcoded metric
    units = 'metric'
    searched_by_map_marker = False
    if request.method == 'GET':
        # if the GET is not searching for a previously provided alt address from dropdown, use address in text-input
        if 'address_typed' in request.GET:
            searched_address = request.GET['address']
        elif 'alternative_addresses' in request.GET:
            searched_address = request.GET['alternative_addresses']
        # if searching on map marker coords (no adress provided only coords)
        elif 'map_marker_coords' in request.GET:
            searched_by_map_marker = True
            context['address_name'] = searched_address = reverse_geocode(
                request.GET['map_marker_coords'])
        else:  # catch-al, set searched address to default
            searched_address = '342 Jan Smuts ave, Hyde Park, Johannesburg'
        form = address_form(
            request.GET, searched_address=searched_address, alternative_addresses=[('', '')])  # set alternative addresses to blank so we can init form and validate received GET info
        if form.is_valid():
            if not searched_by_map_marker:  # if form submitted with typed address or drop-down alternative address
                context['coords'], context['address_name'], context['alternative_addresses'], context['mapbox_api_key'] = get_coordinates(
                    searched_address)
                context['current_weather'], context['hourly_forecast'], context['five_day_forecast'] = get_weather_info(
                    context['coords'], units)
            else:  # form submitted by map marker drag/drop, dont need to get coordinates via api, only get address from map coords
                context['current_weather'], context['hourly_forecast'], context['five_day_forecast'] = get_weather_info(
                    context['address_name'], units)
            form = address_form(
                request.GET, searched_address=searched_address, alternative_addresses=context['alternative_addresses'])  # re init form after validation with additional data for alternative address dropdown
        else:  # if form is invalid, revert to default address
            context['coords'], context['address_name'], context['alternative_addresses'], context['mapbox_api_key'] = get_coordinates(
                searched_address)
            context['current_weather'], context['hourly_forecast'], context['five_day_forecast'] = get_weather_info(
                context['coords'], units)
            form = address_form(searched_address=searched_address, alternative_addresses=[
                ('No Address Searched Yet', '')])
    # create json of data displayed.  Use this to create record if user saves record
    context['save_record'] = json.dumps({'time': str(datetime.now()), 'address': context['address_name'],
                                         'coords': context['coords'], 'weather': context['current_weather']['main'], 'weather_wind':  context['current_weather']['wind'], 'weather_cloud':
                                        context['current_weather']['clouds'], 'icon': context['current_weather']['weather'][0]['icon'],  'weather_desc': context['current_weather']['weather'][0]['description']})
    # split address on , so we can generate individual divs for each address line
    context['address_name'] = context['address_name'].split(",")
    context['form'] = form
    return render(request, "landing.html", context)
