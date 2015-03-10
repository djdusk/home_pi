# home_pi
Goal:
Home security using PIR motion sensor and camera.
Receiving and sending IR signals.
Plant watering system.

Set script to run automatically at boot:
sudo nano /etc/rc.local

Add the line:
/home/pi/home_alarm/home_alarm.py &
above the "exit 0" line
^X to exit and save changes