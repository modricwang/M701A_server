import sys

from sqlalchemy.exc import OperationalError

from m701a.io_utils import connect_helper
import datetime
import time
from sqlalchemy import create_engine

from sqlalchemy import Column, Index
from sqlalchemy import Integer, Float
from sqlalchemy import String, DateTime
# import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from argparse import ArgumentParser
import signal

Base = declarative_base()


class AirData(Base):
    __tablename__ = "air_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime)
    CO2 = Column(Integer)
    CH2O = Column(Integer)
    TVOC = Column(Integer)
    PM2_5 = Column(Integer)
    PM10 = Column(Integer)
    Temperature = Column(Float)
    Humidity = Column(Float)

    # fullname = Column(String)

    def __repr__(self):
        return "ID:%d, DateTime:%s, CO2: %d, CH2O:%d" % (self.id, self.time, self.CO2, self.CH2O)


def process_args():
    parser = ArgumentParser()
    parser.add_argument('--port', default='/dev/ttyAMA0')
    parser.add_argument('--db_url', default='sqlite:///test.db')
    args = parser.parse_args()
    return args


def main():
    args = process_args()
    # conn = connect_helper(port='/dev/ttyAMA0')
    conn = connect_helper(port=args.port)
    engine = create_engine(args.db_url, echo=True, future=True)

    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        time_index = Index('time_index', AirData.time)
        time_index.create(bind=engine)
    except OperationalError:
        pass

    try:
        id_index = Index('id_index', AirData.id)
        id_index.create(bind=engine)
    except OperationalError:
        pass

    while True:
        try:
            try:
                info = conn.read()
            except IOError as e:
                print(e)
                conn.connect.close()
                del conn
                conn = connect_helper(port=args.port)
                continue
            print(datetime.datetime.now(), info)
            time.sleep(30)
            data = AirData(time=datetime.datetime.now(),
                           CO2=info['CO2'],
                           CH2O=info['CH2O'],
                           TVOC=info['TVOC'],
                           PM2_5=info['PM2.5'],
                           PM10=info['PM10'],
                           Temperature=info['Temperature'],
                           Humidity=info['Humidity'])
            session.add(data)
            session.commit()
        except KeyboardInterrupt:
            session.commit()
            session.close()
            break


if __name__ == '__main__':
    main()
