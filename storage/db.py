from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import inspect

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String(20), primary_key = True)
    access = Column(Integer, default=0)
    github = Column(String(64))

class Guild(Base):
    __tablename__ = 'guilds'
    id = Column(String(20), primary_key = True)
    prefix = Column(String(64))
    emojis = relationship('Emoji', back_populates='guild')

class Emoji(Base):
    __tablename__ = 'emojis'
    id = Column(Integer, Sequence('emoji_id_sequence'), primary_key = True)
    guild_id = Column(String(20), ForeignKey('guilds.id'), nullable = False)
    guild = relationship('Guild', back_populates='emojis')
    url = Column(String(64))
    name = Column(String(64))

class DatabaseInterface:
    def __init__(self, url):
        engine = create_engine(url)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def getall(self, Table, **kwargs):
        q = self.session.query(Table)
        for key in kwargs:
            q = q.filter(getattr(Table, key) == kwargs[key])
        return q
    
    def get(self, Table, **kwargs):
        q = self.getall(Table, **kwargs)
        return q.first()
    
    def add(self, obj):
        self.session.add(obj)
        return None
    
    def count(self, Table):
        return self.session.query(Table).count()
    
    def delete(self, obj):
        self.session.delete(obj)
    
    def commit(self):
        self.session.commit()
