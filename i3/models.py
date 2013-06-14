from sqlalchemy import Column, Integer, String
from database import Base
import time
class NewsPost(Base):
    __tablename__ = "news"
    pid = Column(Integer, primary_key = True)
    title = Column(String(512))
    contents = Column(String(4096))
    poster_uid = Column(Integer)
    time_posted = Column(Integer)

    def __init__(self, title = None, contents = None, pid = None, time_posted = time.time(), poster_uid = None):
        self.title = title
        self.contents = str(contents)
        self.pid = pid
        self.poster_uid = poster_uid
        self.time_posted = time_posted

    def __repr__(self):
        return "<NewsPost {0}>".format(self.title) 

class NewsReadMapItem(Base):
    __tablename__ = "news_read_map"
    mapid = Column(Integer, primary_key = True)
    uid = Column(Integer)
    pid = Column(Integer)

    def __init__(self, uid = None, pid = None):
        self.uid = uid
        self.pid = pid

    def __repr__(self):
        return "<NewsReadMapItem: {0} read {1}>".format(uid, pid)

class User(Base):
    __tablename__ = "users"
    uid = Column(Integer, primary_key = True)
    username = Column(String(512))
    passwd_hash = Column(String(512))

    def __init__(self, username, passwd_hash):
        self.username = username
        self.passwd_hash = passwd_hash

    def __repr__(self):
        return "<User {0}>".format(self.username)

class UserPermissionMapItem(Base):
    __tablename__ = "user_permission_map"
    mapid = Column(Integer, primary_key = True)
    uid = Column(Integer)
    permission = Column(String(512))
    
    def __init__(self, uid, permission):
        self.uid = uid
        self.permission = permission

    def __repr__(self):
        return "<UserPermissionMapItem: {0} has {1}>".format(
                self.uid, self.permission)

     
