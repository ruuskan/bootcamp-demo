import datetime
import requests
from sqlalchemy.orm import session
from database.operations import search_between, insert_row

data_url = 'https://www.veikkaus.fi/api/draw-results/v1/games/LOTTO/draws/by-week/'
def handle_data(sd, ed):
    """
    Return query object

    Get data from Veikkaus and save it in database

    Parameters:
    sd: datetime.datetime object for starting date
    ed: datetime.datetime object for ending date
    """
    data = []
    dt = sd
    tuplelist = __is_data_available(sd,ed)
    
    for wytup in tuplelist:
        url_end = f'{wytup[1]}-W{wytup[0]:02}'
        print(url_end)
        resp = requests.get(url=data_url+url_end)
        datason = resp.json()
        if datason != []:
            data.append(datason)
            date=datetime.datetime.fromtimestamp(datason[0]['drawTime']//1000)
            primary=f"{datason[0]['results'][0]['primary']}" 
            try:
                secondary=f"{datason[0]['results'][0]['secondary']}"
            except:
                secondary='[]'
            try:
                tertiary=f"{datason[0]['results'][0]['tertiary']}"
            except KeyError:
                tertiary = '[]'
            share_count=f"{[datason[0]['prizeTiers'][x]['shareCount'] for x in range(len(datason[0]['prizeTiers']))]}" 
            share_amount=f"{[datason[0]['prizeTiers'][x]['shareAmount'] for x in range(len(datason[0]['prizeTiers']))]}"  
            tier_name=f"{[datason[0]['prizeTiers'][x]['name'] for x in range(len(datason[0]['prizeTiers']))]}"
            res = insert_row(date=date,primary=primary,secondary=secondary,tertiary=tertiary,
                            share_count=share_count,share_amount=share_amount,tier_name=tier_name)
        dt = dt + datetime.timedelta(weeks=1)
    return search_between(sd,ed)

def __is_data_available(sd,ed):
    dt = sd
    data_needed = []
    while dt <= ed:
        data_needed.append((dt.isocalendar().week,dt.isocalendar().year))
        dt = dt + datetime.timedelta(weeks=1)
    res = search_between(sd,ed)
    for row in res:
        if (row.date.isocalendar().week,row.date.isocalendar().year) in data_needed:
            data_needed.pop(data_needed.index((row.date.isocalendar().week,row.date.isocalendar().year)))
    return data_needed