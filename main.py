# UserFilesBackup allows you to backup the users' files from remote nodes
# Tested on Linux (Debian == homedir) and Microsoft OS (Windows 10 == "Documents" folder)
# Version 1.0

# Modules required
import platform
import socket
import subprocess
import paramiko
import time
import os


# Function net_scan declaration - list all available nodes within a user given IP range
def net_scan():
    # Obtaining the network IP which will be checked
    input_ip = input("Enter the network IP you wish to check: ")
    start_ip = input("Enter the starting digit to check for this network: ")
    last_ip = input("Enter the last digit to check for this network: ")

    # Reformatting the network for easier use
    ip_split = input_ip.split('.')
    ips_to_scan = ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + '.'

    # Initiating the ping command depending on the system from which the script is launched
    if os_platform == "Windows":
        os_ping = "ping -n 1 -w 250 "
    else:
        os_ping = "ping -c 1 -w 250 "

    # Lets get those online nodes & store them in the dictionary !
    for last_member in range(int(start_ip), int(last_ip)+1):
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

            # Adding this online node to the dictionary
            online_nodes.update({host_name[0]: current_ip})

    # Ensuring we've got some nodes online before launching the menu
    if bool(online_nodes) is False:
        print("No IP response obtained: either all nodes are currently offline or unreachable.")
        print("Exiting the program...")
        exit()


# Function remote_backup declaration - connect to the node, compress the user's folder and transfer it
def remote_backup(ip_to_backup):
    # Variables declaration
    ssh_user = ""
    ssh_password = ""

    # Looping on username input and providing an escape
    while ssh_user == "":
        ssh_user = input("Enter the SSH login for {} (x to exit): ".format(ip_to_backup))
        if ssh_user == "x":
            exit()

    # Looping on password input, providing an escape
    # For additional security this input should be changed to masked characters
    while ssh_password == "":
        ssh_password = input("Enter the password for {} (x to exit): ".format(ssh_user))
        if ssh_password == "x":
            exit()

    # SSH's try block using paramiko module
    try:
        # Creating a new SSHClient
        ssh_client = paramiko.SSHClient()
        # Setting paramiko to allow connection to unknown nodes
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connecting to the node using the provided credentials
        ssh_client.connect(hostname=ip_to_backup,
                           username=ssh_user,
                           password=ssh_password)
        # Passing "ver" command on the distant node to check if it's running Windows or another system
        stdin, stdout, stderr = ssh_client.exec_command("ver")
        out = stdout.read().decode().strip()

        # Formatting the archive's name
        archive_name = time.strftime("%Y%m%d@%Hh%Mm%Ss") + '-' + ip_to_backup + '-' + ssh_user

        # Target is a Windows node
        if 'Windows' in out:
            # Initiating the variables for a Windows node
            delete_cmd = "del "
            filepath = "C:\\Users\\" + ssh_user + "\\Documents\\"
            archive_with_ext = archive_name + ".zip"

            # Prepare and send the command to compress the user's "Documents" folder
            compress_cmd = "powershell Compress-Archive " + filepath + ' ' + filepath + archive_with_ext
            stdin, stdout, stderr = ssh_client.exec_command(compress_cmd)

        # For all other OS
        else:
            # Initiating the variables for other OSes
            delete_cmd = "rm "
            filepath = "/home/" + ssh_user + "/"
            archive_with_ext = archive_name + ".tar.gz"

            # Prepare and send the command to compress the user's home directory
            compress_cmd = "tar -zcvf " + filepath + archive_with_ext + ' ' + filepath
            stdin, stdout, stderr = ssh_client.exec_command(compress_cmd)

        # Waiting on the compress command to be over and checking its result
        exit_compress = stdout.channel.recv_exit_status()
        if exit_compress != 0:
            print("Error while compressing the user's folder", exit_compress)
        else:
            # Initiating a file transfer method (sftp) through the Paramiko ssh's instance
            file_transfer = ssh_client.open_sftp()

            # Generating the local backup folder depending on the OS
            if os_platform == "Windows":
                local_path = "C:\\Backup\\"
            else:
                local_path = "/home/" + os.getlogin() + "/backup/"

            # Making sure this folder exists, if not create it
            if not os.path.exists(local_path):
                os.makedirs(local_path)

            # Importing the archive from the distant node
            file_transfer.get(filepath + archive_with_ext, local_path + archive_with_ext)

            print()
            print("Archive successfully retrieved and stored at: {}".format(local_path + archive_with_ext))

            # Cleaning the archive from the distant node
            stdin, stdout, stderr = ssh_client.exec_command(delete_cmd + filepath + archive_with_ext)
            print("Cleanup on remote node: {} deleted".format(delete_cmd + filepath + archive_with_ext))

            # Cleaning the existing connections
            if file_transfer:
                file_transfer.close()
            if ssh_client:
                ssh_client.close()

    # Except block in case the SSH isn't responding
    except paramiko.ssh_exception.NoValidConnectionsError as error:
        print(error)
        pass
    # Except block on authentication issues (wrong user and/or password)
    except paramiko.ssh_exception.AuthenticationException as error:
        print(error)
        pass


# Function main_menu - using net_scan's output, display the list of available nodes and launch the backup
def main_menu():
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
        print()
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
        remote_backup(user_answer)


# Main program
# Initiating the dictionary that will be used for the program
os_platform = platform.system()
online_nodes = {}

# Invoke net_scan function
net_scan()

# Invoke main_menu function
main_menu()
