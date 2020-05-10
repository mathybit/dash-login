import auth
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
from flask_login import login_user, current_user, logout_user
import util
from app import app, User


DELAY = 3 #the redirect delay in seconds


#################################################################################
################## Components and callbacks for the login page ##################

# The login form
#
def login_form():
	return html.Div(className='login-form', children=[
		html.Div(className='login-form-input', children=[
			dcc.Input(id='login-form-input-user', value='', placeholder='Username...'),
		]),
		html.Div(className='login-form-input', children=[
			dcc.Input(id='login-form-input-pass', value='', placeholder='Password...', type='password'),
		]),
		html.Br(),
		html.Button('Login', id='login-form-button', n_clicks=0, className='custom-button'),
		' ',
		dcc.Link(html.Button('Cancel', n_clicks=0, className='custom-button'), href='/'),
		html.Br(),
		html.P(id='login-form-forgot-password', children=[
			dcc.Link('I forgot my password', href='/reset_password')
		])
	])


# The standard login page
#
def layout_login():
	return html.Div(children=[
		dcc.Location(id='url_login', refresh=True),
		
		login_form()
	])


# The login page when a non-authenticated user tries to access a restricted page
#
def layout_login_required():
	return html.Div(children=[
		dcc.Location(id='url_login', refresh=True),
		
		html.Div('You are trying to access a restricted page. Please login to continue.'),
		html.Br(),
		login_form()
	])


# The callback function which logs a user in
#
@app.callback(
	Output('url_login', 'pathname'),
	[ Input('login-form-button', 'n_clicks') ],
	[
		State('login-form-input-user', 'value'),
		State('login-form-input-pass', 'value'),
		State('url_login', 'pathname')
	])
def login(clicks, username, password, current_state):
	#print('login() triggered')
	if clicks > 0:
		if auth.check_password(username, password):
			#print('pass valid')
			user = auth.get_user_by_name(username)
			login_user(user)
			return '/success'
		else:
			#print('pass invalid')
			return '/failure'
	else:
		return current_state



#################################################################################
################## Components and callbacks login success/fail ##################

# The login failure page
#
def layout_failure():
	return html.Div(children=[
		dcc.Location(id='url_login', refresh=True),
		
		html.Div('You entered the wrong username or password. Please try again.'),
		login_form()
	])


# The successful login page. This contains an Interval component which redirects the user
# after counting down for 'DELAY' seconds.
#
def layout_success():
	return html.Div(children=[
		dcc.Location(id='url_success', refresh=True),
		
		dcc.Interval(
			id='interval-component',
			interval=1000, # in milliseconds
			n_intervals=1
        ),
		
		html.Div(children=[
			'You successfully logged in. You will be redirected to index page in ',
			html.Label(id='remaining-delay'),
			' ...'
		])
	])

# The redirect callback for a successful login
#
@app.callback(
	Output('url_success', 'pathname'),
	[ Input('interval-component', 'n_intervals')],
	[ State('url_success', 'pathname') ])
def redirect_success(n, current_state):
	if n == DELAY:
		return '/'
	else:
		return current_state

@app.callback(
	Output('remaining-delay', 'children'),
	[ Input('interval-component', 'n_intervals')])
def update_time_remaining(n):
	return str(1 + DELAY - n)



#################################################################################
################### Components and callbacks for profile page ###################

# Display the login button, or the 'You are logged in as ...' message depending
# on auth status.
#
def user_display(username=None): 
	if username == None:
		return html.Div(children=[
			dcc.Link(children=[
				html.Button('Sign in', className='custom-button-menu')
			], href='/login')
		])
	else:
		return html.Div(children=[
			html.Label(className='user-display-text', children=[
				'You are logged in as: ',
				dcc.Link(username, href='/profile')
			]),
			dcc.Link(href='/logout', children=[
				html.Button('Logout', id='logout-button', n_clicks=0, className='custom-button-menu')
			])
		])


@app.callback(
	Output('user-display', 'children'),
	[ Input('app-body', 'children') ])
def user_display_callback(dummy):
	if current_user.is_authenticated:
		return user_display(username=current_user.username)
	else:
		return user_display()


# The user profile page
#
def layout_profile():
	admin_controls = None
	if current_user.id == '0':
		admin_controls = html.Div(children=[
			html.H4('Admin Controls'),
			dcc.Link('Add User', href='/adduser'),
			html.Br(),
			dcc.Link('Delete User', href='/deluser')
		])
	
	return html.Div(children=[
		html.H4('User Information'),
		html.Div(children=[
			html.Label('User ID: '),
			current_user.id
		]),
		html.Div(children=[
			html.Label('Username: '),
			current_user.username
		]),
		html.Div(children=[
			html.Label('Email: '),
			current_user.email
		]),
		html.Br(),
		dcc.Link('Change my password', href='/change_password'),
		html.Br(),
		html.Br(),
		admin_controls
	])



#################################################################################
################# Components and callbacks for change pass page #################

# The change password form
#
def change_password_form():
	return html.Div(className='change-form', children=[
		html.Div(className='change-form-input', children=[
			dcc.Input(id='change-form-input-pass', 
				value='', placeholder='Current password...', type='password'),
		]),
		html.Div(className='change-form-input', children=[
			dcc.Input(id='change-form-input-newpass0', 
				value='', placeholder='New password...', type='password'),
		]),
		html.Div(className='change-form-input', children=[
			dcc.Input(id='change-form-input-newpass1', 
				value='', placeholder='Re-enter new password...', type='password'),
		]),
		html.Br(),
		html.Button('Change', id='change-form-button', n_clicks=0, className='custom-button'),
		' ',
		dcc.Link(html.Button('Cancel', n_clicks=0, className='custom-button'), href='/profile'),
		
		html.Br(),
		html.Div(id='change-password-feedback', className='change-form-input', children=None)
	])


# The layout for the change password page
#
def layout_change():
	return html.Div(children=[
		dcc.Location(id='url_change', refresh=True),
		
		change_password_form()
	])


# Change the user's password
#
@app.callback(
	Output('change-password-feedback', 'children'),
	[ Input('change-form-button', 'n_clicks') ],
	[
		State('change-form-input-pass', 'value'),
		State('change-form-input-newpass0', 'value'),
		State('change-form-input-newpass1', 'value'),
		State('change-password-feedback', 'children')
	])
def change_password(clicks, curpass, newpass0, newpass1, current_state):
	if clicks > 0:
		if newpass0 != newpass1:
			return 'Error!'
		
		user = current_user.username
		if auth.change_password(user, curpass, newpass0):
			return 'Success!'
		else:
			#print('pass change fail: auth.change_pass() returned False')
			return 'Error!'
	else:
		return current_state


@app.callback(
	Output('url_change', 'pathname'),
	[ Input('change-password-feedback', 'children') ],
	[ State('url_change', 'pathname') ])
def change_password_redirect(changemsg, current_state):
	if util.isna(changemsg) or (changemsg == 'Error!'):
		return current_state
	else:
		return '/profile'



#################################################################################
################### Components and callbacks for logout page ####################

# The standard logout page
#
def layout_logout():
	return html.Div(children=[
		html.Div('You successfully logged out.')
	])


# If a non-authenticated user tries to access /logout, show this instead
#
def layout_logout2():
	return html.Div(children=[
		html.Div('You are not logged in. You may want to try logging in first.')
	])



#################################################################################
################## Components and callbacks for password reset ##################

# The reset password form
#
def reset_password_form():
	return html.Div(className='reset-form', children=[
		html.Div(className='reset-form-input', children=[
			dcc.Input(id='reset-form-input-user', value='', placeholder='Username...'),
		]),
		html.Br(),
		html.Button('Reset', id='reset-form-button', n_clicks=0, className='custom-button'),
		' ',
		dcc.Link(html.Button('Cancel', n_clicks=0, className='custom-button'), href='/')
	])


# The reset password page and its associated layouts
#
def layout_reset():
	return html.Div(children=[
		dcc.Location(id='url_reset', refresh=True),
		
		reset_password_form()
	])

def layout_reset_success():
	return html.Div(children=[
		html.Div('Your password was reset. A temporary password was sent to your email.')
	])

def layout_reset_failure():
	return html.Div(children=[
		html.Div('We were unable to reset your password. Please check your username and try again.')
	])


# Reset the user's password
#
@app.callback(
	Output('url_reset', 'pathname'),
	[ Input('reset-form-button', 'n_clicks') ],
	[
		State('reset-form-input-user', 'value'),
		State('url_reset', 'pathname')
	])
def reset_password(clicks, username, current_state):
	#print('reset_password() triggered')
	if clicks > 0:
		if auth.reset_password(username.lower()):
			#print('pass reset success')
			return '/reset_success'
		else:
			#print('pass reset failed')
			return '/reset_failure'
	else:
		return current_state



##################################################################################
################## Components and callbacks for adding new user ##################

def add_user_form():
	return html.Div(className='adduser-form', children=[
		html.Div(className='adduser-form-input', children=[
			dcc.Input(id='adduser-form-input-user', value='', placeholder='Username...'),
		]),
		html.Div(className='adduser-form-input', children=[
			dcc.Input(id='adduser-form-input-email', value='', placeholder='Email...'),
		]),
		html.Br(),
		html.Button('Add', id='adduser-form-button', n_clicks=0, className='custom-button'),
		' ',
		dcc.Link(html.Button('Cancel', n_clicks=0, className='custom-button'), href='/profile')
	])

def layout_adduser():
	return html.Div(children=[
		dcc.Location(id='url_adduser', refresh=True),
		add_user_form()
	])

def layout_adduser_success():
	return html.Div(children=[
		dcc.Location(id='url_adduser', refresh=True),
		html.Div('The user was successfully added. A temporary password will be sent to the provided email.'),
		html.Br(),
		add_user_form()
	])

def layout_adduser_failure(adduser_code):
	if adduser_code == 1:
		return html.Div(children=[
			dcc.Location(id='url_adduser', refresh=True),
			html.Div('The provided username already exists. Please try again.'),
			html.Br(),
			add_user_form()
		])
	elif adduser_code == 2:
		return html.Div(children=[
			dcc.Location(id='url_adduser', refresh=True),
			html.Div('The provided email address already has an account associated with it. Please try again.'),
			html.Br(),
			add_user_form()
		])

# Add a new user
#
@app.callback(
	Output('url_adduser', 'pathname'),
	[ Input('adduser-form-button', 'n_clicks') ],
	[
		State('adduser-form-input-user', 'value'),
		State('adduser-form-input-email', 'value'),
		State('url_adduser', 'pathname')
	])
def adduser(clicks, username, email, current_state):
	#print('adduser() triggered')
	if clicks > 0:
		adduser_code = auth.adduser(username.lower(), email.lower())
		if adduser_code == 0:
			#print('adduser success')
			return '/adduser_success'
		else:
			#print('adduser failed:', adduser_code)
			if adduser_code == 1:
				return '/adduser_failure1'
			elif adduser_code == 2:
				return '/adduser_failure2'
	else:
		return current_state


##################################################################################
################## Components and callbacks for deleting a user ##################

dt_css = [
	{
		'selector': '.dash-cell div.dash-cell-value',
		'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
	}
]
dt_style_header = {
	'color': '#483d3f',
	'backgroundColor': '#e8e8ea',
	'fontWeight': 'bold'
}
dt_style_cell = {
	'whiteSpace': 'no-wrap',
	'overflow': 'hidden',
	'textOverflow': 'ellipsis',
	'maxWidth': 0,
	'backgroundColor': '#f4f4f4',
	'textAlign': 'center'
}
dt_style_cell_conditional = [
	{'if': {'column_id': 'ID'}, 'width': '50px', 'textAlign': 'center'},
	{'if': {'column_id': 'Username'}, 'width': '120px', 'textAlign': 'right'},
	{'if': {'column_id': 'Email'}, 'width': '250px', 'textAlign': 'right'}
]
dt_style_table = {
	'maxHeight': '250px' #326
	#'overflowY': 'scroll'
}

def deluser_datatable():
	columns = ['ID', 'Username', 'Email']
	records = [
		{
			'ID': user['id'],
			'Username': user['username'],
			'Email': user['email']
		} for user in auth.users if (user['id'] not in ['0'])
	]
	return dt.DataTable(
		id='deluser-table',
		data=records,
		columns=[ {'id': c, 'name': c} for c in columns ],
		css=dt_css,
		style_header=dt_style_header,
		style_cell=dt_style_cell,
		style_cell_conditional=dt_style_cell_conditional,
		n_fixed_rows=1,
		style_table=dt_style_table,
		row_deletable=True
	)


def layout_deluser():
	return html.Div(className='deluser-table-wrapper', children=[
		html.Div(id='deluser-dummy-output', children=None, style={'display':'none'}),
		deluser_datatable()
	])


@app.callback(
	Output('deluser-dummy-output', 'children'),
	[ Input('deluser-table', 'derived_virtual_data') ],
	[ State('deluser-table', 'data_previous') ])
def deluser(virtual_in, previous_in):
	virtual = []
	previous = []
	
	if util.isna(virtual_in) or (len(virtual_in) == 0) or (len(virtual_in[0].keys()) == 0):
		virtual = []
	else:
		virtual = virtual_in
	
	if previous_in == None:
		previous = []
	else:
		previous = previous_in
	
	uidvirt = set([item['ID'] for item in virtual])
	uidprev = set([item['ID'] for item in previous])
	
	# When deleting a row, the derived_virtual_data property will hold less values than
	# the data_previous. By examining the difference, we determine which ID was deleted.
	if len(virtual) < len(previous):
		diff = uidprev - uidvirt
		for uid in diff:
			auth.deluser(uid)
	return None





