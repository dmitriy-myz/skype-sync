#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import json
import time
from skype import Skype
from slack import Slack
with open('config.json') as f:
    settings = json.load(f)
    USERTOKENSTRING = settings['slack']['USERTOKENSTRING']
    CHANNEL_ID = settings['slack']['CHANNEL_ID']
    slack_oldest = settings['slack']['oldest']
    SkypeChatId = settings['skype']['ChatId']
    delay = 1.0

def writeSettings():
    settings['slack']['oldest'] = slack_oldest
    with open('config.json', 'w') as f:
        json.dump(settings, f)

def onMsgReceive(msg):
    print "==================="
    print "received message"
    print "messenger: %s" % (msg["messenger"])
    print "channel: %s" %(msg["chat"])
    print "from: %s" %(msg["sender"])
    print "text: %s" %(msg["text"])
    #print "[%s] (%s): %s" %(msg["messenger"], msg["sender"], msg["text"])

skypeAPI = Skype()
skypeAPI.Attach();
skypeAPI.onMsgReceive = onMsgReceive

slack = Slack(settings['slack']['USERTOKENSTRING'], settings['slack']['CHANNEL_ID'], True)
slack.onMsgReceive = onMsgReceive
thread = threading.Thread(target=slack.main)
thread.daemon = True
thread.start()

while True:
    raw_input()
    time.sleep(1.0)