import logging
import os
import tornado.web
from restlet.application import RestletApplication

DEFAULT_VCAP_SERVICES = """\
{
    postgresql-9.1: [
        {
            name: "pqdb",
            label: "postgresql-9.1",
            plan: "free",
            tags: [
                "postgresql",
                "postgresql-9.1",
                "relational",
                "postgresql-9.1",
                "postgresql"
            ],
            credentials: {
                name: "d01d2c6f92ad74c3e929653933714ab4a",
                host: "10.0.35.83",
                hostname: "10.0.35.83",
                port: 5432,
                user: "u10f197a24e4e485b8b96cbe6dbac8c8f",
                username: "u10f197a24e4e485b8b96cbe6dbac8c8f",
                password: "pa17ae6a8ed5140948df45e533af83b69"
            }
        }
    ]
}
"""

VCAP_SERVICES = os.getenv("VCAP_SERVICES", DEFAULT_VCAP_SERVICES)
LOG_LEVEL = os.getenv("FZPAPA_LOGLEVEL", "DEBUG")
DEBUGGING = True if LOG_LEVEL == 'DEBUG' else False
# UserHandler.route_to('/users'),
# GroupHandler.route_to('/groups'),
# PermissionHandler.route_to('/permissions')
logging.basicConfig(level=logging.DEBUG)


class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(VCAP_SERVICES or "Hello, world")


from base.views import UserHandler, GroupHandler, PermissionHandler
application = RestletApplication([(r'/', DefaultHandler),
				  UserHandler.route_to('/users'),
                                  GroupHandler.route_to('/groups'),
                                  PermissionHandler.route_to('/permissions')],
                                 dburi='postgresql://postgres:postgres@localhost/test',  # 'sqlite:///:memory:',
                                 loglevel=LOG_LEVEL,
                                 debug=DEBUGGING,
                                 dblogging=DEBUGGING)


if __name__ == "__main__":
    import tornado.ioloop
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
