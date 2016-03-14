#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
#from skype import Skype
from slack import Slack

with open('config.json') as f:
    settings = json.load(f)
    channels = settings["channels"]
#["skype"]["admin"]["#dmuzyca/$8cbca70aee978773"]
#["slack"]["admin"]["C06RKSGDQ"]

def onMsgReceive(msg):
    """
    print "==================="
    print "received message"
    print "messenger: %s" % (msg["messenger"])
    print "source: %s" %(msg["source"])
    print "from: %s" %(msg["sender"])
    print "text: %s" %(msg["text"])
    messenger = msg["messenger"]
    #print "[%s] (%s): %s" %(msg["messenger"], msg["sender"], msg["text"])
    """

    print "==================="
    for channelId in channels:
        if msg["messenger"] in channels[channelId]:
            if msg["source"] in channels[channelId][msg["messenger"]]:
                print "msg source in list"
                print "internal channelId = ", channelId
                sendMsg(msg, channelId)
                break

def sendMsg(msg, channelId):
    for messenger in channels[channelId]:
        for channel in channels[channelId][messenger]:
            if not ((msg["source"] == channel) and (msg["messenger"] == messenger)):
                print "send message to channel: ", channel
                print "on messenger: ", messenger
                print "[%s] (%s): %s" %(msg["messenger"], msg["sender"], msg["text"])

#skype = Skype()
#skype.onMsgReceive = onMsgReceive

slack = Slack('slack.json', False)
slack.onMsgReceive = onMsgReceive

while True:
    raw_input()
    time.sleep(1.0)
