#!/usr/bin/python
#
# home_alarm.py
# Email sent if motion detected.
#
# Author : Dominic Kick
# Date   : 23/08/2014

# Import required Python libraries
import time
import RPi.GPIO as GPIO
import smtplib # for communicating with an email server
import email # Import the email modules we'll need
import email.mime.application
import sys
import os # get the PID (Process Identifier) to kill this script
#import commands # for CPU/GPU temperature

def alarm_pid():
    print os.getpid()

#def get_cpu_temp():
    #tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    #cpu_temp = tempFile.read()
    #tempFile.close()
    #return float(cpu_temp)/1000
    # Uncomment the next line if you want the temp in Fahrenheit
    #return float(1.8*cpu_temp)+32
 
# Uncomment below if GPU temp is needed
#def get_gpu_temp():
    #gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
    #return  float(gpu_temp)
    # Uncomment the next line if you want the temp in Fahrenheit
    # return float(1.8* gpu_temp)+32
    
dest_email = 'archangel2000@gmail.com'
orig_email = '808dogrescue@gmail.com'
pwd_email = 'P@$$W0Rd100'
	
def alert(message):
    """The main function for sending an email using gmail"""
    # Create a text/plain message
    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = message['subject']
    msg['From'] = orig_email
    msg['To'] = dest_email
    # The main body is just another attachment
    msgbody = email.mime.Text.MIMEText(message['body'])
    msg.attach(msgbody)
    # send via Gmail server
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(orig_email,pwd_email)
    s.sendmail(orig_email,[dest_email], msg.as_string())
    s.quit()

# Edit for your subject and message
message1 = dict(subject='Alarm Alert', body='Motion detected on the second floor!')
	
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_PIR = 23

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo

Current_State  = 0
Previous_State = 0


try:

  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0

  # Loop until users quits with CTRL-C
  while True :

    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)

    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      alert(message1)
      # Record previous state
      Previous_State=1
	  #	Wait a minute
      time.sleep(60)
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      Previous_State=0

# For CTRL+C
except KeyboardInterrupt:
  # Reset GPIO settings
  GPIO.cleanup()
