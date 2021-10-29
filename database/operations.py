from database import Draw, Session
from sqlalchemy import or_

def __get_session():
    return Session()

def insert_row(date, primary, secondary, tertiary, share_count, share_amount, tier_name):
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
    return __get_session().query(Draw).filter(Draw.date >= startdate,Draw.date <= enddate)



def get_all():
    return __get_session().query(Draw).all()