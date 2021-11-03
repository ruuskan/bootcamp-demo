from database import Draw, Session
from sqlalchemy import or_

def __get_session():
    return Session()

def insert_row(date, primary, secondary, tertiary, share_count, share_amount, tier_name):
    """
    Return id of the inserted row

    Insert new row with supplied data in the database

    Parameters:
    date:           datetime object of the draw time
    primary:        stringified list of primary numbers
    secondary:      stringified list of secondary numbers
    tertiary:       stringified list of tertiary numbers
    share_count:    stringified list of winners of each prize tier
    share_amount:   stringified list of winnings per winner of each prize tier
    tier_name:      stringified list of tier names
    
    """

    new_row = Draw(date=date, primary=primary, secondary=secondary, tertiary=tertiary,
                share_count=share_count, share_amount=share_amount, tier_name=tier_name)
    db = __get_session()
    db.add(new_row)
    db.commit()
    id = new_row.id
    db.close()
    return id


# def search_time(week,year):
#     return __get_session().query(Draw).filter(Draw.week == week,Draw.year == year)

def search_between(startdate, enddate):
    """
    Returns sqlalchemy query object

    Query result between starting and ending datetimes.

    Parameters:
    startdate:  datetime.datetime type time object specifying starting date for the query
    enddate:    datetime.datetime type time object specifying ending date for the query
    """
    return __get_session().query(Draw).filter(Draw.date >= startdate,Draw.date <= enddate)



def get_all():
    """
    Returns sqlalchemy query object

    Query all data.
    
    """
    return __get_session().query(Draw).all()