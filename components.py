import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as datetime
import json
import util


# The app header component
#
def app_header(title):
	return html.Div(className='app-header', children=[
		html.A(children=[
			html.Div(className='app-header-logo-container', children=[
				html.Img(className='app-header-logo', src=util.encode_image('./assets/logo1.png'), height=60),
			]),
		], href='https://mathybit.github.io/', target='_blank'),
		
		html.Div(className='app-header-title', children=[title])
	])


def menu_bar():
	return html.Div(className='menu-bar', children=[
		html.Div(className='menu-bar-left', children=[
			html.Div(className='menu-option', children=[
				dcc.Link(html.Button('Index', className='custom-button-menu'), href='/')
			]),
			html.Div(className='menu-option', children=[
				dcc.Link(html.Button('App 1', className='custom-button-menu'), href='/app1')
			]),
			html.Div(className='menu-option', children=[
				dcc.Link(html.Button('App 2', className='custom-button-menu'), href='/app2')
			])
		], style={'display': 'inline-block'}),
		
		html.Div(
			id='user-display', 
			className='menu-bar-right', 
			children=[], 
			style={'float': 'right', 'display': 'inline-block'}
		)
	])


# The app footer component
#
def app_footer():
	return html.Div(className='app-footer', children=[
		html.Hr(className='app-footer-separator'),
		html.Div(className='app-footer-content', children=[
			html.P('The MIT License'),
			html.P('Copyright (c) ' + str(datetime.today().year) + ' Adrian Pacurar'),
			html.P("""
				Permission is hereby granted, free of charge, to any person obtaining a copy of this 
				software and associated documentation files (the "Software"), to deal in the Software 
				without restriction, including without limitation the rights to use, copy, modify, merge, 
				publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
				to whom the Software is furnished to do so, subject to the following conditions:
			"""),
			html.P("""
				The above copyright notice and this permission notice shall be included in all copies or 
				substantial portions of the Software.
			"""),
			html.P("""
				THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
				BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
				NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
				DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
				OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
			""")
		])
	])


# Not found error when the user attempt to access a path
#
def not_found(pathname):
	return html.Div(children=[
		html.H3('404 Page not found'),
		html.P(children=[pathname], style={'color': '#6f6f70'}),
		html.P('We could not find the above page on this server.')
	])


