# yaetunnel
Yet Another Easy Tunnel (YAETunnel)

--- 

## History
I developed this because a deep frustration with having to pay a company A LOT of money to just make a secure tunnel between two device. I had been doing a bunch of consulting, where I had a setup that looked like the following:

MY LAPTOP <---vnc---> VNC BROKER <---vnc---> Raspberry Pi IOT device

This service is flawless, has a nice interface, is easy to set up, is easy to share with colleagues, etc. The problem is that it costs an arm and a leg. Even in bulk at 25 devices, their price is about $24 per device per year. At smaller counts the price is about $40 per device per year.

So, I set out to create my own. I figured the simplest way to try and make this as secure as possible was to force everything to go through SSH. In this manner, the solution would be as secure as the system administrator was competent to make it so. 

**!!!DISCLAIMER: I am NOT a network security expert!!! PLEASE consult with your own network security team before using this solution to make sure they allow this use case in their own security policies.** If there are ways that this is considered insecure, please let me know, as I would be interested to know. It seems to be at least as secure as the method of the VNC broker, but maybe I am wrong.

---

## Architecture

This service is composed of three parts, and I will describe them in some level of detail. One of the key aspects of this is that the USER client and the DESTINATION client both interact with the SERVER over SSH. They quite literally execute a program running on the SERVER over SSH and then interpret the results.

![USER ---forward SSH tunnel---> SERVER <---reverse SSH tunnel--- DESTINATION](/3DTest.png)



### SERVER
This piece is comprised of a single executable called yaetunnel-server. The service creates a local sqlite3 database to store information about the registered devices, the tunnel port, the destination port, and the connectivity status. It accepts one of three possible commands {add, delete, query}.

The **add** command requires the the user specify a name, uuid, and the port on the destination that is being added. When this command is executed, it will add the name, uuid, and destination port to the database, as well as generate the next available tunnel port number in the range of >20000. 

The **delete** command allows the DESTINATION client to be deleted from the table of registered devices.

The **query** command allows both the USER client and DESTINATION client to query the registered devices. For the DESTINATION client, this is so it knows whether to add/remove ports based on changes in the config file since the last time it was loaded. For the USER client, this is to make it easy to find out what tunnels are available and to initiate those connections. Whenever the query command is executed, it also checks the results of the 'netstat' command to see which registers DESTINATIONS and ports are connected.


### DESTINATION client
This piece is comprised of an executable called yaetunnel-client, a config file names yaetunnel.ini, and a systemd .service file to create the connection at startup and to manage it going up and down. I will discuss the config file entries later. This piece uses the program autossh to initiate the reverse tunnels and keep them open. autossh is an amazing tool.


### USER client
This piece is comprise of an executable called yaetunnel (I might need change this to make the names of this and the DESTINATION client less confusing). This accepts one of two possible commands: {list, connect}.

The **list** command queries the server and prints out a pretty table of the device names, available ports, and whether the device and port are conencted.

The **connect** command requires the user specify a destination name and port. If the port is 22, it is smart enough to now that you want to actually launch a ssh terminal. If it is any other port, it assumes that you are just using that port for other traffic (such as VNC in my case). There is also a --newterm option for port 22 that launches the ssh session in a new terminal window.

---

## Setup

1. Create an EC2 instance or other public-facing server with ssh capabilities. If you follow EC2 setup instructions, you end up with a .pem file that has the login credentials.
2. Download this package. Update the .ini file before you run any of the install scripts
3. Copy the package with the updated config file to all three machines: USER client, SERVER, and DESTINATION client
4. Using the .pem, log into the SERVER and run 'sudo -E ./install_yaetunnel_server.sh' This creates a folder '/var/lib/yaetunnel' for the database, builds the yaetunnel-server executable using PyInstaller, and copies it to /usr/local/bin
5. Using whatever means needed, log into the DESTINATION machine and run 'sudo -E ./install_yaetunnel_client.sh'. This creates a folder in '/etc/yaetunnel' and copies the config file yaetunnel.ini there. That is why it should be edited appropriately before this step. It also builds the yaetunnel-client executable  using PyInstaller, and copies it to /usr/local/bin. Finally, it copies the .service file to '/etc/systemd/system' and reloads the systemd daemon. This does not enable or start the service, but the script gives instructions on how to do so.
6. On the USER machine, run 'sudo -E ./install_yaetunnel_user.sh'. This creates a folder in '/etc/yaetunnel' and copies the config file in there. Really the only elements that are important for the config file on this machine are the server, SERVER username, PEM location, and the DESTINATION username. It builds the yaetunnel executable using PyInstaller, and copies it to /usr/local/bin.

_Example 1_
At this point, if you started the service on the DESTINATION device, you should be ready to go. You can try the commands of 
  yaetunnel list
to get a list of all the available devices

_Example 2_
You can create a connection by using the command of
  yaetunnel connect --name=devicename --port=22 --username=user
This one in particular will open the ssh connection and you will be prompted for the password for the destination user (I haven't experimented yet with whether you can get a key from that machine and it applies properly through the tunnel). It assumes that port 22 is trying to have an interactive session.

_Example 3_
You can create an ssh connection in a newly launched terminal by using the command of 
  yaetunnel connect --name=devicename --port=22 --username=user --newterm
NOTE: I only have this working on MacOS so far.

_Example 4_
You can create a persistent tunnel for any other port using the command of
  yaetunnel connect --name=devicename --port=5900 --username=user
This will block at the command line and keep the tunnel open until the process is killed. In this scenario, I can then go to my vncviewer software and access it through the tunneled port number (which you will need to find from the yaetunnel list command). 

**TODO: Just realizes I wasn't printing out the tunneled port number in the table from the list command. I need to fix that**



---

## TODO

1. I created some decent script to automate the process of installing. It relies in PyInstaller to make binaries of the three programs and install them to /usr/local/bin. The one thing that still is not fixed is that I have the username of the destiantion machine hard coded right now. Since I am testing on getting to my Rpi, this is 'pi'.
2. I really want to make a nice PyQT5 gui that can be run to simplify the process of getting connected.
3. I want to add the ability to create subgroups based on a team name or team identifier. An example of this is that I often want remote access to a machine in one of the teaching labs at my university to help students who are there late at night working on projects. However, I don't want to show that machine to my consulting clients and don't want my consulting clients to see each others' devices. I suppose the real solution is to spin up an EC2 instance for each customer (which is still probably about $5 per month for a t2.micro instance or about $2 per month for a t3.nano or t3a.nano instance). 




