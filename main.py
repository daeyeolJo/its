# import lxml import etree as ET
import os, sys
import datetime
from jinja2 import Environment, FileSystemLoader
PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    fname = "test.xml"

    os_option = input("1 : gooroom, 2 : window10\n")
    cpu_model = input("1 : westmere, 2 : host-passthrough\n")
    cpu_cache_mode = input("1 : disable, 2 : passthrough\n")

    param = {'cpu_model' : cpu_model, 'cpu_cache_mode' : cpu_cache_mode }

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    new_fname = "_".join([fname, suffix]) + ".xml" # e.g. 'mylogfile_120508_171442'

    file_loader = FileSystemLoader('libvirt-xml')
    env = Environment(loader=file_loader)
    if os_option == '1':
        template = env.get_template('gooroom.auto.xml')
        start_instruction = "virsh start gooroom"
        shutdown_instruction = "virsh shutdown gooroom"
    else:
        template = env.get_template('win10.auto.xml')
        start_instruction = "virsh start win10"
        shutdown_instruction = "virsh shutdown win10"
    output_from_parsed_template = template.render(param=param)

    with open(new_fname, 'w') as f:
        f.write(output_from_parsed_template)

    define_instruction = "virsh define " + new_fname
    os.system(define_instruction)

    check_cpu_usage_instruction = "pidstat -G qemu-system-x86"
    os.system(check_cpu_usage_instruction)

    while(1):
        user_input = input("If you want to shutdown VM, click q or Q")
        if(user_input == 'q' or 'Q'):
            os.system(shutdown_instruction)
            break

