#!/usr/bin/python
# -*- coding: utf-8 -*-

#import Skype4Py
import time
import requests

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = " %(attr)

# Set your config variables from the config.json file
class Skype:
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



