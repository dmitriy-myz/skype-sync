#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
#from skype.skype import Skype
from slack.slack import Slack

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
    """

    print "==================="
    for channelId in channels:
        if msg["messenger"] in channels[channelId]:
            if msg["source"] in channels[channelId][msg["messenger"]]:
#                print "msg source in list"
#                print "internal channelId = ", channelId
                sendMsg(msg, channelId)
                break

def sendMsg(msg, channelId):
    for messenger in channels[channelId]:
        for channel in channels[channelId][messenger]:
            if not ((msg["source"] == channel) and (msg["messenger"] == messenger)):
                print "send message to channel: ", channel
                print "on messenger: ", messenger
                msgText = "[%s] (%s): %s" %(msg["messenger"], msg["sender"], msg["text"])
                messengers[messenger](msgText, messenger)

#skype = Skype()
#skype.onMsgReceive = onMsgReceive
def sendMsgSkype(msg, target):
    #requests.post("https://api.slack.com/api/chat.postMessage", params = params)
    print "send message on skype, channel: ", target
    print msg


slack = Slack('settings/slack.json', False)
slack.onMsgReceive = onMsgReceive

messengers = dict()
messengers["slack"] = slack.sendMsg
messengers["skype"] = sendMsgSkype






while True:
    raw_input()
    time.sleep(1.0)
