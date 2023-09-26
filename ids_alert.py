import os
import sys
import filecmp
import subprocess
import smtplib
import ssl
from tkinter import messagebox
from tkinter import *
from time import sleep

username = os.getlogin()
warning_1 = 0
warning_2 = 0

def check_modif():
    check = filecmp.cmp("/var/log/suricata/fast.log", "/var/log/suricata/fast2.log")
    check2 = filecmp.cmp("/var/log/snort/snort.alert.fast", "/var/log/snort/snort.alert.fast.2")
    
    while True:
        if check and check2:
            check = filecmp.cmp("/var/log/suricata/fast.log", "/var/log/suricata/fast2.log")
            check2 = filecmp.cmp("/var/log/snort/snort.alert.fast", "/var/log/snort/snort.alert.fast.2")
            sleep(10)
        elif not check and not check2:
            warning_1 = 1
            warning_2 = 1
            print_intru()
            break
        elif not check:
            warning_1 = 1
            print_intru()
            break
        else:
            warning_2 = 1
            print_intru()
            break

def mail(ids, file):
    smtp_server = ""  # put your smtp server (like gmail, outlook, etc.)
    sender = ""  # the email that the script is going to login and send the email
    sender_password = ""  # the password of the sender
    recipient = ""  # the email of the recipient
    message = f"""Intrusion Detected !!\nAn Intrusion has been detected by {ids}\nLog: {file}"""  # feel free to change the message

    try:
        SSL_context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls(context=SSL_context)
            server.login(sender, sender_password)
            server.sendmail(sender, recipient, message)
    except Exception as e:
        print("Error:", str(e))
        return

def message():
    r = messagebox.askyesno("Intrusion Detected !!", "An Intrusion has been detected. It might be a false alarm. Disable internet?")
    if r:
        subprocess.run(["ifconfig", "wlan0", "down"])
        subprocess.run(["ifconfig", "lo", "down"])
        subprocess.run(["ifconfig", "eth0", "down"])
        subprocess.run(["killall", "NetworkManager"])
        subprocess.run(["killall", "-9", "mpg123"])
    else:
        subprocess.run(["killall", "-9", "mpg123"])
    main()

def print_intru():
    global warning_1, warning_2
    file = ""
    file2 = ""
    
    if warning_2 == 1 and warning_1 == 1:
        with open('/var/log/snort/snort.alert.fast') as fp:
            for line in fp:
                file += line + "\n"

        with open("/var/log/suricata/fast.log") as fp2:
            for line in fp:
                file += line + "\n"
        mail("Snort & Suricata", file)
        r = messagebox.showwarning("IDS Intrusion Log", file + "\n\n\n" + file2)

    elif warning_2 == 1:
        with open('/var/log/snort/snort.alert.fast') as fp:
            for line in fp:
                file += line + "\n"
        mail("Snort", file)
        r = messagebox.showwarning("Snort Intrusion Log", file)

    else:
        with open('/var/log/suricata/fast.log') as fp:
            for line in fp:
                file += line + "\n"
        mail("Suricata", file)
        r = messagebox.showwarning("Suricata Intrusion Log", file)

    try:
        print(file, "\n\n\n\n", file2)
    except:
        print(file)

    message()

def main():
    global warning_1, warning_2
    suricata_service_active = subprocess.Popen(["systemctl", "is-active", "suricata"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    snort_service_active = subprocess.Popen(["systemctl", "is-active", "snort"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    if suricata_service_active.stdout.read() == b'inactive\n' and snort_service_active.stdout.read() == b'inactive\n':
        b = os.system("systemctl start suricata && systemctl start snort")
    elif snort_service_active.stdout.read() == b'inactive\n':
        b = os.system("systemctl start snort")
    else:
        b = os.system("systemctl start suricata")
    
    warning_1 = 0
    warning_2 = 0
    os.system("cp /var/log/snort/snort.alert.fast /var/log/snort/snort.alert.fast.2")
    os.system("cp /var/log/suricata/fast.log /var/log/suricata/fast2.log")
    check_modif()

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("An error occurred:", error)
