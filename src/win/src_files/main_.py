import glob
import os
import re
import shutil
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchFrameException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

os_name = 'win'


def root_loc():
    rootloc = os.getcwd()
    return rootloc


passby_n = 0
rootloc = root_loc()
config = ConfigParser()
config.read('config.ini')
headless_active = int(config.get('selenium', 'headless_mode'))

# # # VARIABLES # # #
dldir = os.path.abspath(os.path.join(rootloc, 'csv\\download'))
merged_loc = os.path.abspath(os.path.join(rootloc, 'csv\\merge'))
csv_loc = os.path.abspath(os.path.join(rootloc, 'csv\\files'))
history = os.path.abspath(os.path.join(rootloc, 'csv\\history'))
history_merge = os.path.abspath(os.path.join(rootloc, 'csv\\history\\merge'))
history_err = os.path.abspath(os.path.join(rootloc, 'csv\\history\\errors'))
# File locations
# webdriver
fp = webdriver.FirefoxProfile()
options = Options()
if headless_active == 1:
    options.headless = True
fp.set_preference("browser.acceptInsecureCerts", True)
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", dldir)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
driver = webdriver.Firefox(firefox_profile=fp, options=options)
# webdriver
# login
uname = config.get('login', 'uname')
pword = config.get('login', 'pword')
url = config.get('login', 'url')
# email
fromaddress = config.get('email', 'from')
toaddress = config.get('email', 'to')
# email server
smtp_server_addr = config.get('email_server', 'smtp_server_addr')
smtp_server_port = config.get('email_server', 'smtp_server_port')
tls_t = int(config.get('email_server', 'tls'))
if tls_t == 1:
    tls = True
else:
    tls = False
smtp_pword = config.get('email_server', 'smtp_pword')
if int(config.get('file_locations', 'custom_location')) == 1:
    err_loc1 = config.get('file_locations', 'error_output')
else:
    err_loc1 = os.path.abspath(os.path.join(os.getcwd(), 'csv\\errors'))
# navigation
owner = config.get('navigation', 'owner_name')
customer = config.get('navigation', 'customer_name')
try:
    main_group = int(config.get('navigation', 'main_active'))  # Main group = not sub group
except ValueError:
    main_group = 0
isactive_suba = int(config.get('navigation', 'subgroupa'))
if isactive_suba == 1:
    subg_a = config.get('navigation', 'cust_subgroupa')

isactive_subb = int(config.get('navigation', 'subgroupb'))
if isactive_subb == 1:
    subg_b = config.get('navigation', 'cust_subgroupb')

isactive_subc = int(config.get('navigation', 'subgroupc'))
if isactive_subc == 1:
    subg_c = config.get('navigation', 'cust_subgroupc')
# extra info
abbr_cust = config.get('navigation', 'cust_abbr')

# # # VARIABLES # # #


def login():
    driver.get(url)
    driver.set_window_size(1890, 1050)
    while True:
        try:
            driver.switch_to.frame(2)
            frame_switch = True
        except NoSuchFrameException:
            time.sleep(2.5)
            frame_switch = False
        if frame_switch:
            break
    WebDriverWait(driver, 120).until(
        ec.element_to_be_clickable((By.ID, 'ctl09_login_username')))
    driver.find_element(By.ID, "ctl09_login_username").click()
    driver.find_element(By.ID, "ctl09_login_username").send_keys(uname)
    driver.find_element(By.ID, "ctl09_login_password").click()
    driver.find_element(By.ID, "ctl09_login_password").send_keys(pword)
    driver.find_element(By.ID, "ctl09_btnLogin").click()
    time.sleep(5)


def navigation(owner_n, customer_n, subgroup_n, passby_n):
    if passby_n == 0:
        if owner_n and customer_n == 'null':
            pass
        else:
            driver.switch_to.default_content()
            driver.switch_to.frame(1)
            WebDriverWait(driver, 60).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, ".selectGroupText")))
            driver.find_element(By.CSS_SELECTOR, ".selectGroupText").click()
            driver.find_element(By.LINK_TEXT, owner_n).click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, ".selectGroupText").click()
            driver.find_element(By.LINK_TEXT, customer_n).click()
            time.sleep(.5)
            if subgroup_n == 'null':
                driver.find_element(By.ID, "timerInfoImg").click()
                pass
            else:
                driver.find_element(By.CSS_SELECTOR, ".selectGroupText").click()
                driver.find_element(By.LINK_TEXT, subgroup_n).click()
                time.sleep(1)
                driver.find_element(By.ID, "timerInfoImg").click()
    if passby_n >= 1:
        if subgroup_n == 'null':
            pass
        else:
            driver.find_element(By.CSS_SELECTOR, ".selectGroupText").click()
            try:
                driver.find_element(By.LINK_TEXT, subgroup_n).click()
            except NoSuchElementException:
                driver.find_element(By.CSS_SELECTOR, ".selectGroupText").click()
                driver.find_element(By.LINK_TEXT, owner_n).click()
                driver.find_element(By.CSS_SELECTOR, ".selectGroupText").click()
                time.sleep(.5)
                driver.find_element(By.LINK_TEXT, customer_n).click()
                driver.find_element(By.CSS_SELECTOR, ".selectGroupText").click()
                time.sleep(.5)
                driver.find_element(By.LINK_TEXT, subgroup_n).click()
    time.sleep(1)
    WebDriverWait(driver, 60).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'vehListItem')))
    vehlist = driver.find_element(By.XPATH, '//*[@id="vehicleList"]')
    vehlist_r = vehlist.find_elements(By.CLASS_NAME, 'vehListItem')
    for i in vehlist_r:
        try:
            i.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", i)
        reg_name = i.find_element_by_tag_name('span').text
        reg_name_s = str(reg_name)
        file_name1 = re.sub('[^A-Za-z0-9]+ /', '', reg_name_s)
        file_name2 = re.sub(' ', '_', file_name1)
        file_name3 = re.sub('/', '_', file_name2)
        file_name4 = re.sub('\\*', '', file_name3)
        file_name5 = re.sub('\\[', '', file_name4)
        file_name6 = re.sub(']', '', file_name5)
        file_name = file_name6 + '.csv'
        print(file_name)
        driver.switch_to.default_content()
        driver.switch_to.frame(0)
        driver.find_element(By.CSS_SELECTOR, "a:nth-child(3) img").click()
        driver.switch_to.default_content()
        driver.switch_to.frame(2)
        WebDriverWait(driver, 60).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".reportNavButton:nth-child(44) > p")))
        driver.find_element(By.CSS_SELECTOR, ".reportNavButton:nth-child(44) > p").click()
        try:
            WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.ID, "ctl09_btnGenerateCSV")))
        except TimeoutException:
            driver.find_element_by_id('ctl09_btnGenerateCSV').click()
        time.sleep(.5)
        driver.find_element(By.ID, "ctl09_btnGenerateCSV").click()
        os.chdir(dldir)
        src_file = glob.glob('*.csv')
        timeout = time.time() + 30
        if not src_file:
            while True:
                if glob.glob('*.csv')[:1]:
                    break
                if time.time() > timeout:
                    driver.find_element(By.ID, "ctl09_btnGenerateCSV").click()
                    src_file1 = glob.glob('*.csv')
                    if not src_file1:
                        while True:
                            if glob.glob('*.csv')[:1]:
                                break
                            if time.time() > timeout:
                                print('Error getting report for', reg_name, file=err_veh)
                    elif src_file1:
                        pass
        elif src_file:
            pass
        for file in src_file:
            shutil.move(file, '..\\files' + '\\' + file_name)
        try:
            for d_file in src_file:
                os.remove(d_file)
        except FileNotFoundError:
            pass
        os.chdir(rootloc)
        driver.switch_to.default_content()
        driver.switch_to.frame(0)
        driver.switch_to.default_content()
        driver.switch_to.frame(1)
        driver.execute_script("arguments[0].click();", i)
        time.sleep(1)
    passby_n += 1
    return passby_n


def vehicle_select():
    # Originally, owner_f / owner_f1 etc were set to 'null' so the program knew not to restart the menu. Now, passby_n
    # variable should handle this, but null is being left in stable release until sure it's working OK.
    if main_group == 1:
        passby_1 = navigation(owner, customer, 'null', passby_n)
        if isactive_suba == 1:
            passby_2 = navigation(owner, customer, subg_a, passby_1)
            if isactive_subb == 1:
                owner_f = 'null'
                customer_f = 'null'
                passby_3 = navigation(owner_f, customer_f, subg_b, passby_2)
                if isactive_subc == 1:
                    owner_f1 = 'null'
                    customer_f1 = 'null'
                    navigation(owner_f1, customer_f1, subg_c, passby_3)
    else:
        if isactive_suba == 1:
            passby_2 = navigation(owner, customer, subg_a, passby_n)
            if isactive_subb == 1:
                owner_f = 'null'
                customer_f = 'null'
                passby_3 = navigation(owner_f, customer_f, subg_b, passby_2)
                if isactive_subc == 1:
                    owner_f1 = 'null'
                    customer_f1 = 'null'
                    navigation(owner_f1, customer_f1, subg_c, passby_3)
    driver.quit()


def csv_merge():
    import pandas as pd
    os.chdir(csv_loc)
    filenames = glob.glob('*.csv')
    writer = pd.ExcelWriter('merged_mdt.xlsx', engine='xlsxwriter')  # pylint: disable=abstract-class-instantiated
    for f in filenames:
        df = pd.read_csv(f, header=None, sep='\n')
        df = df[0].str.split(',', expand=True)
        df.to_excel(writer, sheet_name=os.path.splitext(f)[0])
    writer.save()
    mdt_name = 'merged_mdt' + date_r + '.xlsx'
    shutil.move('merged_mdt.xlsx', '..\\merge\\' + mdt_name)
    os.chdir(rootloc)


def csv_check():
    """
    check for:
    3's in column 1 that appear 3 times in a row
    2's in column 1 that appear 5 times in a row
    """
    from xlrd import open_workbook
    os.chdir(merged_loc)
    merged_book_l = glob.glob('*.xlsx')[:1]
    merged_book_m = str(merged_book_l[:1])
    mbn1 = re.sub("\\[", '', merged_book_m)
    mbn2 = re.sub("]", '', mbn1)
    merged_book_n = re.sub("'", '', mbn2)
    try:
        merge_book = open_workbook(merged_book_n)
        os.chdir(rootloc)
        for sheet in merge_book.sheets():
            reg_name = sheet.name
            print(sheet.name)
            sheet_val_o = sheet.col_values(2, 5)
            sheet_val = [val.replace('"', '') for val in sheet_val_o if val != '"']
            print(sheet_val)
            err_val3 = error_identifier3(sheet_val)
            reg_vis = re.sub('_', ' ', reg_name).strip()
            return_reg(reg_vis)
            err_val2 = error_identifier2(sheet_val)
            blank_check = is_blank(sheet_val)
            if err_val3:
                print(reg_vis, 'ERROR (3)', file=err_veh)

            elif err_val2:
                print(reg_vis, 'POTENTIAL ERROR (2)', file=err_veh)

            elif blank_check is True:
                print(reg_vis, 'IS BLANK', file=err_veh)

            elif sheet_val is None:
                print(reg_vis, 'Error getting report', file=err_veh)

            else:
                print(reg_vis, 'STATUS: OK', file=err_veh)
                print('\n')

            print(reg_vis, file=reg_list)
        print('\n', file=err_veh)
    except FileNotFoundError:
        print('File not found, program ending')


def return_reg(registration_no):
    vehicle_registration = registration_no
    return vehicle_registration


def error_identifier3(arr):
    if '333' in ''.join(arr):
        err_val3 = True
        return err_val3
    else:
        err_val3 = False
        return err_val3


def error_identifier2(arr):
    if '22222' in ''.join(arr):
        err_val2 = True
        return err_val2
    else:
        err_val2 = False
        return err_val2


def is_blank(arr):
    if not arr:
        blank_check = True
        return blank_check
    else:
        blank_check = False
        return blank_check


def email_report():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    msg = MIMEMultipart()
    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = owner + ': ' + abbr_cust + ' Camera Reports | Daily'
    os.chdir(err_loc)
    logged = open(err_fname)
    os.chdir(rootloc)
    bodymsg = logged.read()
    msg.attach(MIMEText(bodymsg, 'plain'))
    attachment = open(err_file, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename=mdt_report.txt")
    msg.attach(p)

    s = smtplib.SMTP(smtp_server_addr, smtp_server_port)
    if tls is True:
        s.starttls()
    s.login(fromaddress, smtp_pword)
    text = msg.as_string()
    s.sendmail(fromaddress, toaddress, text)
    s.quit()


def move_to_history():
    err_veh.close()
    os.chdir(merged_loc)
    mf_name = glob.glob('*.xlsx')
    try:
        for hist_file in mf_name:
            shutil.move(hist_file, history_merge)
    except shutil.Error:
        pass
    os.chdir(err_loc)
    reg_list.close()
    # try:
    #     shutil.move(err_fname, history_err_f)
    # except shutil.Error:
    #     pass
    try:
        shutil.move(err_file, full_reports)
    except shutil.Error:
        pass
    os.chdir(rootloc)


def cleanup_start():
    os.chdir(merged_loc)
    mdl_name = glob.glob('*.xlsx')
    for delete_m in mdl_name:
        os.remove(delete_m)
    os.chdir(dldir)
    dl_name = glob.glob('*.csv')
    for delete_dl in dl_name:
        os.remove(delete_dl)
    os.chdir(csv_loc)
    csvdl_name = glob.glob('*.csv')
    for delete_csv in csvdl_name:
        os.remove(delete_csv)
    #os.chdir(err_loc)
    #errdl_name = glob.glob(f'{customer}*.log') and glob.glob('blank_veh*.log')
    #for delete_log in errdl_name:
    #    os.remove(delete_log)
    os.chdir(rootloc)


def file_limit():
    file_list = glob.glob('*.log')
    if len(file_list) > 7:
        oldest_file = min(file_list, key=os.path.getctime)
        os.remove(os.path.abspath(oldest_file))
        listcheck_2 = os.listdir(full_reports)
        if len(listcheck_2) > 7:
            file_limit()


def weekly_init():
    import weekly_report
    weekly_report.cleanup()  # Removes last weekly report
    os.chdir(rootloc)
    weekly_report.read_report()
    weekly_report.read_full_report()
    weekly_report.error_alert()
    weekly_report.email_weekly_report(fromaddress, toaddress, smtp_pword, smtp_server_addr, smtp_server_port, tls,
                                      owner, abbr_cust, full_reports)  # Last function to run before ending
    weekly_report.history_cleanup()  # Removes files used to compile weekly report


if __name__ == '__main__':
    print('Cleaning..')
    cleanup_start()
    date_f = datetime.date(datetime.now())
    date_r = str(date_f)
    os.chdir(err_loc1)
    if os.path.isdir(date_r):
        pass
    else:
        os.mkdir(date_r)
    err_loc = os.path.abspath(os.path.join(err_loc1, date_r))
    os.chdir(err_loc)
    err_fname = customer + date_r + '.log'
    err_veh = open(err_fname, 'w+', encoding='utf-8')
    reg_list = open('registrations.txt', 'w+', encoding='utf-8')
    os.chdir(rootloc)
    full_reports = os.path.abspath(os.path.join(rootloc, 'csv\\history\\reports'))
    err_file = os.path.abspath(os.path.join(err_loc, err_fname))
    history_err_f = os.path.abspath(os.path.join(rootloc, f'{history_err}\\{err_fname}'))
    print('Started..')
    login()
    print('Logged in..')
    vehicle_select()
    print('Files downloaded..')
    csv_merge()
    print('Files merged..')
    csv_check()
    err_veh.close()
    email_report()
    move_to_history()
    print(f'MDT downloaded and scanned. Files can be found at {merged_loc}. Errors can be found at {full_reports}')
    os.chdir(full_reports)
    file_number = len(glob.glob('*.log'))

    if file_number == 7:
        os.chdir(rootloc)
        weekly_init()

    elif file_number > 7:
        file_limit()
        weekly_init()

    else:
        pass
    sys.exit()

# P_FIXED: Daily running code is bringing up 2-3 status reports for some vehicles, this seems to happen when there is
# a potential error, it then counts further and the remaining numbers suggest the status is OK.
