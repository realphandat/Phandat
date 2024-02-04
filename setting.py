from json import load, dump
from os import  system, name

#Color
class color:
	mark = "\033[104m"
	gray = "\033[90m"
	bold = "\033[1m"
	blue = "\033[94m"
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
[3] Prefix
[4] OwO
[5] Grind
[6] Exp
[7] Coinflip
[8] Coinflip Bet
[9] Coinflip Rate
[10] Slot
[11] Slot bet
[12] Slot Rate
[13] Gem
[14] Change
[15] Sleep{}""".format(color.bold, color.reset))

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
		prefix(data, False)
	elif choice == "4":
		owo(data, False)
	elif choice == "5":
		grind(data, False)
	elif choice == "6":
		quote(data, False)
	elif choice == "7":
		coinflip(data, False)
	elif choice == "8":
		cfbet(data, False)
	elif choice == "9":
		cfrate(data, False)
	elif choice == "10":
		slot(data, False)
	elif choice == "11":
		sbet(data, False)
	elif choice == "12":
		srate(data, False)
	elif choice == "13":
		gem(data, False)
	elif choice == "14":
		change(data, False)
	elif choice == "15":
		sleep(data, False)
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

#Prefix
def prefix(data, all):
	data['prefix'] = input("{}Enter OwO's Prefix: {}".format(color.gray, color.reset))
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#OwO
def owo(data, all):
	data['owo'] = input("{}Toggle OwO (YES/NO): {}".format(color.gray, color.reset))
	data['owo'] = data['owo'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Grind
def grind(data, all):
	data['grind'] = input("{}Toggle Grind (YES/NO): {}".format(color.gray, color.reset))
	data['grind'] = data['grind'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Quote
def quote(data, all):
	data['quote'] = input("{}Toggle Quote (YES/NO): {}".format(color.gray, color.reset))
	data['quote'] = data['quote'].lower() == "yes"
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

#Gem
def gem(data, all):
	data['gem'] = input("{}Toggle Using Gem (YES/NO): {}".format(color.gray, color.reset))
	data['gem'] = data['gem'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()


#Change
def change(data, all):
	data['change'] = input("{}Toggle Change Channel (YES/NO): {}".format(color.gray, color.reset))
	data['change'] = data['change'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

#Sleep
def sleep(data, all):
	data['sleep'] = input("{}Toggle Sleep Mode (YES/NO): {}".format(color.gray, color.reset))
	data['sleep'] = data['sleep'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print("{}[INFO] Saved!{}".format(color.green, color.reset))
	if not all:
		main()

if __name__ == "__main__":
	main()
