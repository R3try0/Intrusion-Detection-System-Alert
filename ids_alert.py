import os,sys,filecmp
from tkinter import messagebox
from tkinter import *
from time import sleep

warning_1 = 0
warning_2 = 0

def alert():
	# Just modify it and give an alert sound of your choise:)	
	s = os.system("mpg123 /home/adam/eas.mp3 > /dev/null 2>&1 & ")
	return s 

def check_modif():
	check = filecmp.cmp("/var/log/suricata/fast.log","/var/log/suricata/fast2.log")
	check2 = filecmp.cmp("/var/log/snort/snort.alert.fast","/var/log/snort/snort.alert.fast.2")
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
	


def message():
	r = messagebox.askyesno("Intrution Detected !!", "An Intrution has been detected it might be a false alarm. Disable internet ?")
	if r == 1:
		os.system("ifconfig wlan0 down && ifconfig lo down && ifconfig eth0 down && killall NetworkManager")
		os.system("killall -9 mpg123 2>&1 &")
	else:
		os.system("killall -9 mpg123 2>&1 &")
	main()

def print_intru():
	alert()
	if warning_2 == 1 and warning_1 == 1:
		with open('/var/log/snort/snort.alert.fast') as fp:
			for line in fp:
				pass
			file = line

		with open("/var/log/suricata/fast.log") as fp2:
			for line in fp2:
				pass
			file2 = line

		r = messagebox.showwarning("IDS Intrution Log",file + "\n\n\n" + file2)

	elif warning_2 == 1:
		with open('/var/log/snort/snort.alert.fast') as fp:
			for line in fp:
				pass
			file = line

		r = messagebox.showwarning("Snort Intrution Log",file)

	else:
		with open('/var/log/snort/snort.alert.fast') as fp:
			for line in fp:
				pass
			file = line
			
		r = messagebox.showwarning("Suricata Intrution Log",file)	

	try:
		print(file,"\n\n\n\n",file2)
	except:
		print(file)
	message()

def main():
	warning_1 = 0
	warning_2 = 0
	os.system("cp /var/log/snort/snort.alert.fast /var/log/snort/snort.alert.fast.2")
	os.system("cp /var/log/suricata/fast.log /var/log/suricata/fast2.log")
	check_modif()

main()
