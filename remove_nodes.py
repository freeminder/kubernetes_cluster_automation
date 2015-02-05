#!/usr/bin/env python
import dosa
from subprocess import call
import random
import string
import urllib
import urllib2
import fileinput
import shutil
import os
import sys
import time
from myconfig import *


# set variables
# dosa.set_debug()  # enables debug logs
client = dosa.Client(api_key=API_KEY)
HOME = os.environ['HOME']
os.environ['DO_TOKEN'] = API_KEY
os.environ['DISCOVERY_URL'] = urllib2.urlopen("https://discovery.etcd.io/new").read()
os.environ['NUM_OF_DROPLETS'] = str(CLUSTER_SIZE)

x = 1
z = 0 - CLUSTER_SIZE
while x <= CLUSTER_SIZE:
	client.droplets.delete(client.droplets.list()[-1]["droplets"][z]["id"])
	x += 1
	z += 1
