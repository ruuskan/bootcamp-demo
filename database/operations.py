from database import Draw, Session
from sqlalchemy import or_

def __get_session():
    return Session()

def insert_row(date, primary, secondary, tertiary, share_count, share_amount, draw_type, commit = True):
    new_row = Draw(date=date, primary=primary, secondary=secondary, tertiary=tertiary,
                share_count=share_count, share_amount=share_amount, draw_type=draw_type)
    db = __get_session()
    db.add(new_row)

def commit_changes():
    db = __get_session()
    db.commit()
    db.close()
    return True

# def search_time(week,year):
#     return __get_session().query(Draw).filter(Draw.week == week,Draw.year == year)

def search_between(startdate, enddate):
    return __get_session().query(Draw).filter(Draw.week >= startdate,Draw.year <= enddate)



def get_all():
    return __get_session().query(Draw).all()