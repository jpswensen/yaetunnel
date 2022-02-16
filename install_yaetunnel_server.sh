#!/bin/bash

# TODO: Maybe i the future we should have this step create a user just for this server?
USER=$1
GROUP=$2

if [ `id -u` = 0 ] ; then
    echo "Creating a folder in /var/lib/yaetunnel and giving ownership to $USER:$GROUP"
    mkdir -p /var/lib/yaetunnel
    chown -R $USER:$GROUP /var/lib/yaetunnel

    echo "Attempting to build yaetunnel server using pyinstaller"
    python3 -m PyInstaller -F yaetunnel-server

    echo "Installing yaetunnel binary"
    install -C -o $USER -g $GROUP -m 751 dist/yaetunnel-server /usr/local/bin

    rm -rf dist
    rm -rf build

    # Update the sshd server to require the ClientAlive* messages to keep data going over the tunnel even
    # when there isn't an active connection
    sed -i 's/#ClientAliveInterval.*/ClientAliveInterval 15/' /etc/ssh/sshd_config
    sed -i 's/#ClientAliveCountMax.*/ClientAliveCountMax 4/' /etc/ssh/sshd_config
    
else
    echo "You need to run as root to create folders and change permission in /var/lib/yaetunnel"
fi

exit
