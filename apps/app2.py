import components as comp
import dash_core_components as dcc
import dash_html_components as html
from flask_login import logout_user, current_user


def layout():
	return html.Div(children=[
		html.Div('Place your App 2 body content here.'),
		html.Div('This app is NOT login-protected.'),
		html.Br(),
		html.Div('A user does not need to be logged in to view this.'),
		html.Br(),
		html.Div('If you want to protect this page, add \'/app2\' to the configuration file config.json.')
	])
