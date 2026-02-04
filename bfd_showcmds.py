from netmiko import ConnectHandler
from getpass import getpass
import re

uname = 'valet027'
pwd = getpass('Enter password: ')

rtr_lst = ['aandlr-attr0-gw.net.disney.com', 'eorcrp-1120lab1-gw.net.disney.com']

for rtr in rtr_lst:
    cisco_dev = {'device_type': 'cisco_ios', 'host': rtr, 'username': uname, 'password': pwd}
    netm_login = ConnectHandler(**cisco_dev)
    sh_bfdnei = netm_login.send_command('show bfd neighbor')

    # Extract the IPv6 block only
    ipv6_block = re.search(r'IPv6 Sessions.*?(?=IPv4 Sessions|$)', sh_bfdnei, re.S)
    if ipv6_block:
        ipv6_text = ipv6_block.group(0)
        # Capture interface values in Int column
        interfaces = re.findall(r'\b\w+\d+/\d+/\d+\b', ipv6_text)
        for intf in interfaces:
            print(rtr + ": " + intf)