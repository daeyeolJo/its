import os, sys
import datetime
from jinja2 import Environment, FileSystemLoader
PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    fname = "gooroom"
    os_option = input("1 : gooroom, 2 : window10\n")
    cpu_model = input("1 : host-passthrough, 2 : westmere\n")
    cpu_cache_mode = input("1 : passthrough, 2 : disable\n")
    disk_aio_mode = input("1 : threads, 2 : native, 3 : queue\n")
    video_model = input("1 : vga, 2 : cirrus\n")
    param = {'cpu_model' : cpu_model, 'cpu_cache_mode' : cpu_cache_mode, 'disk_aio_mode': disk_aio_mode, 'video_model' : video_model}

    suffix = datetime.datetime.now().strftime("%y%m%d_%S")
    new_fname = "_".join([fname, suffix]) # e.g. 'mylogfile_120508_171442'
    new_fname += ("_" + cpu_model + cpu_cache_mode + disk_aio_mode + video_model +".xml")
    file_loader = FileSystemLoader('libvirt-xml')
    env = Environment(loader=file_loader)
    if os_option == '1':
        template = env.get_template('ubuntu.xml')
        start_instruction = "virsh start udesktop20_04-03"
        shutdown_instruction = "virsh shutdown udesktop20_04-03"
    else:
        template = env.get_template('win10.auto.xml')
        start_instruction = "virsh start win10"
        shutdown_instruction = "virsh shutdown win10"
    output_from_parsed_template = template.render(param=param)

    with open(new_fname, 'w') as f:
        f.write(output_from_parsed_template)

    define_instruction = "virsh define " + new_fname
    os.system(define_instruction)
    os.system(start_instruction)

    check_cpu_usage_instruction = "pidstat -G qemu-kvm"
    os.system(check_cpu_usage_instruction)

    while(1):
        user_input = input("If you want to shutdown VM, click q or Q")
        if(user_input == 'q' or 'Q'):
            os.system(shutdown_instruction)
            break
