import glob
import os
import time
from configparser import ConfigParser
from datetime import datetime

cur_date = datetime.today().strftime('%d%m%Y')


def create_summary():
    os.chdir(log_files)
    with open('blank.log', 'w+') as f:
        f.writelines('\n')
    with open('err2.log', 'w+') as f:
        f.writelines('\n')
    with open('err3.log', 'w+') as f:
        f.writelines('\n')
    with open('stat.log', 'w+') as f:
        f.writelines('\n')
    file_list = glob.glob('*.log')
    for i in file_list:
        print(i)
        comp_line = 0
        comp_line_e2 = 0
        comp_line_e3 = 0
        comp_line_so = 0
        time.sleep(3)
        with open(i, 'r') as cur_file:
            cur_lines = cur_file.readlines()
            for line in cur_lines:
                if 'IS BLANK' in line:
                    comp_line = blank(i, line, comp_line)
                elif 'POTENTIAL ERROR (2)' in line:
                    comp_line_e2 = err2(i, line, comp_line_e2)
                elif 'ERROR (3)' in line:
                    comp_line_e3 = err3(i, line, comp_line_e3)
                elif 'STATUS: OK' in line:
                    comp_line_so = stat(i, line, comp_line_so)
        print(comp_line, ' after for')
        comp_line = 0
        comp_line_e2 = 0
        comp_line_e3 = 0
        comp_line_so = 0


def err3(fname, line, comp_line1):
    with open('err3.log', 'r') as f:
        fline_read = f.readlines()
    wline = f'=== {fname} ==='
    for line1 in fline_read:
        if comp_line1 >= 1:
            pass
        elif comp_line1 == 0:
            with open('err3.log', 'a') as f:
                f.writelines('\n' + wline + '\n')
            comp_line1 += 1
    with open('err3.log', 'a') as f:
        f.writelines(line)
    return comp_line1


def err2(fname, line, comp_line2):
    with open('err2.log', 'r') as f:
        fline_read = f.readlines()
    wline = f'=== {fname} ==='
    for line1 in fline_read:
        if comp_line2 >= 1:
            pass
        elif comp_line2 == 0:
            with open('err2.log', 'a') as f:
                f.writelines('\n' + wline + '\n')
            comp_line2 += 1
    with open('err2.log', 'a') as f:
        f.writelines(line)
    return comp_line2


def stat(fname, line, comp_line3):
    with open('stat.log', 'r') as f:
        fline_read = f.readlines()
    wline = f'=== {fname} ==='
    for line1 in fline_read:
        if comp_line3 >= 1:
            pass
        elif comp_line3 == 0:
            with open('stat.log', 'a') as f:
                f.writelines('\n' + wline + '\n')
            comp_line3 += 1
    with open('stat.log', 'a') as f:
        f.writelines(line)
    return comp_line3


def blank(fname, line, comp_line4):
    with open('blank.log', 'r') as f:
        fline_read = f.readlines()
    wline = f'=== {fname} ==='
    for line1 in fline_read:
        if comp_line4 >= 1:
            pass
        elif comp_line4 == 0:
            with open('blank.log', 'a') as f:
                f.writelines('\n' + wline + '\n')
            comp_line4 += 1
    with open('blank.log', 'a') as f:
        f.writelines(line)
    return comp_line4


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')
    log_files = config.get('summary', 'summary_folder')
    create_summary()
