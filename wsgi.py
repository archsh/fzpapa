import logging
import os
from tornado.web import RedirectHandler, RequestHandler, StaticFileHandler
from restlet.application import RestletApplication
import simplejson as json

## The default VCAP_SERVICES for local development. Which is from appfog.
DEFAULT_VCAP_SERVICES = """\
{
 "postgresql-9.1":[
    {
      "name":"pqdb",
      "label":"postgresql-9.1",
      "plan":"free",
      "tags":["postgresql","postgresql-9.1","relational","postgresql-9.1","postgresql"],
      "credentials":{
        "name":"fzpapadb",
        "host":"localhost",
        "hostname":"localhost",
        "port":5432,
        "user":"postgres",
        "username":"postgres",
        "password":"postgres"
      }
    }
  ]
}
"""

VCAP_SERVICES = os.getenv("VCAP_SERVICES", DEFAULT_VCAP_SERVICES)
LOG_LEVEL = os.getenv("FZPAPA_LOGLEVEL", "DEBUG")
DEBUGGING = True if LOG_LEVEL == 'DEBUG' else False
logging.basicConfig(level=logging.DEBUG)

try:
    _VCAP_SERVICES_ = json.loads(VCAP_SERVICES)
except:
    _VCAP_SERVICES_ = {}

if "postgresql-9.1" in _VCAP_SERVICES_:
    _DBURI_ = "postgresql://%(username)s:%(password)s@%(host)s:%(port)d/%(name)s" \
              % _VCAP_SERVICES_["postgresql-9.1"][0]["credentials"]
else:
    _DBURI_ = ""


class DefaultHandler(RequestHandler):
    def get(self):
        self.write(VCAP_SERVICES or "Hello, world")


from base.views import UserHandler, GroupHandler, PermissionHandler
from base.models import Base


class FzpapaApplication(RestletApplication):
    """\
    We need to do initialization here.
    """
    def __init__(self, handlers=None, default_host="", transforms=None,
                 wsgi=False, **settings):
        super(FzpapaApplication, self).__init__(handlers=handlers,
                                                default_host=default_host,
                                                transforms=transforms,
                                                wsgi=wsgi, **settings)
        if self.db_engine is not None:
            Base.metadata.create_all(self.db_engine)

working_directory = os.path.abspath(os.path.dirname(__file__))
application = FzpapaApplication([(r'/(.*)',
                                  StaticFileHandler,
                                  {"path": os.path.join(working_directory, "_webpages_default"),
                                   "default_filename": "index.html"}),
                                 (r'/admin/(.*)',
                                  StaticFileHandler,
                                  {"path": os.path.join(working_directory, "_webpages_admin"),
                                   "default_filename": "index.html"}),
                                 ],
                                dburi=_DBURI_,  # 'sqlite:///:memory:',
                                loglevel=LOG_LEVEL,
                                debug=DEBUGGING,
                                dblogging=DEBUGGING)


if __name__ == "__main__":
    import tornado.ioloop
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
