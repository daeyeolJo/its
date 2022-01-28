# import lxml import etree as ET
import os, sys
import datetime
from jinja2 import Environment, FileSystemLoader
PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    fname = "test.xml"
    cpu_model = input("1 : westmere, 2 : host-passthrough")
    cpu_cache_mode = input("1 : disable, 2 : passthrough")

    param = {'cpu_model' : cpu_model, 'cpu_cache_mode' : cpu_cache_mode }

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    new_fname = "_".join([fname, suffix]) + ".xml" # e.g. 'mylogfile_120508_171442'

    file_loader = FileSystemLoader('libvirt-xml')
    env = Environment(loader=file_loader)
    template = env.get_template('gooroom.auto.xml')
    output_from_parsed_template = template.render(param=param)

    define_instruction = "virsh define" + new_fname
    os.system(define_instruction)


    with open(new_fname, 'w') as f:
        f.write(output_from_parsed_template)
