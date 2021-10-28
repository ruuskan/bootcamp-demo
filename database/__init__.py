from sqlalchemy import create_engine, text, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import os, datetime
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Draw(Base):
    """
    Table object to hold the draws for Finnish lottery

    """
    __tablename__ = 'draws'

    id = Column(Integer,primary_key=True)
    date = Column(DateTime)
    primary = Column(String(150))
    secondary = Column(String(100))
    tertiary = Column(String(100))
    share_count = Column(Integer)
    share_amount = Column(Integer)
    draw_type = Column(String(100))

    def __repr__(self):
        return f"<Draw (type = '{self.draw_type}', week='{self.week}',year='{self.year}')>"

DATABASE_URL = os.environ['DATABASE_URL']
db = create_engine(DATABASE_URL)
Session = sessionmaker(bind=db)