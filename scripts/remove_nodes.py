#!/usr/bin/env python
import dosa
from subprocess import call, check_output
import random, string, urllib, urllib2, fileinput, shutil, os, sys, time, re
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from myconfig import *


# set variables
# dosa.set_debug()  # enables debug logs
client = dosa.Client(api_key=API_KEY)
HOME = os.environ['HOME']
os.environ['DO_TOKEN'] = API_KEY
os.environ['DISCOVERY_URL'] = urllib2.urlopen("https://discovery.etcd.io/new").read()
os.environ['NUM_OF_DROPLETS'] = str(CLUSTER_SIZE)
droplet_name = "tcore"


x = 1
z = 0 - CLUSTER_SIZE
while x <= CLUSTER_SIZE:
	if droplet_name in client.droplets.list()[-1]["droplets"][z]["name"]:
		client.droplets.delete(client.droplets.list()[-1]["droplets"][z]["id"])
		print("Node " + client.droplets.list()[-1]["droplets"][z]["name"] + " deleted.")
	x += 1
	z += 1
