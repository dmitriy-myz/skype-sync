#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import requests
import json
import threading


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
    def smartDelay(self, msgCount):
        if msgCount != 0:
            self._delay = self._minDelay
        elif self._delay < self._maxDelay:
            self._delay += 0.1
        else:
            self._delay = self._maxDelay
    def main(self):
        while True:
            time.sleep(self._delay)
            try:
                msgCount = self.getHistory()
                self.smartDelay(msgCount)
            except Exception as e:
               print(e)
               print("exception")

