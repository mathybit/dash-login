import base64
from flask_login import UserMixin
import hashlib
import json
import random
import smtplib
import ssl
import string
import uuid

AUTH_CONFIG_FILE = "./config/auth.json"
USERS_FILE = "./config/userdb.json"

with open(AUTH_CONFIG_FILE) as f:
	config = json.load(f)

with open(USERS_FILE) as f:
	users = json.load(f)['credentials']


reset_email_template = """\
From: admin <{}>
Subject: Your new password

Your password has been reset. Your temporary password is: {}

THIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY.
"""

change_email_template = """\
From: admin <{}>
Subject: Your password has changed

Your password was recently changed. If this was you, you may ignore this message.

If you did not authorize this change, change your password immediately.

THIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY.
"""

adduser_email_template = """\
From: admin <{}>
Subject: Your new account

Your account has been created. 
Your username is: {}
Your temporary password is: {}

THIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY.
"""


# Extend the UserMixin class from flask-login (see flask-login documentation for details)
#
class User(UserMixin):
	def __init__(self, uid):
		attr = users[int(uid)]
		self.id = str(attr['id'])
		self.username = attr['username']
		self.email = attr['email']
	

# Returns a User given a UID, or None if the UID is not in the database
#
def get_user(uid):
	iuid = int(uid)
	if iuid >= 0 & iuid < len(users):
		return User(iuid)
	else:
		return None


# Returns a User given a username, or None if the username is not in the database
#
def get_user_by_name(uname):
	for user in users:
		if uname == user['username']:
			return User(user['id'])
	return None


# Used for login, checks the provided username and password against the stored
# encrypted database credentials.
#
def check_password(uname, upass):
	for user in users:
		if uname == user['username']:
			return check_hash(upass, user['password'])
	return False
			

# Helper function for check_password()
#
def check_hash(plaintext, hashed_password):
	p, salt = hashed_password.split(':')
	hashtext = hash_password(plaintext, salt)
	return hashtext == hashed_password


# Hashes a plaintext. One can specify the salt (this is needed in check_hash())
#
def hash_password(password, salt=None):
	# uuid is used to generate a random number for the salt
	if salt == None:
		salt = uuid.uuid4().hex
	return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


# Sends an email to the user with the specified message
#
def send_email(from_email, to_email, message):
	if not config['enable_email']:
		print('Emulating email send to', to_email + '.', 'Message:\n', message)
		return
	server = config['email_settings']['hostname']
	port = int(config['email_settings']['port'])
	
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(server, port, context=context) as server:
		server.login(
			config['email_settings']['username'],
			config['email_settings']['password']
		)
		server.sendmail(from_email, to_email, message)
	

# Part of forgot password functionality. Resets a user's password to a random
# string of lowercase letters (length 8 by default)
#
def reset_password(uname, passlength=8):
	for user in users:
		if uname == user['username']:
			letter_set = string.ascii_lowercase
			newpass = ''.join(random.choice(letter_set) for i in range(passlength))
			encpass = hash_password(newpass)
			#print(newpass, encpass)
			user['password'] = encpass
			
			from_email = config['email_settings']['from']
			msg = reset_email_template.format(from_email, newpass)
			send_email(from_email, user['email'], msg)
			
			with open(USERS_FILE, 'w') as f:
				json.dump({"credentials": users}, f)
			return True
	return False


# Allows a user to change their password on the profile page
#
def change_password(uname, curpass, newpass):
	for user in users:
		if uname == user['username']:
			if check_hash(curpass, user['password']):
				#print('change_password(): hash check passed')
				encpass = hash_password(newpass)
				user['password'] = encpass
				
				from_email = config['email_settings']['from']
				msg = change_email_template.format(from_email)
				send_email(from_email, user['email'], msg)
				
				with open(USERS_FILE, 'w') as f:
					json.dump({"credentials": users}, f)
				return True
			else:
				#print('change_password(): hash check failed')
				return False
	#print('change_password(): user not found:', uname)
	return False


# Add user functionality. It searches the user database to ensure the username
# or provided email don't already exist. If successful, creates a new user with
# ID one more than the max existing ID, with a randomly generated password of
# lowercase letters (length 8 by default)
#
def adduser(uname, email, passlength=8):
	uid = 0
	for user in users:
		if uname == user['username']:
			return 1
		elif email == user['email']:
			return 2
		uid = max(uid, int(user['id']))
	
	letter_set = string.ascii_lowercase
	newpass = ''.join(random.choice(letter_set) for i in range(passlength))
	encpass = hash_password(newpass)
	
	newuser = {
		'id': str(1 + uid),
		'username': uname,
		'password': encpass,
		'email': email
	}
	users.append(newuser)
	
	from_email = config['email_settings']['from']
	msg = adduser_email_template.format(from_email, uname, newpass)
	send_email(from_email, newuser['email'], msg)
	
	with open(USERS_FILE, 'w') as f:
		json.dump({"credentials": users}, f)
	return 0


# Delete user functionality. It searches the user database for the provided ID,
# and removes that entry.
#
def deluser(uid):
	user_to_remove = None
	for user in users:
		if uid == user['id']:
			user_to_remove = user
	
	if user_to_remove is not None:
		users.remove(user_to_remove)
		with open(USERS_FILE, 'w') as f:
			json.dump({"credentials": users}, f)




