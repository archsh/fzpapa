# -*- coding: utf-8 -*-
import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table, Column, Integer, String, Sequence, MetaData, DateTime, func,
                        ForeignKey, Text, SmallInteger, Boolean, Numeric)
from sqlalchemy.orm import relationship, backref
_logger = logging.getLogger('tornado.restlet')

Base = declarative_base()

group2permission_table = Table('groups2permissions', Base.metadata,
                               Column('group_id', Integer,
                                      ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True),
                               Column('permission_id', Integer,
                                      ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True))


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, Sequence('group_id_seq'), primary_key=True)
    name = Column(String(50))
    users = relationship('User', backref="group", cascade="all, delete, delete-orphan",
                         passive_deletes=True)
    permissions = relationship('Permission', secondary=group2permission_table, passive_deletes=True)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    fullname = Column(String(50), nullable=True)
    password = Column(String(40), nullable=True)
    key = Column(String(32), nullable=True, doc='Another key')
    created = Column(DateTime, default=func.NOW())
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id)


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, Sequence('permission_id_seq'), primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(String(128), nullable=True)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id)
