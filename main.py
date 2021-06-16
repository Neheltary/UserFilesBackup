# UserFilesBackup allows you to backup the users' files from remote nodes
# Tested on Linux (Debian == homedir) and Microsoft OS (Windows 10 == "Documents" folder)
# Version 0.1

# Modules required
import platform
import socket
import subprocess
import paramiko
import time
import os

# Function netscan declaration - list all available nodes within a user given IP range
def netscan():
    # To be done -----

# Function remotebackup declaration - connect to the node, zip f
def remotebackup():
    # To be done -----

# Function nodeselection - using netscan's output, display the list of available nodes and launch the backup
def nodeselection():
    # To be done -----

# Main program
# Invoke netscan function
netscan()

# Invoke nodeselection fuction
nodeselection()