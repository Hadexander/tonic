from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import *

_engine = create_engine(dburl)
Session = sessionmaker(bind=_engine)
Base = declarative_base()
class User(Base):
    __tablename__ = 'owners'
    sha = Column(String(64), primary_key = True)
    access = Column(Integer, default=0)

    def __init__(self, **kwargs):
        self.sha = kwargs.pop('sha', None)
        self.access = kwargs.pop('access', 0)

    def store(self):
        session = Session()
        session.merge(self)
        session.commit()
        session.close()

    def retrieve(self):
        session = Session()
        query = session.query(User).filter(User.sha == self.sha)
        u = query.one_or_none()
        if(u):
            self.access = u.access
        session.close()

Base.metadata.create_all(_engine)
