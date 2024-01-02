from json import load, dump
from os import  system, name

#Color
class color:
	mark = "\033[104m"
	gray = "\033[90m"
	bold = "\033[1m"
	blue = "\033[94m"
	orange = "\033[33m"
	green = "\033[92m"
	yellow = "\033[93m"
	red = "\033[91m"
	purple = "\033[35m"
	reset = "\033[0m"

#Intro
system('cls' if name == 'nt' else 'clear')
print("{}█▀▄ ▄▀█ ▀█▀ ▄▀█{}".format(color.blue, color.reset))
print("{}█▄▀ █▀█  █  █▀█{}".format(color.blue, color.reset))
print("""
{}[1] Token
[2] Channel
[3] Grind
[4] Exp
[5] Coinflip
[6] Coinflip Bet
[7] Coinflip Rate
[8] Slot
[9] Slot bet
[10] Slot Rate
[11] Command
[12] Prefix
[13] Allow
[14] Webhook
[15] Link
[16] Ping{}""".format(color.orange, color.reset))

#Settings
def main():
	with open("config.json", "r") as f:
		data = load(f)
		print()
	choice = input("{}Enter Your Choice: {}".format(color.yellow, color.reset))
	if choice == "0":
		pass
	elif choice == "1":
		token(data, False)
	elif choice == "2":
		channel(data, False)
	elif choice == "3":
		grind(data, False)
	elif choice == "4":
		exp(data, False)
	elif choice == "5":
		coinflip(data, False)
	elif choice == "6":
		cfbet(data, False)
	elif choice == "7":
		cfrate(data, False)
	elif choice == "8":
		slot(data, False)
	elif choice == "9":
		sbet(data, False)
	elif choice == "10":
		srate(data, False)
	elif choice == "11":
		command(data, False)
	elif choice == "12":
		prefix(data, False)
	elif choice == "13":
		allow(data, False)
	elif choice == "14":
		webhook(data, False)
	elif choice == "15":
		link(data, False)
	elif choice == "16":
		ping(data, False)
	else:
		print("{}[INFO] Invalid!{}".format(color.red, color.reset))

#Token
def token(data, all):
	data['token'] = input("{}Enter Account Token: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Channel
def channel(data, all):
	data['channel'] = input("{}Enter Channel ID: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Grind
def grind(data, all):
	data['grind'] = input("{}Toggle Grinding (YES/NO): {}".format(color.gray, color.reset))
	data['grind'] = data['grind'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Exp
def exp(data, all):
	data['exp'] = input("{}Toggle Exp (YES/NO): {}".format(color.gray, color.reset))
	data['exp'] = data['exp'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Coinflip
def coinflip(data, all):
	data['coinflip'] = input("{}Toggle Coinflip (YES/NO): {}".format(color.gray, color.reset))
	data['coinflip'] = data['coinflip'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Coinflip Bet
def cfbet(data, all):
	data['cfbet'] = input("{}Enter Coinflip Bet: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Coinflip Rate
def cfrate(data, all):
	data['cfrate'] = input("{}Enter Coinflip Rate: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Slot
def slot(data, all):
	data['slot'] = input("{}Toggle Slot (YES/NO): {}".format(color.gray, color.reset))
	data['slot'] = data['slot'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Slot Bet
def sbet(data, all):
	data['sbet'] = input("{}Enter Slot Bet: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Slot Rate
def srate(data, all):
	data['srate'] = input("{}Enter Slot Rate: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Command
def command(data, all):
	data['command'] = input("{}Toggle Command (YES/NO): {}".format(color.gray, color.reset))
	data['command'] = data['command'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()


#Prefix
def prefix(data, all):
	data['prefix'] = input("{}Enter Prefix: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Allow
def allow(data, all):
	data['allow'] = input("{}Enter Allow ID: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Webhook
def webhook(data, all):
	data['webhook'] = input("{}Toggle Webhook (YES/NO): {}".format(color.gray, color.reset))
	data['webhook'] = data['webhook'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()


#Link
def link(data, all):
	data['link'] = input("{}Enter Webhook Link: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Ping
def ping(data, all):
	data['ping'] = input("{}Enter Ping ID: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

if __name__ == "__main__":
	main()
