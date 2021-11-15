from .models import *
from pathlib import Path
from gmap.geohash import Geohash
class Sqlite():

    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.engine = create_engine(f'sqlite:///{BASE_DIR}/db.sqlite3')
        self.gh = Geohash()

    def get_companies(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        companies = session.query(Company).all()
        company_dict_list = [company.to_join_line_station_dict() for company in companies]
        session.close()
        return company_dict_list

    def get_prefectures_cities(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        prefectures = session.query(Prefecture).all()
        prefecture_dict_list = [prefecture.to_join_city_spot_dict() for prefecture in prefectures]
        session.close()
        return prefecture_dict_list

    def get_spot(self, id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        spot = session.query(Spot).filter(Spot.id == id).one_or_none()
        spot_dict = spot.to_spot_dict()
        neighbors = self.get_neighbors(spot_dict['geohash'])
        num = 1
        while num < 6:
            stations = session.query(Station).filter(Station.geohash.in_(neighbors)).all()
            if stations:
                break
            else:
                for neighbor in neighbors:
                    neighbors = neighbors + self.get_neighbors(neighbor)
                neighbors = list(set(neighbors))
            num += 1
        station_dict_list = [station.to_join_company_line_dict() for station in stations]
        spot_dict['stations'] = station_dict_list
        session.close()
        return spot_dict

    def get_neighbors(self, geohash):
        neighbors = self.gh.neighbors(geohash)
        for neighbor in neighbors:
            neighbors = neighbors + self.gh.neighbors(neighbor)
        return list(set(neighbors))

    def get_prefectures(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        prefectures = session.query(Prefecture).all()
        prefecture_dict_list = [prefecture.to_prefecture_dict() for prefecture in prefectures]
        session.close()
        return prefecture_dict_list

    def get_stations_by_name(self, id, name):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        stations = session.query(Station).filter(Station.prefecture_id == id).filter(Station.name == name).all()
        station_dict_list = [station.to_join_company_line_station_dict() for station in stations]
        session.close()
        return station_dict_list

    def get_stations(self, id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        stations = session.query(Station).filter(Station.prefecture_id == id).all()
        station_dict_list = [station.to_station_dict() for station in stations]
        session.close()
        return station_dict_list

    def get_lines(self, id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        lines = session.query(Line).filter(Line.prefecture_id == id).all()
        line_dict_list = [line.to_line_dict() for line in lines]
        session.close()
        return line_dict_list

    def get_cities(self, id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        cities = session.query(City).filter(City.id == id).all()
        city_dict_list = [city.to_join_spot_town_station_company_line_dict() for city in cities]
        session.close()
        return city_dict_list

    def search_stations(self, words):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        query = session.query(Station)
        filters = []
        for word in words:
            filters.append(and_(Station.search_text.like('%' + word + '%')))
        stations = query.filter(and_(*filters)).all()
        station_dict_list = [station.to_station_dict() for station in stations] if stations else []
        new_station_dict_list = []
        for station_dict in station_dict_list:
            if word in station_dict['name']:
                new_station_dict_list = [station_dict] + new_station_dict_list
            else:
                new_station_dict_list.append(station_dict)
        session.close()
        return new_station_dict_list

    def search_towns(self, words):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        query = session.query(Town)
        filters = []
        for word in words:
            filters.append(and_(Town.search_text.like('%' + word + '%')))
        towns = query.filter(and_(*filters)).all()
        town_dict_list = [town.to_short_town_dict() for town in towns] if towns else []
        new_town_dict_list = []
        for town_dict in town_dict_list:
            if word in town_dict['name']:
                new_town_dict_list = [town_dict] + new_town_dict_list
            else:
                new_town_dict_list.append(town_dict)
        session.close()
        return new_town_dict_list
