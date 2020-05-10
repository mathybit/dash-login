import argparse
import base64
import hashlib
import uuid

def hash_password(password, salt=None):
	# uuid is used to generate a random number
	if salt == None:
		salt = uuid.uuid4().hex
	return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

parser = argparse.ArgumentParser(description='Password Hash Generator.')
parser.add_argument('password', metavar='password', type=str, help='The password string to be hashed.')
args = parser.parse_args()

print(hash_password(args.password))
