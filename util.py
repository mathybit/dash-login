import base64
import numpy as np
import pandas as pd


def encode_image(image_file):
	with open(image_file, 'rb') as f:
		encoded = base64.b64encode(  f.read()  )
	return 'data:image/png;base64,{}'.format(encoded.decode())


def isna(value):
	"""
	Returns true if the given value is NaN. This can occur for np.nan but other types as well,
	hence the need for the second comparison. A NaN value will not equal itself.
	"""
	return (value is None) or (value is np.nan) or (value != value) or (str(value) == '')
