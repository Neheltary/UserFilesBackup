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
    # Obtaining the network IP which will be checked
    input_ip = input("Enter the network IP you wish to check (/24 expected): ")

    # Reformatting the network for easier use
    ip_split = input_ip.split('.')
    ips_to_scan = ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + '.'
    last_member = int(ip_split[3]) + 1

    # Initiating the ping command depending on the system from which the script is launched
    if os_platform == "Windows":
        os_ping = "ping -n 1 "
    else:
        os_ping = "ping -c 1 "

    # Lets get those online nodes & store them in the dictionary !
    for loop_control in range(1, 254):
        # Setting the ping command
        current_ip = ips_to_scan + str(last_member)
        current_check = os_ping + current_ip

        # Storing the ping result
        result = subprocess.Popen(current_check, shell=True, stdout=subprocess.PIPE).communicate()[0]
        # Ensuring the result content will always be the same no matter what OS is running the script
        upper_result = str(result).upper()

        # For each available nodes: populating the dictionary with the found hostname & IP address
        # Using socket.gethostbyaddr() function which returns a tuple containing: the host name, the IP address
        # and the alias list for the IP address (if any) of the host
        if 'TTL=' in upper_result:
            # Catching possible error on socket.gethostbyaddr()
            try:
                host_name = socket.gethostbyaddr(current_ip)
            except socket.herror:
                host_name = ("Hostname unavailable",)

            # Adding this node to the dictionary
            online_nodes.update({host_name[0]: current_ip})

        # Preparing the next iteration
        last_member += 1

        # Control on the IP: ensure we're not trying to check xxx.xxx.xxx.256 and above
        if last_member == 256:
            ip_split[2] += 1
            last_member = 0
            ips_to_scan = ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + '.'

    # Ensuring we've got some nodes online before launching the menu
    if bool(online_nodes) is False:
        print("No IP response obtained: either all nodes are currently offline or unreachable.")
        print("Exiting the program...")
        exit()


# Function remotebackup declaration - connect to the node, zip f
def remotebackup(ip_to_backup):
    print("Ici, je dois implémenter la fonction de sauvegarde pour {}".format(ip_to_backup))
    # Unix node ?
    # Use tar cmd
    # Windows node ?
    # powershell Compress-Archive C:\Users\User\Documents\ C:\Users\User\test.zip


# Function mainmenu - using netscan's output, display the list of available nodes and launch the backup
def mainmenu():
    # Using the network scan result, printing the selection menu
    # Loop condition
    keep_showing = True

    # Setting some variables
    top = '=' * 50
    bottom = '-' * 50

    # Looping on the menu until the user asks to stop
    # >> if 'x' is entered ==> exit,
    # >> if a 'known' IP is entered ==> launch the backup function and back to the menu
    # >> if an 'unknown' IP is entered ==> the program loops on showing the menu
    while keep_showing:
        print(top)
        print("{: ^1}{: ^30}{: ^1}{: ^17}{: ^1}".format("|", "Hostname", "|", "IP", "|"))
        print(top)
        # loop on key and value from dictionary to print the table
        for host_name, ip in online_nodes.items():
            print("{: ^1}{: ^30}{: ^1}{: ^17}{: ^1}".format("|", host_name, "|", ip, "|"))
            print(bottom)

        # Asking the user which node he wants to backup
        user_answer = input("Enter the IP address on which you want to launch the backup (x to exit): ")

        # Ensuring the user's answer is a know item
        while user_answer not in online_nodes.values():
            if user_answer == 'x':
                print("As instructed, exiting the program now...")
                exit()
            else:
                user_answer = input("Given IP address not available, please refer to the table or enter 'x' to exit): ")

        # Start the backup function
        remotebackup(user_answer)


# Main program
# Initiating the dictionary that will be used for the program
os_platform = platform.system()
online_nodes = {}

# Invoke netscan function
netscan()

# Invoke nodeselection fuction
mainmenu()

