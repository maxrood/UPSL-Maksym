dasimport os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Risk(Base):
    __tablename__ = 'risks'
    id = Column(Integer, primary_key=True)
    zagrozenie = Column(String)
    prawdopodobienstwo = Column(Integer)
    wplyw = Column(Integer)

def init_db():
    Base.metadata.create_all(engine)
    return engine, Session

def add_risk(zagrozenie, prawdopodobienstwo, wplyw):
    session = Session()
    new_risk = Risk(
        zagrozenie=zagrozenie,
        prawdopodobienstwo=prawdopodobienstwo,
        wplyw=wplyw
    )
    session.add(new_risk)
    session.commit()
    session.close()

def get_risks():
    session = Session()
    risks = session.query(Risk).all()
    data = [{
        "Zagrożenie": r.zagrozenie,
        "Prawdopodobieństwo": r.prawdopodobienstwo,
        "Wpływ": r.wplyw
    } for r in risks]
    session.close()
    return pd.DataFrame(data)
