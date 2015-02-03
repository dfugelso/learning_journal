import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    UnicodeText,
    Unicode,
    desc,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from cryptacular.bcrypt import BCRYPTPasswordManager as Manager

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
 
    
class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column (UnicodeText, default=u'')
    created = Column (DateTime, default=datetime.datetime.utcnow)
    edited = Column (DateTime, default=datetime.datetime.utcnow)
    
    # def __init__(self, title):
        # self.title = title
    
    @classmethod
    def all (cls, session=None):
        '''
        Return all entries latest entry first.
        ''' 
        if session is None:
            session = DBSession
        return session.query(cls).order_by(desc(cls.created)).all()
        
    @classmethod        
    def by_id(cls, id, session=None):
        '''
        Return entry buy Index.
        '''
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.id == id).first()
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)

    @classmethod
    def by_name(cls, name, session=None):
        if session is None:
            session = DBSession
        return session.query(User).filter(User.name == name).first()
        
    def verify_password(self, password):
        ''' 
        Verify username and password using Cryptacular.
        '''
        manager = Manager()
        return manager.check(self.password, password)
    

