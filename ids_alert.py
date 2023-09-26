import os,sys,filecmp,subprocess
from tkinter import messagebox
from tkinter import *
from time import sleep


username = os.getlogin()
warning_1 = 0
warning_2 = 0

def check_modif():
	check = filecmp.cmp("/var/log/suricata/fast.log","/var/log/suricata/fast2.log")# checking the suricata intrution log
	check2 = filecmp.cmp("/var/log/snort/snort.alert.fast","/var/log/snort/snort.alert.fast.2")# checking the snort intrution log
	while True:
		if check == True and check2 == True:
			check = filecmp.cmp("/var/log/suricata/fast.log","/var/log/suricata/fast2.log")
			check2 = filecmp.cmp("/var/log/snort/snort.alert.fast","/var/log/snort/snort.alert.fast.2")
			sleep(10)

		elif check == False and check2 == False:
			warning_1 = 1 
			warning_2 = 1
			print_intru() 
			break

		elif check == False:
			warning_1 = 1
			print_intru()
			break

		else:
			warning_2 = 1
			print_intru() 
			break

def mail(ids,file):
	smtp_server = ""# put your smtp server (like gmail,outlook...etc)
	sender = ""#  the email that the script is going to login and send the email
	sender_password = "" # the password of the sender
	recipient = "" # the email of the recipient
	message =  f""" Intrution Detected !!", "An Intrution has been detected it by {ids}\n Log: {file}"""# fill free to change the messege {"Title", "Messege"}
	try:
		SSL_context = ssl.create_default_context()
		with smtplib.SMTP(smtp_server + smtp_server2, 587) as server:
		    server.starttls(context=SSL_context)
		    server.login(sender, sender_password)
		    server.sendmail(sender, recipient, message)
	except:
		print("Error: No login credentials OR Failed to connect to the SMTP Server. Check your internet connection")
		return


def message():
	r = messagebox.askyesno("Intrution Detected !!", "An Intrution has been detected it might be a false alarm. Disable internet ?")# fill free to change the messege
	if r == 1:
		os.system("ifconfig wlan0 down && ifconfig lo down && ifconfig eth0 down && killall NetworkManager")
		os.system("killall -9 mpg123")
	else:
		os.system("killall -9 mpg123")
	main()

def print_intru():
	s = os.system(f"mpg123 /home/{username}/eas.mp3 > /dev/null 2>&1 & ")
	if warning_2 == 1 and warning_1 == 1:
		with open('/var/log/snort/snort.alert.fast') as fp:
			for line in fp:
				file += line + "\n"

		with open("/var/log/suricata/fast.log") as fp2:
			for line in fp:
				file += line + "\n"
		mail("Snort & Suricata",file)
		r = messagebox.showwarning("IDS Intrution Log",file + "\n\n\n" + file2)

	elif warning_2 == 1:
		with open('/var/log/snort/snort.alert.fast') as fp:
			for line in fp:
				file += line + "\n"
		mail("Snort",file)
		r = messagebox.showwarning("Snort Intrution Log",file)

	else:
		with open('/var/log/suricata/fast.log') as fp:
			for line in fp:
				file += line + "\n"
		mail("Suricata",file)
		r = messagebox.showwarning("Suricata Intrution Log",file)	

	try:
		print(file,"\n\n\n\n",file2)

	except:
		print(file)

	message()

def main():
	suricata_service_active = subprocess.Popen(["systemctl","is-active","suricata"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	snort_service_active = subprocess.Popen(["systemctl","is-active","snort"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if suricata_service_active.stdout.read() ==  "b'inactive\n'" and snort_service_active.stdout.read() == "b'inactive\n'":
		b = os.system("systemctl start suricata && systemctl start snort")
	elif snort_service_active.stdout.read() == "b'inactive\n'":
		b = os.system("systemctl start snort")
	else:
		b = os.system("systemctl start suricata")
	warning_1 = 0
	warning_2 = 0
	os.system("cp /var/log/snort/snort.alert.fast /var/log/snort/snort.alert.fast.2")
	os.system("cp /var/log/suricata/fast.log /var/log/suricata/fast2.log")
	check_modif()
	
	
if __name__=="__main__":
	try:
		main()
	except Exception as error:
		print("An error occourd: ",error)
		exit()
