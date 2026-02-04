from netmiko import ConnectHandler
from getpass import getpass
import re
from jinja2 import Environment, FileSystemLoader

uname = input('Enter username: ')
pwd = getpass('Enter password: ')

# Read router list from external file
with open("rtr_list.txt") as f:
    rtr_lst = [line.strip() for line in f if line.strip()]

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

            # Load Jinja2 environment (looks for templates in current directory)
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template('bfd_int.j2')

            # Render template with data
            for intf in interfaces:
                output = template.render(intf=intf)

            # Export output to a text file
                with open("report.txt", "a") as file:
                    file.write(f' == {rtr} == \n')
                    file.write(output)
                    file.write("\n")

                    print(f"{rtr} report has been written to report.txt")
