#!/usr/bin/python
# -*- coding: utf-8 -*-

import Skype4Py
import time
import requests
import json
import threading

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = " %(attr)

# Set your config variables from the config.json file
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
class Skype:
    def __init__(self):
        skype = Skype4Py.Skype();
        skype.OnMessageStatus = self.onMsg
        skype.Attach();
    
    def onMsg(self, Message, Status):
        msg = dict()
        if Status == 'RECEIVED':
            if Message.Sender.FullName == "":
                msg["sender"] = Message.Sender.Handle
            else:
                msg["sender"] = Message.Sender.FullName
            msg["text"] = Message.Body
            msg["messenger"] = "skype"
            msg["chat"] = Message.Chat.Name
#            msg = "[skype] (%s): %s" % (Name, Message.Body)
            onMsgReceive(msg)
#            if SkypeChatId in Message.Chat.Name:
#                sendSlackMsg(msg)
    #commands
    def sendMsg(self, msg):
        for chat in skype.Chats:
            if SkypeChatId in chat.Name:
                chat.SendMessage(msg)
                print chat.Name 

class Slack:
    def __init__(self, userToken=None, channelId=None):
        self._token = userToken
        self._channelId = channelId
        self._users = self._loadUsers()
        self._oldest = 0
        self._maxDelay = 5.0
        self._minDelay = 1.0
        self._delay = 1.0
    def memberList(self):
        userNames = []
        params = {"token": self._token, "channel": self._channelId}
        response = requests.post("https://api.slack.com/api/channels.info", params = params)
        members = json.loads(response.text.decode('utf-8'), encoding = 'utf-8')["channel"]["members"]
        for member in members:
            userName = self.findUser(member)
            userNames.append(userName)
        return "\n".join(userNames)
    def sendMsg(self, msg):
        params = {"token": self._token, "channel": self._channelId, "text": msg}
        requests.post("https://api.slack.com/api/chat.postMessage", params = params)
        print msg
    def _loadUsers(self):
        params = {"token": self._token, "channel": self._channelId}
        responseUser = requests.get("https://slack.com/api/users.list",params=params)
        users = json.loads(responseUser.text)["members"]
        return users
    def findUser(self, userId, recurcive=True):
        for user in self._users:
            if userId == user["id"]:
                return user["name"]
        if recursive:
            self._users = self._loadUsers()
            return self.findUser(userId, False)
    def getHistory(self):
        msg = dict()
        params = {"token": self._token, "channel": self._channelId, "oldest": self._oldest}
        response = requests.post("https://slack.com/api/channels.history", params=params)
        messages = json.loads(response.text.decode('utf-8'), encoding = 'utf-8')["messages"]
        msgCount = len(messages)
        for message in reversed(messages):
            if "username" in message:
                msg["sender"] = message["username"]
            else:
                msg["sender"] = self.findUser(message["user"])
            msg["text"] = message["text"]
            msg["chat"] = self._channelId
            msg["messenger"] = "slack"
            if not "bot" in msg["sender"]:
                onMsgReceive(msg)
            if float(self._oldest) <= float(message["ts"]):
                self._oldest = str(message["ts"])
                #writeSettings()
        return msgCount
    def smartDelay(self, msgCount, currentDelay):
        if msgCount != 0:
            return self._minDelay
        elif currentDelay < self._maxDelay:
            return currentDelay+0.1
        else:
            return self._maxDelay
    def main(self):
        while True:
            time.sleep(self._delay)
            try:
                msgCount = self.getHistory()
                self._delay = self.smartDelay(msgCount, delay)
            except Exception as e:
               print(e)

def onMsgReceive(msg):
    print "==================="
    print "received message"
    print "messenger: %s" % (msg["messenger"])
    print "channel: %s" %(msg["chat"])
    print "from: %s" %(msg["sender"])
    print "text: %s" %(msg["text"])
    #print "[%s] (%s): %s" %(msg["messenger"], msg["sender"], msg["text"])

slack = Slack(settings['slack']['USERTOKENSTRING'], settings['slack']['CHANNEL_ID'])
#skype = Skype()

thread = threading.Thread(target=slack.main)
thread.daemon = True
thread.start()
while True:
    raw_input()
    time.sleep(1.0)
