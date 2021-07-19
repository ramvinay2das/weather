from django.shortcuts import render
from django.contrib import messages
from .models import City

# Create your views here.
import urllib.request
import json
import geocoder

# http://api.openweathermap.org/data/2.5/group?id=1733046,1735106,1732752

def get_all_city():
    all_city = City.objects.all()
    city_dropdown = []
    for city in all_city:
        city_dropdown.append(city.name)
    return city_dropdown

def get_default_card_weather():
    tkn = 'be81a9e37acdb1d9f783d653e776e223'
    source_def = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/group?id=1733046,1735106,1732752&units=metric&appid=' + tkn).read()
    list_data_def = json.loads(source_def)
    card_data = []
    for item in list_data_def['list']:
        row = []
        row.append(str(item['name']))
        row.append(str(item['main']['temp']) + '°C')
        row.append(str(item['main']['humidity']))
        row.append(str(item['weather'][0]['main']))
        row.append(str(item['weather'][0]['description']))
        card_data.append(row)
    return card_data

def index(request):
    city_dropdown = get_all_city()
    card_data = get_default_card_weather()
    if request.method == 'POST':
        tkn = 'be81a9e37acdb1d9f783d653e776e223'
        try:
            if request.POST['search_by'] == "location":
                myloc = geocoder.ip('me')
                latitude = str(myloc.latlng[0])
                longitude= str(myloc.latlng[1])
                source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?lat=' + latitude + '&lon=' + longitude + '&units=metric&appid=' + tkn).read()
                list_data = json.loads(source)
            else:
                city = request.POST['city'].replace(" ","%20")
                source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+ city + '&units=metric&appid=' + tkn).read()
                list_data = json.loads(source)
            context = {
            "city" : str(list_data['name']),
            "temp" : str(list_data['main']['temp']) + '°C',
            "pressure" : str(list_data['main']['pressure']),
            "humidity" : str(list_data['main']['humidity']),
            "country_code" : str(list_data['sys']['country']),
            "main" : str(list_data['weather'][0]['main']),
            "description" : str(list_data['weather'][0]['description']),
            "city_dropdown" : city_dropdown,
            "title" : "Current Weather",
            "card_data" : card_data, 
            }
        except:
            messages.warning(request, 'Error, City not found')
            context = {
                "city_dropdown" : city_dropdown,
                "title" : "Current Weather",
                "card_data" : card_data,
            }
    else:
        context = {
            "city_dropdown" : city_dropdown,
            "title" : "Current Weather",
            "card_data" : card_data,
        }
    return render( request, "weatherapp/index.html", context)

def day_forecast(request):
    city_dropdown = get_all_city()
    card_data = get_default_card_weather()
    if request.method == 'POST':
        tkn = 'be81a9e37acdb1d9f783d653e776e223'
        try:
            if request.POST['search_by'] == "location":
                myloc = geocoder.ip('me')
                latitude = str(myloc.latlng[0])
                longitude= str(myloc.latlng[1])
                source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?lat=' + latitude + '&lon=' + longitude + '&units=metric&appid=' + tkn).read()
                list_data = json.loads(source)
            else:
                city = request.POST['city'].replace(" ","%20")
                source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?q='+ city + '&units=metric&appid=' + tkn).read()
                list_data = json.loads(source)
            five_forecast = []
            for item in list_data['list']:
                row = {
                    "date_time" : str(item['dt_txt']), 
                    "temp" : str(item['main']['temp']) + '°C',
                    "pressure" : str(item['main']['pressure']),
                    "humidity" : str(item['main']['humidity']),
                    "main" : str(item['weather'][0]['main']),
                    "description" : str(item['weather'][0]['description']),
                }
                five_forecast.append(row)
            context = {
                "city_dropdown" : city_dropdown,
                "city" : str(list_data['city']['name']),
                "country_code" : str(list_data['city']['country']),
                "title" : "Forecast Weather",
                "card_data" : card_data,
                "five_forecast" : five_forecast
            }
        except:
            messages.warning(request, 'Error, City not found')
            context = {
                "city_dropdown" : city_dropdown,
                "title" : "Forecast Weather",
                "card_data" : card_data
            }
    else:
        context = {
            "city_dropdown" : city_dropdown,
            "title" : "Forecast Weather",
            "card_data" : card_data
        }
    return render( request, "weatherapp/day_forecast.html", context)

def modify_city(request):
    city_data = get_all_city()
    card_data = get_default_card_weather()
    if request.method == "POST":
        tkn = 'be81a9e37acdb1d9f783d653e776e223'
        if 'delete' in request.POST:
            try:
                City.objects.filter(name = request.POST['delete']).delete()
                messages.success(request, 'Data deleted successfully')
            except:
                messages.warning(request, 'Error in deleting data')
        elif 'edit' in request.POST:
            try:
                city_update = City.objects.get(name = request.POST['edit'])
                city_update.name = request.POST['city_val']
                city_update.save()
                messages.success(request, 'Data upated successfully')
            except:
                messages.warning(request, 'Error in updating data')
        elif 'add' in request.POST:
            try:
                city_add = City(name = request.POST['add'])
                city_add.save()
                messages.success(request, 'Data added successfully')
            except:
                messages.warning(request, 'Error in adding data')
        city_data = get_all_city()

    context = {
        "city_data" : city_data,
        "title" : "Modify City",
        "card_data" : card_data,
    }
    return render(request, "weatherapp/modify_city.html", context)

