#!/usr/bin/python
# -*- coding: utf-8 -*-

import Skype4Py

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = " %(attr)

class SkypeChannel(object, channels):
    def __init__(self):
        self.skype = Skype4Py.Skype(Events=self)
        self.skype.Attach()
    def MessageStatus(self, Message, Status):
        msg = dict()
        if Status == 'RECEIVED':
            Message.MarkAsSeen()
            if Message.Sender.FullName == "":
                msg["sender"] = Message.Sender.Handle
            else:
                msg["sender"] = Message.Sender.FullName
            msg["text"] = Message.Body
            msg["messenger"] = "skype"
            msg["chat"] = Message.Chat.Name
#            msgTxt = "[skype] (%s): %s" % (msg["sender"], Message.Body)
#            print msgTxt
            self.onMsgReceive(msg)
#            if SkypeChatId in Message.Chat.Name:
#                sendSlackMsg(msg)
    #commands
    def sendMsg(self, msg, channel):
        for chat in skype.Chats:
            if channel == chat.Name:
                chat.SendMessage(msg)
                print chat.Name 

    def onMsgReceive(self,msg):
        pass



