import os
import shutil
from configparser import ConfigParser
import time
import sys

rootloc = os.getcwd()
config_loc = os.path.abspath(os.path.join(rootloc, 'src_files\\config.ini'))
cust_files = os.path.abspath(os.path.join(rootloc, 'Customers'))
src_files = os.path.abspath(os.path.join(rootloc, 'src_files'))

config = ConfigParser()
config.read('config.ini')

os.chdir(cust_files)

uname = config.get('login', 'uname')
pword = config.get('login', 'pword')
url = config.get('login', 'url')
from_e = config.get('email', 'from')
to_e = config.get('email', 'to')
smtp_addr = config.get('email_server', 'smtp_server_addr')
smtp_port = config.get('email_server', 'smtp_server_port')
tls_on = config.get('email_server', 'tls')
smtp_pword = config.get('email_server', 'smtp_pword')
cust_loc = config.get('file_locations', 'custom_location')
error_output = config.get('file_locations', 'error_output')
headless = config.get('selenium', 'headless_mode')
owner_name = config.get('navigation', 'owner_name')
main_active = config.get('navigation', 'main_active')

customer_name = input('Please enter customer name as is on portal: ')
cust_abbr = input('Please enter abbreviation for customer: ')
try:
    subgroupa = int(input('Type 1 to enable subgroup 1 (leave blank to disable): '))
except ValueError:
    subgroupa = 0
try:
    subgroupb = int(input('Type 1 to enable subgroup 2 (leave blank to disable): '))
except ValueError:
    subgroupb = 0
try:
    subgroupc = int(input('Type 1 to enable subgroup 3 (leave blank to disable): '))
except ValueError:
    subgroupc = 0
if subgroupa == 1:
    cust_subgroupa = input('Enter name of subgroup 1: ')
if subgroupb == 1:
    cust_subgroupb = input('Enter name of subgroup 2: ')
if subgroupc == 1:
    cust_subgroupc = input('Enter name of subgroup 3: ')
if os.path.isdir('Customers'):
    pass
else:
    os.mkdir('Customers')


def create_config():
    with open(config_loc, 'w+') as f:
        f.write(f'[login]\nuname = {uname}\npword = {pword}\nurl = {url}\n')  # Enter login information
        f.write(f'\n[email]\nfrom = {from_e}\nto = {to_e}\n')  # Enter email info
        f.write(f'\n[email_server]\nsmtp_server_addr = {smtp_addr}\nsmtp_server_port = {smtp_port}\ntls = {tls_on}\n'
                f'smtp_pword = {smtp_pword}\n')  # Enter email server info
        f.write(f'\n[file_locations]\ncustom_location = {cust_loc}\nerror_output = {error_output}\n')  # Files location
        f.write(f'\n[selenium]\nheadless_mode = {headless}\n')  # Sets selenium headless on/off
        f.write(f'\n[navigation]\nowner_name = {owner_name}\ncustomer_name = {customer_name}\n'
                f'main_active = {main_active}\ncust_abbr = {cust_abbr}\nsubgroupa = {subgroupa}\nsubgroupb = '
                f'{subgroupb}\nsubgroupc = {subgroupc}\n')  # Variables used to run the reports
        if subgroupa == 1:
            f.write(f'cust_subgroupa = {cust_subgroupa}\n')
        else:
            f.write(f'cust_subgroupa = \n')
        if subgroupb == 1:
            f.write(f'cust_subgroupb = {cust_subgroupb}\n')
        else:
            f.write(f'cust_subgroupb = \n')
        if subgroupc == 1:
            f.write(f'cust_subgroupc = {cust_subgroupc}\n')
        else:
            f.write(f'cust_subgroupc = \n')


def copy_program(symlinks=False, ignore=None):
    if not os.path.isdir(cust_abbr):
        os.mkdir(cust_abbr)
    elif os.path.isdir(cust_abbr):
        shutil.rmtree(cust_abbr)
        try:
            os.mkdir(cust_abbr)
        except PermissionError:
            timeout_set = 0
            while True:
                if timeout_set <= 30:
                    if not os.path.isdir(cust_abbr):
                        time.sleep(2.5)
                        timeout_set += 1
                        try:
                            os.mkdir(cust_abbr)
                        except FileExistsError:
                            break
                    else:
                        break
                else:
                    print(f'Removing existing files timed out for {cust_abbr}. Exiting')
                    sys.exit()
    for item in os.listdir(src_files):
        s = os.path.join(src_files, item)
        d = os.path.join(f'{rootloc}\\Customers\\{cust_abbr}\\', item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
    time.sleep(1)
    for item in os.listdir(src_files):
        s = os.path.join(src_files, item)
        d = os.path.join(f'{rootloc}\\Customers\\{cust_abbr}\\', item)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
        except FileExistsError:
            pass


def make_batch_launcher():
    venv_loc = config.get('path_to_venv', 'venv')
    cust_main_pyloc = os.path.abspath(os.path.join(rootloc, f'Customers\\{cust_abbr}\\'))
    os.chdir(cust_abbr)
    with open('autorun.bat', 'w+') as f:
        f.write('@echo off\n')
        f.write(f'cmd /k "cd /d {venv_loc} & activate.bat & cd /d {cust_main_pyloc} & python main_.py"')
    os.chdir(rootloc)


if __name__ == '__main__':
    create_config()
    copy_program()
    make_batch_launcher()
