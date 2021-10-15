import os
from typing_extensions import ParamSpec
import pandas as pd
import copy
from sklearn.linear_model import LinearRegression
from django.conf import settings

pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)

class HouseModel():
    def __init__(self, house_info):
        self.house_info = house_info
        self.prefecture_id = house_info['prefecture_id']
        self.city_code = house_info['city_code']
        self.layout = house_info['layout']
        self.station = house_info['station']
        self.direction = house_info['direction']
        area = house_info['area']
        age = house_info['age']
        distance = house_info['distance']
        self.x_parameters = [area, age, distance]
        if 'options' in self.house_info:
            options = self.house_info['options']
            self.bicycle = options['bicycle']
            self.bike = options['bike']
            self.washlet = options['washlet']
            self.dryer = options['dryer']
            self.floor_heating = options['floor_heating']
            self.washroom = options['washroom']
            self.loft = options['loft']
            self.furniture = options['furniture']
            self.appliance = options['appliance']
            self.autolock = options['autolock']
            self.x_parameters = self.x_parameters + [self.bicycle, self.bike, self.washlet, self.dryer, self.floor_heating, self.washroom, self.loft, self.furniture, self.appliance, self.autolock]
        self.df = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/model/{self.prefecture_id}/{self.city_code}.csv'))
    def analysis(self):
        model = LinearRegression()
        df_main = self.df.query(f'layout == "{self.layout}"')
        q = df_main.quantile(0.95)['rental_fee']
        df_main = df_main.query(f'rental_fee < {q}')
        station_dummy = pd.get_dummies(df_main['station'])
        direction_dummy = pd.get_dummies(df_main['direction'])

        stations = self.create_station_num(station_dummy.columns, self.station)
        directions = self.create_direction_num(direction_dummy.columns, self.station)
        self.x_parameters = self.x_parameters + stations + directions
        y = df_main['rental_fee']
        X = df_main.fillna(0)
        X = pd.concat([X, station_dummy, direction_dummy], axis=1)
        X = X.drop(['layout', 'address', 'total_deposit', '駐車場', 'バストイレ別', '洗面化粧台', '防音','rental_fee', 'direction','layout','station','company'], axis=1)
        model.fit(X, y)
        return model.predict([self.x_parameters])

    def create_station_num(self, station_columns, station):
        station_columns = list(station_columns)
        stations = [1 if station == station_column else 0 for station_column in station_columns]
        return stations

    def create_direction_num(self, direction_columns, direction):
        direction_columns = list(direction_columns)
        directions = [1 if direction == direction_column else 0 for direction_column in direction_columns]
        return directions

    def create_address_num(address_columns, address):
        address_columns = list(address_columns)
        addresses = [1 if address == address_column else 0 for address_column in address_columns]
        return addresses


house_info_dict = {
    'prefecture_id': 13,
    'city_code': 102,
    'layout': '1K',
    'area': 10.16,
    'age': 24,
    'distance': 5,
    'station': '東京駅',
    'direction': '南東',
    'options': {
        'bicycle': 1,
        'bike': 0,
        'washlet': 1,
        'dryer': 1,
        'floor_heating': 0,
        'washroom': 0,
        'loft': 0,
        'furniture': 0,
        'appliance': 0,
        'autolock': 0,
    }
}
hm = HouseModel(house_info_dict)
value = hm.analysis()
