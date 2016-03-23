#!/usr/bin/python
# -*- coding: utf-8 -*-

import Skype4Py

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = " %(attr)

class Skype(object):
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
            msg["source"] = Message.Chat.Name
            self.onMsgReceive(msg)
    #commands
    def sendMsg(self, msg, target):
        for chat in skype.Chats:
            if target == chat.Name:
                print chat.Name
                chat.SendMessage(msg)

    def onMsgReceive(self,msg):
        msgTxt = "[skype] (%s): %s" % (msg["sender"], msg["text"])
        print msgTxt
        pass



