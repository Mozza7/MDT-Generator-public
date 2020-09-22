import os
from shutil import copy2

os.chdir('..')

customers_folder = os.path.abspath(os.path.join(os.getcwd(), 'Customers'))
main_py = os.path.abspath(os.path.join(os.getcwd(), 'src_files\\main_.py'))
os.chdir(customers_folder)

for dirs in os.listdir(customers_folder):
    copy2(main_py, f'{dirs}\\main_.py')
# use this to update main_.py when changed in src_files (instead of remaking each customer)
