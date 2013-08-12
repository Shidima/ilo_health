#!/usr/bin/env python

"""
@author 	Christiaan Janssen
@contact 	menicus@gmail.com
@license	GPL
"""

import hpilo
import argparse
import sys

# Setup command line argument parser:
parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="Host to performe the health check on")
parser.add_argument("-u", "--user_name", help="ilo user name" )
parser.add_argument("-p", "--password", help="ilo password")

args = parser.parse_args()

# Create the iLo instance to check:
ilo = hpilo.Ilo(args.hostname, args.user_name, args.password).get_embedded_health()

state = "OK"
# Parse the returnvalues
for key in ilo:
	# The information we are intrested in:
	if(key == "health_at_a_glance"):
		for i, l in ilo[key].items():
			for m in l:
				if (m  == "status"):
					#print "{} => {}".format(i, ilo[key][i][m])
					# Some how the drive state is Ok and not OK...
					# so we need to check for both:
					if (ilo[key][i][m] == "OK" or ilo[key][i][m] == "Ok"): 
						state = "OK"
					else:
						# If the state of my hardware is not ok that is a critical
						# fail for me:
						state = "CRITICAL"


# The return statusses we need for nagios
if state == "OK":
	print "Ilo State - {}".format(state)
	sys.exit(0)
elif state == "WARNING":
	print "Ilo State - {}".format(state)
	sys.exit(1)
elif state ==  "CRITICAL":
	print "Ilo State - {}".format(state)
	sys.exit(2)
else:
	print "Ilo State - {}".format(state)
	sys.exit(3)

