import googlemaps
from datetime import datetime


class GoogleNavigation:
    def __init__(self):
        self.__end_position_lat = 45.4874172
        self.__end_position_lng = 9.1923037
        self.__gmaps = googlemaps.Client(key='AIzaSyCLNO5mol_LjqDuOkTKLBke4Q9de-6GVy4')
    
    
    def calculate_route(self, directions:list):
        try:
            pass
        except Exception as e:
            print(e)