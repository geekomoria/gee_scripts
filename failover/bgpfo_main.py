from jinja2 import Environment, FileSystemLoader
import sys

# Ensure exactly 2 arguments are provided (script name + 2 values)
if len(sys.argv) != 3:
    print("Error: Exactly 2 arguments required. Usage: python3 script.py <BGPAS> <BGPNEI>")
    sys.exit(1)
    
# Load Jinja2 environment (looks for templates in current directory)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('bgpfo.j2')

#render interface input
try:
    BGPAS = sys.argv[1]
    BGPNEI = sys.argv[2]
except IndexError:
    print("Error: Missing arguments. Usage: python3 script.py <BGPAS> <BGPNEI>")
    sys.exit(1)

output = template.render(BGPAS=BGPAS, BGPNEI=BGPNEI)

#print output
print(output)