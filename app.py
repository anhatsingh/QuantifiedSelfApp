import os, logging
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

logging.basicConfig(filename='debug.log', level=logging.INFO, format='[%(levelname)s %(asctime)s %(name)s] ' + '%(message)s')
app = None

def create_app():
    app = Flask(__name__, template_folder='templates')
    if os.environ.get('FLASK_ENV') == 'development':
        app.logger.info('STARTING DEVELOPMENT ENVIRONMENT')
        app.config.from_object(LocalDevelopmentConfig)
    
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.controllers.default import *

if __name__ == '__main__':
    app.run()