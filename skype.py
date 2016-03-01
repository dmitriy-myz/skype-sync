#!/usr/bin/python
# -*- coding: utf-8 -*-

import Skype4Py
import time
import requests
import json

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

def onSkypeMsg(Message, Status):
    if Status == 'RECEIVED':
        if Message.Sender.FullName == "":
            Name = Message.Sender.Handle
        else:
            Name = Message.Sender.FullName
        msg = "[skype] (%s): %s" % (Name, Message.Body)
        if SkypeChatId in Message.Chat.Name:
            sendSlackMsg(msg)
#commands
        if "!ping" in Message.Body:
            print msg
            Message.Chat.SendMessage("pong")
        elif "!members" in Message.Body:
            print msg
            answer = memberListSlack()
            answer = "Slack: %s" %(answer)
            Message.Chat.SendMessage(answer)


def memberListSlack():
    userNames = []
    token = USERTOKENSTRING
    params = {"token": token, "channel": CHANNEL_ID}
    response = requests.post("https://api.slack.com/api/channels.info", params = params)
    members = json.loads(response.text.decode('utf-8'), encoding = 'utf-8')["members"]
    for member in members:
        UserName = findUser(member)
        userNames.append(UserName)
    return "\n".join(userNames)


def sendSkypeMsg(msg):
    for chat in skype.Chats:
        if SkypeChatId in chat.Name:
            chat.SendMessage(msg)
            print chat.Name 

def sendSlackMsg(msg):
    token = USERTOKENSTRING
    params = {"token": token, "channel": CHANNEL_ID, "text": msg}
    requests.post("https://api.slack.com/api/chat.postMessage", params = params)
    print msg
    pass

def loadUsers(token):
    params = {"token": token, "channel": CHANNEL_ID, "oldest": slack_oldest}
    responseUser = requests.get("https://slack.com/api/users.list",params=params)
    users = json.loads(responseUser.text)["members"]
    return users

def findUser(userId, recurcive=True):
    global users
    if 'users' not in globals():
        users = loadUsers(USERTOKENSTRING)
    for user in users:
        if userId == user["id"]:
            return user["name"]
    if recursive:
        users = loadUsers(USERTOKENSTRING)
        return findUser(userId, False)
 
def getSlackHistory(token):
    global slack_oldest
    params = {"token": token, "channel": CHANNEL_ID, "oldest": slack_oldest, "inclusive": 0}
    response = requests.get("https://slack.com/api/channels.history",params=params)
#    print "oldest: %s" %(slack_oldest)

    messages = json.loads(response.text.decode('utf-8'), encoding = 'utf-8')["messages"]
    msgCount = len(messages)
    for message in reversed(messages):
        if "username" in message:
            userName = message["username"]
        else:
            userName = findUser(message["user"])

        msg = "[slack] (%s): %s" %(userName, message["text"])
        if not "bot" in userName:
            print msg.encode('utf-8')
            sendSkypeMsg(msg)

        if float(slack_oldest) <= float(message["ts"]):
            slack_oldest = str(message["ts"])
            writeSettings()
    return msgCount

def smartDelay(msgCount, currentDelay):
    maxDelay = 5.0
    if msgCount != 0:
        return 1.0
    elif currentDelay < maxDelay:
        return currentDelay+0.1
    else:
        return maxDelay

skype = Skype4Py.Skype(); 
skype.OnMessageStatus = onSkypeMsg
skype.Attach();

while True:

    time.sleep(delay)
    try:
        msgCount = getSlackHistory(USERTOKENSTRING)
        delay = smartDelay(msgCount, delay)
    except:
       pass
#    print "delay: %s" %(delay)
