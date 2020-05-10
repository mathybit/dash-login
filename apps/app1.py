import components as comp
import dash_core_components as dcc
import dash_html_components as html
from flask_login import logout_user, current_user


def layout():
	return html.Div(children=[
		html.Div('Place your App 1 body content here.'),
		html.Div('This app is login-protected. If you are seeing this, you successfully logged in.'),
		html.Br(),
		html.Div('A non-authenticated user will be redirected to the login page if they try to access this.'),
	])
