# yaetunnel
Yet Another Easy Tunnel (YAETunnel)

I developed this because a deep frustration with having to pay a company A LOT of money to just make a secure tunnel between two device. I had been doing a bunch of consulting, where I had a setup that looked like the following:

MY LAPTOP <---vnc---> VNC BROKER <---vnc---> Raspberry Pi IOT device

This service is flawless, has a nice interface, is easy to set up, is easy to share with colleagues, etc. The problem is that it costs an arm and a leg. Even in bulk at 25 devices, their price is about $24 per device per year. At smaller counts the price is about $40 per device per year.

So, I set out to create my own. I figured the simplest way to try and make this as secure as possible was to force everything to go through SSH. In this manner, the solution would be as secure as the system administrator was competent to make it so. 
!!!DISCLAIMER: I am NOT a network security expert!!! If there are ways that this is considered insecure, please let me know, as I would be interested to know. It seems to be at least as secure as the method of the VNC broker, but maybe I am wrong.

= Architecture

This service is composed of three parts, and I will describe them in some level of detail. One of the key aspects of this is that the USER client and the DESTINATION client both interact with the SERVER over SSH. They quite literally execute a program running on the SERVER over SSH and then interpret the results.

USER ---forward SSH tunnel---> SERVER <---reverse SSH tunnel DESTINATION


SERVER: This piece is comprised of a single executable called yaetunnel-server. The service creates a local sqlite3 database to store information about the registered devices, the tunnel port, the destination port, and the connectivity status. It accepts one of three possible commands {add, delete, query}.

The add command requires the the user specify a name, uuid, and the port on the destination that is being added. When this command is executed, it will add the name, uuid, and destination port to the database, as well as generate the next available tunnel port number in the range of >20000. 

The delete command allows the DESTINATION client to be deleted from the table of registered devices.

The query command allows both the USER client and DESTINATION client to query the registered devices. For the DESTINATION client, this is so it knows whether to add/remove ports based on changes in the config file since the last time it was loaded. For the USER client, this is to make it easy to find out what tunnels are available and to initiate those connections. Whenever the query command is executed, it also checks the results of the 'netstat' command to see which registers DESTINATIONS and ports are connected.


DESTINATION client: This piece is comprised of an executable called yaetunnel-client, a config file names yaetunnel.ini, and a systemd .service file to create the connection at startup and to manage it going up and down. I will discuss the config file entries later. This piece uses the program autossh to initiate the reverse tunnels and keep them open. autossh is an amazing tool.



USER client: This piece is comprise of an executable called yaetunnel (I might need change this to make the names of this and the DESTINATION client less confusing). This accepts one of two possible commands: {list, connect}.

The list command queries the server and prints out a pretty table of the device names, available ports, and whether the device and port are conencted.

The connect command requires the user specify a destination name and port. If the port is 22, it is smart enough to now that you want to actually launch a ssh terminal. If it is any other port, it assumes that you are just using that port for other traffic (such as VNC in my case). There is also a --newterm option for port 22 that launches the ssh session in a new terminal window.





