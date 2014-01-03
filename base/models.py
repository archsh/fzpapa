# -*- coding: utf-8 -*-
import logging
import datetime
from restlet.application import RestletApplication
from restlet.handler import RestletHandler, encoder, decoder, route
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table, Column, Integer, String, Sequence, MetaData, DateTime, func,
                        ForeignKey, Text, SmallInteger, Boolean, Numeric)
from sqlalchemy.orm import relationship, backref
_logger = logging.getLogger('tornado.restlet')

Base = declarative_base()