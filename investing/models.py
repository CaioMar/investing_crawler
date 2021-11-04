from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from investing import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE), echo=True)


def init_db(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Articles(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    article_title = Column(String, nullable=False)
    article_link = Column(String, nullable=True)
    article_text = Column(String, nullable=True)
    article_author = Column(String, nullable=True)
    article_type = Column(String, nullable=True)
    article_date = Column(String, nullable=True)