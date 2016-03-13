#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
#from skype import Skype
from slack import Slack

with open('config.json') as f:
    settings = json.load(f)
    USERTOKENSTRING = settings['slack']['USERTOKENSTRING']
    CHANNEL_ID = settings['slack']['CHANNEL_ID']
    slack_oldest = settings['slack']['oldest']
    SkypeChatId = settings['skype']['ChatId']

def writeSettings():
    settings['slack']['oldest'] = slack_oldest
    with open('config.json', 'w') as f:
        json.dump(settings, f)

#class message proceed
#link one channel to other

#["skype"]["admin"]["#dmuzyca/$8cbca70aee978773"]
#["slack"]["admin"]["C06RKSGDQ"]
"""
settings.skype.chats.1.id

channels.1.skype.id
channels.1.slack.id1
channels.1.slack.id2
"channels": { "1": {
        "skype": ["#dmuzyca/$8cbca70aee978773"],
        "slack": ["C06RKSGDQ"]
    }
}


"""
def onMsgReceive(msg):
    print "==================="
    print "received message"
    print "messenger: %s" % (msg["messenger"])
    print "source: %s" %(msg["source"])
    print "from: %s" %(msg["sender"])
    print "text: %s" %(msg["text"])
    messenger = msg["messenger"]
    #print "[%s] (%s): %s" %(msg["messenger"], msg["sender"], msg["text"])
    for channelId in channels:
        if msg["messenger"] in channels[channelId]:
            if msg["source"] in channels[channelId][msg["messenger"]]
                print "msg source in list"
                print "internal channelId = ", channelId
                break


skype = Skype()
skype.onMsgReceive = onMsgReceive

slack = Slack(settings['slack']['USERTOKENSTRING'], settings['slack']['CHANNEL_ID'], True)
slack.onMsgReceive = onMsgReceive

while True:
    raw_input()
    time.sleep(1.0)
