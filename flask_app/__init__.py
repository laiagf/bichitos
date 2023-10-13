
from flask import Flask

from flask_app.config import Config


import datetime 


def create_app(config_class=Config):

	app = Flask(__name__)
	app.config.from_object(Config)
	

	#from flask_app.users.routes import users
	#from flask_app.science.routes import science
	#from flask_app.projects.routes import projects
	#from flask_app.equipment.routes import equipment
	from flask_app.main.routes import main
	#from flask_app.errors.handlers import errors

	#app.register_blueprint(users)
	#app.register_blueprint(science)
	#app.register_blueprint(projects)
	#app.register_blueprint(equipment)
	app.register_blueprint(main)
	#app.register_blueprint(errors)
	return app
