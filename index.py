from apps import login
import auth
import components as comp
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_login import current_user, logout_user

from app import app, config
from apps import app1, app2


# Overall app layout. The visible content is rendered based on the URL
#
app.layout = html.Div(children=[
	dcc.Location(id='url', refresh=False),
	
	comp.app_header(config['app_title']),
	
	comp.menu_bar(),
	
	html.Br(),
	
	html.Div(id='app-body', className='app-body', children=[]),
	
	comp.app_footer()
])


def layout():
	return html.Div(children=[
		html.Div('Place your index page body content here.')
	])


@app.callback(
	Output('app-body', 'children'),
	[ Input('url', 'pathname') ])
def display_page(pathname):
	allow = False
	authed = current_user.is_authenticated
	if pathname in config['protected_paths']:
		if authed:
			allow = True
		else:
			return login.layout_login_required()
	else:
		allow = True
	
	if pathname == '/': #index page is not protected
		return layout()
	elif pathname == '/login': #login page shouldn't depend on 'allow'
		return login.layout_login()
	elif pathname == '/reset_password': #reset password page shouldn't depend on 'allow'
		return login.layout_reset()
	elif pathname == '/reset_success':
		return login.layout_reset_success()
	elif pathname == '/reset_failure':
		return login.layout_reset_failure()
	elif pathname == '/success' and authed:
		return login.layout_success()
	elif pathname == '/failure':
		return login.layout_failure()
	elif pathname == '/change_password' and authed:
		return login.layout_change()
	elif pathname == '/profile' and authed:
		return login.layout_profile()
	
	elif pathname == '/adduser' and authed:
		if current_user.id == '0':
			return login.layout_adduser()
		else:
			return comp.not_found(pathname)
	elif pathname == '/adduser_success' and authed:
		if current_user.id == '0':
			return login.layout_adduser_success()
		else:
			return comp.not_found(pathname)
	elif pathname == '/adduser_failure1' and authed:
		if current_user.id == '0':
			return login.layout_adduser_failure(1)
		else:
			return comp.not_found(pathname)
	elif pathname == '/adduser_failure2' and authed:
		if current_user.id == '0':
			return login.layout_adduser_failure(2)
		else:
			return comp.not_found(pathname)
	
	elif pathname == '/deluser' and authed:
		if current_user.id == '0':
			return login.layout_deluser()
		else:
			return comp.not_found(pathname)
	elif pathname == '/logout': #logout page shouldn't depend on 'allow'
		if current_user.is_authenticated:
			logout_user()
			return login.layout_logout()
		else:
			return login.layout_logout2()
	
	# Here you add your own apps. We include 2 apps as an example.
	# App 1 requires authentication. App 2 does not. This is set in the config.json file.
	elif pathname == '/app1' and allow:
		return app1.layout()
	elif pathname == '/app2' and allow:
		return app2.layout()
	
	else:
		return comp.not_found(pathname)


if __name__ == '__main__':
	app.run_server(port=config['port'], debug=config['debug'])

