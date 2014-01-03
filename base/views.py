# -*- coding: utf-8 -*-
import datetime
import logging
from restlet.handler import RestletHandler, encoder, decoder, route
from .models import Group, Permission, User
_logger = logging.getLogger('tornado.restlet')


class GroupHandler(RestletHandler):
    class Meta:
        table = Group


class PermissionHandler(RestletHandler):
    class Meta:
        table = Permission


class UserHandler(RestletHandler):
    """UserHandler to process User table."""
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)
        self.t1 = datetime.datetime.now()
        self.t2 = None

    def on_finish(self):
        self.t2 = datetime.datetime.now()
        _logger.info('Total Spent: %s', self.t2 - self.t1)

    class Meta:
        table = User
        #allowed = ('GET', )  # 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS')
        #denied = ('POST',)  # Can be a tuple of HTTP METHODs
        readonly = ('name', )  # None means no field is read only
        invisible = ('password', )  # None means no fields is invisible
        encoders = None  # {'password': lambda x, obj: hashlib.new('md5', x).hexdigest()}
                             # or use decorator @encoder(*fields)
        decoders = None  # User a dict or decorator @decoder(*fields)
        generators = None  # User a dict or decorator @generator(*fields)
        extensible = None  # None means no fields is extensible or a tuple with fields.

    @encoder('password')
    def password_encoder(passwd, inst=None):  # All the encoder/decoder/generator/validator can not bound
    # to class or instance
        import hashlib
        return hashlib.new('md5', passwd).hexdigest()

    @route(r'/(?P<uid>[0-9]+)/login', 'POST', 'PUT')
    @route(r'/login', 'POST', 'PUT')
    def do_login(self, *args, **kwargs):
        _logger.info("OK, It's done!: %s, %s, %s", args, kwargs, self.request.arguments)
        self.write("OK, It's done!: %s, %s" % (args, kwargs))