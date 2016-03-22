#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import requests
import json
import threading


class Slack:
    def __init__(self, configFile, debug = False):
        self.configFile = configFile
        self.loadSettings()
        self._users = self._loadUsers()
        self._debug = debug
        self._maxDelay = 5.0
        self._minDelay = 1.0
        self._delay = 1.0
        thread = threading.Thread(target=self.main)
        thread.daemon = True
        thread.start()

    def loadSettings(self):
        with open(self.configFile) as f:
            self._settings = json.load(f)
            self._token = self._settings['USERTOKENSTRING']
            self._channelId = self._settings['CHANNEL_ID']
            self._oldest = self._settings['oldest']

    def saveSettings(self):
        self._settings['oldest'] = self._oldest
        with open(self.configFile, 'w') as f:
            json.dump(self._settings, f, indent=4, sort_keys=True)

    def memberList(self):
        userNames = []
        params = {"token": self._token, "channel": self._channelId}
        response = requests.post("https://api.slack.com/api/channels.info", params = params)
        members = json.loads(response.text.decode('utf-8'), encoding = 'utf-8')["channel"]["members"]
        for member in members:
            userName = self.findUser(member)
            userNames.append(userName)
        return "\n".join(userNames)

    def sendMsg(self, msg, target):
        params = {"token": self._token, "channel": target, "text": msg}
        print "send message on slack, channel: ", target
        print msg
        #requests.post("https://api.slack.com/api/chat.postMessage", params = params)

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
        if self._debug:
            print "get Hystory"
            print response.text.decode('utf-8')
        messages = json.loads(response.text.decode('utf-8'), encoding = 'utf-8')["messages"]
        msgCount = len(messages)
        for message in reversed(messages):
            if "username" in message:
                msg["sender"] = message["username"]
            else:
                if self._debug:
                    print "search name"
                msg["sender"] = self.findUser(message["user"])
            msg["text"] = message["text"]
            msg["source"] = self._channelId
            msg["messenger"] = "slack"
            if not "bot" in msg["sender"]:
                if self._debug:
                    print "calling onMsgReceive"
                self.onMsgReceive(msg)
#            elif self._debug:
#                print "bot in name. Msg from: %s" %(msg["sender"])
            if float(self._oldest) <= float(message["ts"]):
                self._oldest = str(message["ts"])
                self.saveSettings()
        return msgCount

    def smartDelay(self, msgCount):
        if msgCount != 0:
            self._delay = self._minDelay
        elif self._delay < self._maxDelay:
            self._delay += 0.1
        else:
            self._delay = self._maxDelay

    def onMsgReceive(self, msg):
        """
        function called on receive message
        """

    def main(self):
        while True:
            if self._debug:
                print "delay: %s" %(self._delay)
            time.sleep(self._delay)
            try:
                msgCount = self.getHistory()
                self.smartDelay(msgCount)
            except Exception as e:
               print(e)
               print("exception")
