import os
import glob
import re
from configparser import NoSectionError
import time
from main_ import root_loc
try:
    root_local = root_loc()
except NoSectionError:
    time.sleep(2)
    root_local = root_loc()

os.chdir(root_local)
os_name = 'win'

hist_reports = os.path.abspath(os.path.join(root_local, 'csv\\history\\reports'))
hist_merge = os.path.abspath(os.path.join(root_local, 'csv\\history\\merge'))
weekly_rep = os.path.abspath(os.path.join(root_local, 'csv\\weekly'))
reg_no = os.path.abspath(os.path.join(root_local, 'csv\\errors\\registrations.txt'))
weekly_err_rep = os.path.abspath(os.path.join(root_local, 'csv\\weekly\\weekly_error_rep.log'))


def email_weekly_report(fromaddress, toaddress, smtp_pword, smtp_server_addr, smtp_server_port, tls, owner,
                        abbr_cust, full_reports):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    msg = MIMEMultipart()
    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = owner + ': ' + abbr_cust + ' Camera Reports | Weekly'
    os.chdir(root_local)
    attachment = open(weekly_err_rep)
    bodymsg = attachment.read()
    msg.attach(MIMEText(bodymsg, 'plain'))
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename=weekly_mdt_report.txt")
    msg.attach(p)
    s = smtplib.SMTP(smtp_server_addr, smtp_server_port)
    if tls is True:
        s.starttls()
    s.login(fromaddress, smtp_pword)
    text = msg.as_string()
    s.sendmail(fromaddress, toaddress, text)
    s.quit()


def history_cleanup():
    os.chdir(hist_reports)
    he_list = glob.glob('*.log')
    for i in he_list:
        os.remove(i)
    os.chdir(hist_merge)
    hm_list = glob.glob('*.xlsx')
    for j in hm_list:
        os.remove(j)
    print(root_local, 'ROOT')
    os.chdir(root_local)


def read_report():
    os.chdir(weekly_rep)
    with open('errors_merged.log', "wb") as outfile:
        os.chdir(hist_reports)
        hist_logs = glob.glob('*.log')
        for f in hist_logs:
            with open(f, 'rb') as infile:
                outfile.write(infile.read())


def read_full_report():
    os.chdir(weekly_rep)
    registrations = open(reg_no, 'r', encoding='utf-8')
    reg_lines = registrations.readlines()
    registrations.close()

    regs = []

    for regi in reg_lines:
        reg_1 = re.sub(' ', '', regi)
        reg_ = re.sub('\\n', '', reg_1)
        rtf = open(reg_+'.log', 'w+', encoding='utf-8')
        rtf.close()

    with open(reg_no) as file1:
        for line in file1:
            regs.append(line.strip())

    with open('errors_merged.log') as file2:
        for j in regs:
            blank_dict = {j: 0}
            err2_dict = {j: 0}
            err3_dict = {j: 0}
            errg_dict = {j: 0}
            ok_dict = {j: 0}
        for line in file2:
            for i in regs:
                if i in line:
                    blankstring = i + ' IS BLANK'
                    err2string = i + ' POTENTIAL ERROR (2)'
                    err3string = i + ' ERROR (3)'
                    err_get = i + ' Error getting report'
                    statusstring = i + ' STATUS: OK'
                    if blankstring in line:
                        blank_dict[i] = blank_dict.get(i, 0) + 1
                    if err2string in line:
                        err2_dict[i] = err2_dict.get(i, 0) + 1
                    if err3string in line:
                        err3_dict[i] = err3_dict.get(i, 0) + 1
                    if err_get in line:
                        errg_dict[i] = errg_dict.get(i, 0) + 1
                    if statusstring in line:
                        ok_dict[i] = ok_dict.get(i, 0) + 1

    with open('weekly_rep.log', 'w') as file3:
        for j in regs:
            print('BLANKS for', j, ':', blank_dict.get(j), file=file3)
            print('ERROR2 for', j, ':', err2_dict.get(j), file=file3)
            print('ERROR3 for', j, ':', err3_dict.get(j), file=file3)
            print('REPORT_ERROR for', j, ':', errg_dict.get(j), file=file3)
            print('OK for', j, ':', ok_dict.get(j), file=file3)
            print('\n', file=file3)
    
    txt_files = glob.glob('*.log')
    for cm in txt_files:
        with open(cm, 'r') as ff:
            lines = ff.readlines()
            lines1 = [q for q in lines if "ROW" in q]
            with open('weekly_rep.log', 'a+') as f1:
                f1.writelines(lines1)
                print('\n', file=f1)


def error_alert():
    with open('weekly_rep.log', 'r') as file:
        for i in file:
            # Get number of: blanks, error2, error3, report errors and OK's, if err3 is x then report, etc
            if 'BLANKS for ' in i:
                reg_h1 = i[11:]
                reg = reg_h1[:reg_h1.find(":")]
                # Defined here as "BLANKS for" is the first field, reg helps filter the list by registration plate
                if reg in i:
                    print(reg)
                    print(re.sub(r'^.*?:', '', i))

            if 'ERROR2 for ' in i:
                if reg in i:
                    try:
                        err2_val = int(re.sub(r'^.*?:', '', i))
                        if err2_val > 4:
                            err2 = f'Potential issues: {err2_val} for {reg}'
                            error_report(err2)
                    except ValueError:
                        pass
                
            if 'ERROR3 for ' in i:
                if reg in i:
                    try:
                        err3_val = int(re.sub(r'^.*?:', '', i))
                        if err3_val > 1:
                            err3 = f'Issues: {err3_val} for {reg}'
                            error_report(err3)
                    except ValueError:
                        pass


def error_report(err_type):
    with open('weekly_error_rep.log', 'a+') as file:
        file.write(err_type)
        file.write('\n')


def cleanup():
    os.chdir(weekly_rep)
    cf = glob.glob('*.log')
    for rem in cf:
        os.remove(rem)


if __name__ == '__main__':
    cleanup()  # Run this first, deletes last weekly report
    read_report()
    read_full_report()
    error_alert()
    history_cleanup()  # RUN THIS LAST
    
    import sys
    sys.exit()
