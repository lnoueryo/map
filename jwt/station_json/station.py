
from jwtauth.settings import BASE_DIR
class StationJson:
    def get_line():
        f = open(f'{BASE_DIR}/station_json/json/yamanote.json', 'r', encoding='utf8')
        data = f.read()
        f.close()
        return data