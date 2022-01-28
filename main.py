# import lxml import etree as ET
import os
import datetime
from jinja2 import Environment, FileSystemLoader
PATH = os.path.dirname(os.path.abspath(__file__))

# def load_xml(name):
#     ''' Takes an xml file as input. Outputs ElementTree and element'''
#     # specify parser setting
#     parser = ET.XMLParser(strip_cdata=False)
#     # pass parser to do the actual parsing
#     tree = ET.parse(name, parser)
#
#     root = tree.getroot()
#     return tree, root

# def render_template(template_filename, context):
#     return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
if __name__ == '__main__':
    fname = "test.xml"
    cpu_model = input("1 : westmere, 2 : host-passthrough")
    cpu_cache_mode = input("1 : disable, 2 : passthrough")


    cpu_model = '\'' + cpu_model + '\''

    param = {'cpu_model' : cpu_model}

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    new_fname = "_".join([fname, suffix]) # e.g. 'mylogfile_120508_171442'

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('test.xml')
    output_from_parsed_template = template.render(param=param)

    with open(new_fname, 'w') as f:
        f.write(output_from_parsed_template)



