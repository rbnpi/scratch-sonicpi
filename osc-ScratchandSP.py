#!/usr/bin/env python3
#SPoschandler.py written by Robin Newman, May 2020
#updated April 2024 to allow for a bug correction in gpiozero
#when this was writtem gpiozero did not respond to buttonboard.when_released events properly
#instead a button_pressed event was generated when a button was released
# the pr function used flags to accommodate this.
# the simplest fix now that it works properly in current gpiozero is to add the line

#Provides the "glue" to enable the GPIO on Raspberry Pi
#to communicate with Sonic Pi. Sonic Pi can control LEDs etc,and receive
#input from devices like push buttons connected to GPIO pins
#Sonic Pi can be running either on the Raspberry Pi,
#or on an external networked computer

#The program requires gpiozero (already in Raspbian) and python-osc to be installed


from gpiozero import ButtonBoard,LED,Button
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from time import sleep
import argparse
import sys


bn=20 #number of "buttons" in ButtonBoard
b=ButtonBoard(1,2,4,5,6,7,8,9,10,11,12,13,16,19,20,21,22,23,24,25)
reset = Button(27) #dealt with separately from ButtonBoard
flag=False #used in def pr to separate on/off messages
activate=False #used to activate sender once it is declared in __init__
current=0 #used to hold current activated button

def pr():
  global flag,current
  if activate: #make sure sender has been defined and is active
    if flag==False:
      for i in range(0,bn): #find which pin triggerd on
        if b.value[i]>0:
            print(i,b.value[i])
            sender.send_message('/playOn',i) #send OSC message for on
            flag=True #switch to looking for "off"
            current=i #current 'on' pin
    else:
      flag=False #looking for switch off
      print(current,b.value[current])
      sender.send_message('/playOff',current)

#both the next two lines trigger the pr function. Which is responsible is dealt with in the function logic
b.when_pressed = pr #trigger change of state event handled by function pr
b.when_released = pr #trigger change of state event handled by function pr
def doReset(): #deals with reset button pushed (pin 27)
    global activate 
    print("reset",reset.value)
    if activate==True: #only proceed if sender is activated
        sender.send_message('/reset',1) #send reset OSC to Sonic PI


reset.when_pressed=doReset #triggers doReset when button is pressed

l1 = LED(26) #this pin state controlled by input OSC from Sonic Pi


   
 #This is activated when /start OSC message is received by the server.
 #single argument is 1 or 0
def start(unused_addr,args, n):
    print("Start",n)
    if n==1:
        print("l1 on")
        l1.on() #set GPIO pin 26
    if n==0:
        print("l1 off")
        l1.off() #reset GPIO pin 26
        
#The main routine called when the program starts up follows
if __name__ == "__main__":
    try: #use try...except to handle possible errors
        #first set up and deal with input args when program starts
        parser = argparse.ArgumentParser()
        #This arg gets the server IP address to use. 127.0.0.1 or
        #The local IP address of the PI, required when using external Sonic Pi
        parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
        #This is the port on which the server listens. Usually 8000 is OK
        #but you can specify a different one
        parser.add_argument("--port",
              type=int, default=8000, help="The port to listen on")
        #This is the IP address of the machine running Sonic Pi if remote
        #or you can omit if using Sonic Pi on the local Pi.
        parser.add_argument("--sp",
              default="127.0.0.1", help="The ip Sonic Pi is on")
        args = parser.parse_args()
        if args.ip=="127.0.0.1" and args.sp !="127.0.0.1":
            #You must specify the local IP address of the Pi if trying to use
            #the program with a remote Sonic Pi aon an external computer
            raise AttributeError("--ip arg must specify actual local machine ip if using remote SP, not 127.0.0.1")
        #Provide feed back to the user on the setup being used    
        if args.sp == "127.0.0.1":
            spip=args.ip
            print("local machine used for SP",spip)  
        else:
            spip=args.sp
            print("remote_host for SP is",args.sp)
        #setup a sender udp-client to send out OSC messages to Sonic Pi
        #Sonic Pi listens on port 4560 for incoming OSC messages
        sender=udp_client.SimpleUDPClient(spip,4560) #sender set up for specified IP
        activate=True #signal that sender is now defined, to functions above
 
        #dispatcher reacts to incoming OSC messages and then allocates
        #different handler routines to deal with them
        dispatcher = dispatcher.Dispatcher()
        #The following handler responds to the OSC message /testprint
        #and prints it plus any arguments (data) sent with the message
        dispatcher.map("/testprint",print)
 
        #following dispatcher handles "/start" osc message
        dispatcher.map("/start",start,"n")

        #Now set up and run the OSC server
        server = osc_server.ThreadingOSCUDPServer(
              (args.ip, args.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        #run the server "forever" (till stopped by pressing ctrl-C)
        server.serve_forever()
    #deal with some error events
    except KeyboardInterrupt:
        print("\nServer stopped") #stop program with ctrl+C
    #Used the AttributeError to specify problems with the local ip address
    except AttributeError as err:
        print(err.args[0])
    #handle errors generated by the server
    except OSError as err:
       print("OSC server error",err.args)
    #anything else falls through
