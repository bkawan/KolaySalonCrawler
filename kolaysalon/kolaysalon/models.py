from sqlalchemy import Column, ForeignKey,VARCHAR,INTEGER,String

from sqlalchemy.dialects.mssql import  TEXT,TINYINT,VARCHAR,INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.interfaces import  MapperExtension
from sqlalchemy import create_engine
import settings

from sqlalchemy.orm import relationship, backref


DeclarativeBase = declarative_base()


def db_engine_connect():

    connection_string = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
        settings.MYSQL_USER,
        settings.MYSQL_PASSWORD,
        settings.MYSQL_HOST,
        settings.MYSQL_DBNAME
    )

    # 'engine = create_engine('mysql+pymysql://root:root@127.0.0.1/kolay', echo=True)

    connection_engine = create_engine(connection_string, echo=True)

    return connection_engine


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)



class Business(DeclarativeBase):
    """ Business entity Class"""
    __tablename__ = 'businesses'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    """

    """

    id = Column(INTEGER, primary_key=True)
    shop_name_value = Column(VARCHAR(255), primary_key=True)
    kolayrandevu_url = Column(VARCHAR(255))
    name = Column(VARCHAR(255))
    logo = Column(VARCHAR(255))
    province = Column(VARCHAR(255))
    district = Column(VARCHAR(255))
    full_address = Column(VARCHAR(255))
    geoposition = Column(VARCHAR(255))
    working_hours = Column(VARCHAR(255))
    about = Column(TEXT)
    photos = Column(TEXT)
    professionals = Column(TEXT)


class Review(DeclarativeBase):
    """Review Entity Class"""
    __tablename__ = 'reviews'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(INTEGER, primary_key=True)
    rating_count = Column(INTEGER)
    comment_count = Column(INTEGER)
    business_id = Column(INTEGER, ForeignKey('businesses.id'))

    business = relationship(
        Business,
        backref=backref('review',
                        uselist=True,
                        cascade='delete,all'))

class Service(DeclarativeBase):
    """Review Entity Class"""
    __tablename__ = 'services'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(INTEGER, primary_key=True)
    services = Column(TEXT)
    gender = Column(VARCHAR(255))
    business_id = Column(INTEGER, ForeignKey('businesses.id'))
    business = relationship(
        Business,
        backref=backref('service',
                        uselist=True,
                        cascade='delete,all'))









