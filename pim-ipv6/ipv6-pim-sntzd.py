from netmiko import ConnectHandler
from getpass import getpass
import os
import subprocess
#os.chdir('/root/gee_python_exercises')
import re

uname = input("username: ")
pwd = getpass("password: ")

config_items = ['10.68.32.122', '10.68.32.123']


for ci in config_items:

    print(f'===={ci}=====')
    cisco_dev = {'device_type': 'cisco_xr', 'host': ci, 'username': uname, 'password': pwd}
    netm_login = ConnectHandler(**cisco_dev)
    show_run_outp = netm_login.send_command('show run')

    pairs = []
    last_interface = None

    for line in show_run_outp.splitlines():
        if re.search(r'\binterface\b', line):
            # Update the most recent interface line
            last_interface = line.strip()
        if re.search(r'\bipv6 pim bfd\b', line):
            # Record the pair (interface, bfd line)
            if last_interface:
                pairs.append((last_interface, line.strip()))

    # Print all interface–bfd pairs
    for iface, bfd_line in pairs:
        print(f"\n{iface}" + "\n   no ipv6 pim bfd" +"\n   ipv6 nd cache expire 120 refresh\n\n")