import datetime
import requests
from database.operations import search_between

data_url = 'https://www.veikkaus.fi/api/draw-results/v1/games/LOTTO/draws/by-week/'
data = []
def handle_data(sd, ed):
    dt = sd
    while dt < ed:
        url_end = f'{dt.isocalendar().year}-W{dt.isocalendar().week:02}'

        resp = requests.get(url=data_url+url_end)
        datason = resp.json()
        if datason != []:
            data.append(datason)

        dt = dt + datetime.timedelta(weeks=1)
    
    return data

def __is_data_available(st,ed):
    dt = st
    data_needed = []
    while dt <= ed:
        data_needed.append(dt)
        dt = dt + datetime.timedelta(weeks=1)
    res = search_between(st,ed)
    for row in res:
        if row.date in data_needed:
            data.needed.pop(data_needed.index(row.date))
