#!/bin/bash

# Need to run with sudo -E for it to find the python interpreter and pip packages correctly
#    sudo -E ./install_yateunnel_client.sh pi pi
# Of course, you will need to change the name user and group so that the config file can be read

# TODO: Maybe i the future we should have this step create a user just for this server?
USER=$1
GROUP=$2

if [ `id -u` = 0 ] ; then
    echo "Creating a folder in /etc/yaetunnel and giving ownership to $USER:$GROUP"
    mkdir -p ~/.yaetunnel
    cp yaetunnel_user.ini ~/.yaetunnel/yaetunnel_user.ini
    chown -R $1:$2 ~/.yaetunnel
    
    echo "Attempting to build yaetunnel user using pyinstaller"
    # I have to weirdly use the system python instead of my custom 3.8 beacuse I forgot to build with shared libraries 
    /usr/local/bin/python3 -m PyInstaller -F yaetunnel

    echo "Installing yaetunnel binary"
    install -C -o $USER -g $GROUP -m 751 dist/yaetunnel /usr/local/bin

    #rm -rf dist
    #rm -rf build
    
else
    echo "You need to run as root to create folders and change permission in /var/lib/yaetunnel"
fi

exit
