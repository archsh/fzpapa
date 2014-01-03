from flask import Flask, Request, Response
import os

application = app = Flask(__name__)
VCAP_SERVICES = os.getenv("VCAP_SERVICES")


@app.route('/')
def hello_world():
    return VCAP_SERVICES or 'HelloWorld'


if __name__ == '__main__':
    app.run()
