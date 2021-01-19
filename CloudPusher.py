#!/usr/bin/env python3

# CloudPusher.py
#
# This script monitors the logfile of WSJT-X or 
# JTDX and uploads new log entries to Cloudlog 
# URL: https://www.magicbug.co.uk/cloudlog/
#
# Orignal version from Christopher, M0YNG
# URL: https://m0yng.uk/2020/05/Cloudpusher-logging-WSJT-X-to-Cloudlog/
#
# Modified by Michael Clemens, DL6MHC


# Imports for stuff
import configparser
import requests
import os
import time

# read in the config
config = configparser.ConfigParser()
config.read('config.ini')

# Some fixed common things
qsourl = '/index.php/api/qso'

# What to do when we find a new contact
def pushContact(filename, lines):
    for line in lines:
        r = requests.post(
            config['cloudlog']['host'] + qsourl,
            json={"key": config['cloudlog']['key'],
                  "type": "adif",
                  "string": line
                  }
        )
        if r.status_code == 201:
            print("Log uploaded to Cloudlog.")
        else:
            print('Something went wrong')
            print(r.text)

# open log file and set the pointer to its last line
def openFile(filename):
    if os.path.isfile(filename):
        logfile = open(filename, "r")
        logfile.seek(os.path.getsize(logfile.name)) 
        print("Watching file %s" % filename)
        return logfile
    else:
        print ("%s does not exist" % filename)

# monitor the logfile for new lines
def loop(logfile):
    while 1:
        new_entry = logfile.readlines()
        if new_entry:
            pushContact(logfile.name, new_entry)
        time.sleep(1)

# open log file
logfile = openFile(config['cloudlog']['file'])

# start the watching
if not logfile:
    print("Something went wrong while opening the log file")
else:
    loop(logfile)
