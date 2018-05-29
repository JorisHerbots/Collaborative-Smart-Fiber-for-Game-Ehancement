import re
import math

with open('colors.txt', 'r') as f:
	for line in f:
		# Pink 	FF C0 CB	255 192 203
		matchObj = re.match( r'(.*) (.*) (.*) (.*) ([0-9]*) ([0-9]*) ([0-9]*)', line.strip(), re.M|re.I)
		name = "_".join(re.findall('[A-Z][^A-Z]*', matchObj.group(1)))
		print(name.upper() + " = " + "Color(" + matchObj.group(5) + ", " + matchObj.group(6) + ", " + matchObj.group(7) + ")")
