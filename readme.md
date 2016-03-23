Messenger synchronizer
===


TODO
---
* bot interface 
* use sqlite for storing settings
* advanced commands on chat
* python virtualenv
* x64 skype?

***

Install
---

```bash
apt-get install python-pip git python-dbus python-gobject dbus dbus-x11
pip install Skype4Py
```
[Install Skype for linux](http://www.skype.com/ru/download-skype/skype-for-computer/)
```bash
wget http://download.skype.com/linux/skype-debian_4.3.0.37-1_i386.deb
sudo dpkg --add-architecture i386
sudo apt-get update
sudo dpkg -i skype-debian_4.3.0.37-1_i386.deb
sudo apt-get install -f
```
rename `config.json.example` to `config.json`

Rename `slack.json.example` to `slack.json`


On headless box you may need before to install `xvbf fluxbox` packages. And some vnc client

```bash
apt-get install xvfb fluxbox x11vnc
```
After `start-headless.sh` script may be used.

get chat id's
---

* Skype:
send `/get name` on chat

* Slack:

  * [Get you token] (https://api.slack.com/docs/oauth-test-tokens)
  * [Get channel list](https://slack.com/api/channels.list?pretty=1&token=xoxp-xxxx "Add you token to url")

***

Limitation
---
* Skype:

  * only old-style chat rooms supported. To create such chat just send to any chat `/createmoderatedchat` on new version of skype.
* Slack:

  * currently only one channel served.




