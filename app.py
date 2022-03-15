import os, logging
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.models import User, Role

logging.basicConfig(filename='debug.log', level=logging.INFO, format='[%(levelname)s %(asctime)s %(name)s] ' + '%(message)s')
app = None

def create_app():
    app = Flask(__name__, template_folder='templates')
    if os.environ.get('FLASK_ENV') == 'development':
        app.logger.info('STARTING DEVELOPMENT ENVIRONMENT')
        app.config.from_object(LocalDevelopmentConfig)
    
    db.init_app(app)
    app.app_context().push()

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)

    app.logger.info('App setup complete.')
    return app

app = create_app()

from application.controllers.default import *
from application.controllers.error_handlers import *

if __name__ == '__main__':
    app.run()