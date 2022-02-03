import os, sys, time, threading
import datetime
from jinja2 import Environment, FileSystemLoader
PATH = os.path.dirname(os.path.abspath(__file__))

def check_cpu_usage():
    while(1):
        check_cpu_usage_instruction = "pidstat -G qemu-system-x86"
        os.system(check_cpu_usage_instruction)
        time.sleep(5)

if __name__ == '__main__':
    fname = "gooroom"
    os_option = input("1 : gooroom, 2 : window10\n")
    cpu_model = input("1 : host-passthrough, 2 : westmere\n")
    cpu_cache_mode = input("1 : passthrough, 2 : disable\n")
    disk_aio_mode = input("1 : threads, 2 : native, 3 : queue\n")
    video_model = input("1 : vga, 2 : cirrus\n")
    param = {'cpu_model' : cpu_model, 'cpu_cache_mode' : cpu_cache_mode, 'disk_aio_mode': disk_aio_mode, 'video_model' : video_model}

    suffix = datetime.datetime.now().strftime("%y%m%d_%S")
    new_fname = "_".join([fname, suffix]) 
    new_fname += ("_" + cpu_model + cpu_cache_mode + disk_aio_mode + video_model +".xml")
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
    os.system(start_instruction)

    t = threading.Thread(target=check_cpu_usage)
    t.daemon = True
    t.start()

    while(1):
        user_input = input("If you want to shutdown VM, click q or Q")
        if (user_input == 'q' or 'Q'):
            os.system(shutdown_instruction)
            break
