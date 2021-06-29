# 
![Python 3.9.5](https://img.shields.io/badge/python-3.9.5%2B-brightgreen)
![Paramiko 2.7.2](https://img.shields.io/badge/Paramiko-2.7.2-lightgrey)

# UserFilesBackup

This tool is saving user files as specified below:
- Windows nodes - "Documents" folder
- Unix nodes - homedir

Tested from Debian 11 to Debian 11 / Windows 10 & from Windows 10 to Debian 11 / Windows 10

# Version history
v1.0: a network scan is done in order to prompt the user about choosing a node to backup

# TO DO
**Security:**
- Hide the password inputs --> getpass module
- Ensure that the user's inputs are respecting the required format 
- Encrypt the saved data

**User experience & removing the network scan requirement:**
- Input an IP to backup directly from command line
- Propose to input an IP to backup from the menu before the network scan & user prompt

**Performance:**
- Decrease the network scan's time by multithreading it (or use an existing module: scapy ?)

# How to use
**Requirements:**
- **Paramiko** has to be installed on the node running the script
  ```
  pip install paramiko
  ```
- Windows 10 _remote_ nodes need to have the OpenSSH server installed & configured

Step 1: go to the script location & launch it
- Windows 
  ```
  python main.py
  ```
- Unix
  ```
  python3 main.py
  ```
 
 Step 2: Enter the network to be scanned as well as the IP range to check
 ![image](https://user-images.githubusercontent.com/67184779/123561954-e7025000-d7ab-11eb-9996-ab545fc1abf1.png)
 
 Step 3: Choose the node to remotely backup
 
 Step 4: Enter the username & password
![image](https://user-images.githubusercontent.com/67184779/123562182-4e6ccf80-d7ad-11eb-8f4f-f25fbd5820a3.png)
 
 Step 5: Repeat 3 & 4 until you're done (x to exit)!
