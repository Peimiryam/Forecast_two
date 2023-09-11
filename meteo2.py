import requests

import datetime as dt

import json

import sys

from os.path import join, getmtime,exists

#import dirname

meteo = []

class WeatherForecast():
    def date(self):
        global item
        self.date_input = date_input
        date_input = input("Input 'tomorrow' if you want to check the tomorrow forecast or 'select' if you want to check for a specific a date: ")
        self.date_input = date_input
        if date_input == 'tomorrow':
            self.date_input = date_input
            date_input = dt.date.today() + dt.timedelta(1)
            self.item = date_input.strftime('%Y-%m-%d')
            print(f"Checking for tomorrow date: {self.item}")
            meteo.append(self.item)
            return self.item
        elif not date_input:
            sys.exit()
        if date_input == 'select':
            self.date_input = date_input
            try:
                date_input = dt.datetime.strptime(date_input, '%Y-%m-%d' )
                self.item = date_input.strftime ('%Y-%m-%d')
                meteo.append(self.item)
                return self.item
            except ValueError:
                print("invalid date input")
                sys.exit()
    
    #def __str__(self):
        #return 'WeatherForecast',(str(self.date_input))
    
    def __int__(self):
        return self.item

    def weather(self, search_date):
        latitude, longitude = 51.5085, 0.1257
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={search_date}&end_date={search_date}'
        response = requests.get(url)
        return response.text
    
    def weather_cached(self, search_date):
        global precipitation_sum
        use_cache = True
        file_path = join('cache', search_date)
        if not exists(file_path):
            use_cache = False
        elif dt.datetime.fromtimestamp(getmtime(file_path)) < dt.datetime.now() - dt.timedelta(hours=24):
            use_cache = False
        if use_cache:
            print("Cache used")
            with open(file_path) as file:
                precipitation = json.load(file)
                precipitation_sum = float(precipitation["daily"]["precipitation_sum"][0])
                if precipitation_sum <= 0:
                    return "it will rain"
                elif precipitation_sum > 0:
                    return "it will not rain"
        

        weather_txt = self.weather(search_date)

        with open (file_path, 'w') as file:
            file.write(weather_txt)
            print("Done")
            precipitation = json.loads(search_date)
            precipitation_sum = float(precipitation["daily"]["precipitation_sum"][0])
            meteo.append(precipitation_sum)
            return precipitation_sum
            
    def __getitem__(self, item):
        try:

            return self.weather_cached(item)
        
        except KeyError:

            return None
        
    def __setitem__(self, item, value):
        object[item] = self.weather_cached(value)

    def __iter__(self):
        for item in meteo:
            yield item

    def items(self):
        #print(meteo)
        for item, self.weather_cached in object:
            print(item, self.weather_cached)

object = WeatherForecast()

print(object['2023-09-12'])
#print(object['2023-09-12'])> this works
#object.items() > this not
#object.items()

#wf['2023-09-11'] = 'it will rain'


