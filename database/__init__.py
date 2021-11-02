from sqlalchemy import create_engine, text, Column, String, Integer, DateTime, Float, ARRAY
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
    primary = Column(String(255))
    secondary = Column(String(255))
    tertiary = Column(String(255))
    share_count = Column(String(255))
    share_amount = Column(String(255))
    tier_name = Column(String(255))

    def __repr__(self):
        return f"<Draw date='{self.date}')>"
        

DATABASE_URL = os.environ['DATABASE_URL']
db = create_engine(DATABASE_URL)
Session = sessionmaker(bind=db)