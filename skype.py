#!/usr/bin/python
# -*- coding: utf-8 -*-

import Skype4Py

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = " %(attr)

class Skype(Skype4Py.Skype):
    def OnMessageStatus(self, Message, Status):
        msg = dict()
        if Status == 'RECEIVED':
            if Message.Sender.FullName == "":
                msg["sender"] = Message.Sender.Handle
            else:
                msg["sender"] = Message.Sender.FullName
            msg["text"] = Message.Body
            msg["messenger"] = "skype"
            msg["chat"] = Message.Chat.Name
            msgTxt = "[skype] (%s): %s" % (Name, Message.Body)
            print msg
            self.onMsgReceive(msg)
#            if SkypeChatId in Message.Chat.Name:
#                sendSlackMsg(msg)
    #commands
    def sendMsg(self, msg):
        for chat in skype.Chats:
            if SkypeChatId in chat.Name:
                chat.SendMessage(msg)
                print chat.Name 
    def onMsgReceive(self,msg):
        pass



