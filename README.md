THIS PROJECT HAS BEEN ADJUSTED TO RUN WITH GPIOZERO 2.0.1 his resulted when reviewing its operation on a Pi under RaspberryPI OS Bookworm with latest Scratch3 release 3.30.9 with which it now works.
This project uses a python script to act as an OSC server and client to enable messages to be sent from Sonic PI to control the GPIO pins on a Raspberry Pi4 (or 3B+) computer running the latest Raspbian. The script can also detect the state of designated pins on the GPIO of the Pi and send information back to Sonic PI. Scratch3 running on the PI has an extension which enables it to interact with GPIO pins. By this means control can be established between Scratch and Sonic Pi. Options exist for Sonic Pi to run on the same Pi as Scratch3, or on a different computer running on the same local network.

Sonic PI 3.2.2 or later is required on the PI as the Sonic PI 3.1 supplied with Raspbian is not a full version and doesn't support OSC messaging. You can download a binary deb for Sonic PI 3.3.1 from https://sonic-pi.net/files/releases/v3.3.1/sonic-pi_3.3.1_1_armhf.deb (or the earlier Sonic PI 3.2.2 on Raspbian from http://r.newman.ch/rpi/sonic-pi-3.2.2 )

An article on the project is available at https://rbnrpi.wordpress.com/controlling-sonic-pi-from-scratch-3-on-a-raspberry-pi4/

A video of the project in action is available at https://youtu.be/sIDeQ9Hq74M
Three files comprise the project
SonicPiAndScratch.sb3 which is the scratch3 file.
scratchclickbuttons.rb which is a Sonic Pi file that should be downlaoded and opened in a Sonic PI buffer.
osc-ScratchandSP.py which is an executable script which runs on the Pi hosting Scratch3.
