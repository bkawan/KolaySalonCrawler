from sqlalchemy import Column, ForeignKey,VARCHAR,INTEGER,String

from sqlalchemy.dialects.mssql import TEXT,TINYINT,VARCHAR,INTEGER
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.interfaces import  MapperExtension
from sqlalchemy import create_engine,DateTime
import settings
import datetime
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

def drop_tables(engine):
    DeclarativeBase.metadata.drop_all(engine)




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
    logo = Column(MEDIUMBLOB)
    province = Column(VARCHAR(255))
    district = Column(VARCHAR(255))
    full_address = Column(VARCHAR(255))
    geoposition = Column(VARCHAR(255))
    working_hours = Column(VARCHAR(255))
    about = Column(TEXT)
    photos = Column(TEXT)
    professionals = Column(TEXT)
    created_at = Column(DateTime, default=datetime.datetime.now)
    modified_at = Column(DateTime, onupdate=datetime.datetime.now)


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
    created_at = Column(DateTime, default=datetime.datetime.now)
    modified_at = Column(DateTime, onupdate=datetime.datetime.now)

    business = relationship(
        Business,
        backref=backref('review',
                        uselist=True,
                        cascade='delete,all'))


class Category(DeclarativeBase):
    """ Category Entity class"""

    __tablename__ = 'categories'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(255),unique=True)


class Service(DeclarativeBase):
    """ Servie Entity Class"""
    __tablename__ = 'services'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(255))

    category_id = Column(INTEGER, ForeignKey('categories.id'))
    # category_id = 1

    category = relationship(
        Category,
        backref=backref('category',
                        uselist=True,
                        cascade='delete,all'))



class BusinessServicesRel(DeclarativeBase):
    """Service Entity Class"""
    __tablename__ = 'business_services_rels'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }



    id = Column(INTEGER, primary_key=True)
    gender = Column(VARCHAR(255))
    business_id = Column(INTEGER, ForeignKey('businesses.id'))
    service_id = Column(INTEGER, ForeignKey('services.id'))
    price = Column(VARCHAR(255))
    created_at = Column(DateTime, default=datetime.datetime.now)
    modified_at = Column(DateTime, onupdate=datetime.datetime.now)

    business = relationship(
        Business,
        backref=backref('business_rel',
                        uselist=True,
                        cascade='delete,all'))
    service = relationship(
        Service,
        backref=backref('service_rel',
                        uselist=True,
                        cascade='delete,all'))


















