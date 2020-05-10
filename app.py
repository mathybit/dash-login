import auth
from auth import User
import dash
import flask
from flask_login import LoginManager, UserMixin
import json
import os

CONFIG_FILE = './config/config.json'

with open(CONFIG_FILE) as f:
	config = json.load(f)


# Create the app
#
app = dash.Dash(__name__)
app.title = config['app_name'] #this gets displayed in the window name
app.config['suppress_callback_exceptions'] = config['suppress_callback_exceptions']

# Overwrite the default Dash favicon
#
server = app.server
@server.route('/favicon.ico')
def favicon():
	return flask.send_from_directory(
		os.path.join(server.root_path, 'static'), 
		'favicon.ico'
	)


# Logic needed for authentication
#
server.config.update(
	SECRET_KEY = os.urandom(12)
)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(uid):
	#print('load_user() triggered')
	return auth.get_user(uid)

