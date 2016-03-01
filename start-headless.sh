#!/bins/bash
XSERVERNUM=1
export DISPLAY=:$XSERVERNUM

Xvfb :$XSERVERNUM -screen 0 800x600x16&
fluxbox&
skype&

#install -d ~/.x11vnc
#x11vnc -storepasswd ~/.x11vnc/passwd
#x11vnc -display :$XSERVERNUM -bg -xkb -rfbauth ~/.x11vnc/passwd

cd skype-sync
python -u skype.py &>> out.log </dev/null &

