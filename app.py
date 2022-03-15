import os, logging
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

from application.models import User, Role
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired

# set the configurations for the log file
logging.basicConfig(filename='debug.log', level=logging.INFO, format='[%(levelname)s %(asctime)s %(name)s] ' + '%(message)s')
# set app = None to initialize variable
app = None


def create_app():
    '''This function creates a flask app along with all the necessary db, context, security relating things.
    '''
    # create flask app with name = __name__ and template folder where .html are stored
    app = Flask(__name__, template_folder='templates')

    # check if flask environment is is development
    if os.environ.get('FLASK_ENV') == 'development':
        app.logger.info('STARTING DEVELOPMENT ENVIRONMENT')
        # load development configurations
        app.config.from_object(LocalDevelopmentConfig)
    
    # initialize database
    db.init_app(app)
    app.app_context().push()

    # this is used to extend the registration form in Flask-Security. This inherits
    # the Flask-Security's already created RegisterForm class.
    class ExtendedRegisterForm(RegisterForm):
        # the additional field we are adding to the form, name of variable must be exactly same as database attribute.
        username = StringField('Full Name', [DataRequired()])

    # initialize the Flask-Security.
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    # this provides a current_user object in all the possible templates.
    security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

    app.logger.info('App setup complete.')
    return app

app = create_app()

# import default controllers
from application.controllers.default import *
# import api controllers
from application.controllers.api import *
# import error handling controllers
from application.controllers.error_handlers import *

if __name__ == '__main__':
    app.run()