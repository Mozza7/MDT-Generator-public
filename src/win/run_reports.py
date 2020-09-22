import subprocess
import os

customers_folder = os.path.abspath(os.path.join(os.getcwd(), 'Customers'))
os.chdir(customers_folder)

for dirs in os.listdir(customers_folder):
    os.chdir(dirs)
    subprocess.call([r'autorun.bat'])
    os.chdir(customers_folder)
