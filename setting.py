from json import load, dump
from os import  system, name

#Color
class color:
	mark = "\033[104m"
	bold = "\033[1m"
	gray = "\033[90m"
	cyan = "\033[36m"
	blue = "\033[94m"
	orange = "\033[33m"
	yellow = "\033[93m"
	red = "\033[91m"
	green = "\033[92m"
	purple = "\033[95m"
	reset = "\033[0m"

#Intro
system('cls' if name == 'nt' else 'clear')
print(f"""{color.blue}█▀▄ ▄▀█ ▀█▀ ▄▀█
█▄▀ █▀█  █  █▀█{color.reset}""")
print(f""" {color.bold}[1] Token
 [2] Nickname
 [3] Channel
 [4] Prefix
 [5] OwO
 [6] Grind
 [7] Exp
 [8] Coinflip
 [9] Coinflip Bet
[10] Coinflip Rate
[11] Slot
[12] Slot bet
[13] Slot Rate
[14] Daily
[15] Gem
[16] Sleep
[17] Webhook{color.reset}""")

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
		nickname(data, False)
	elif choice == "3":
		channel(data, False)
	elif choice == "4":
		prefix(data, False)
	elif choice == "5":
		owo(data, False)
	elif choice == "6":
		grind(data, False)
	elif choice == "7":
		quote(data, False)
	elif choice == "8":
		coinflip(data, False)
	elif choice == "9":
		cfbet(data, False)
	elif choice == "10":
		cfrate(data, False)
	elif choice == "11":
		slot(data, False)
	elif choice == "12":
		sbet(data, False)
	elif choice == "13":
		srate(data, False)
	elif choice == "14":
		daily(data, False)
	elif choice == "15":
		gem(data, False)
	elif choice == "16":
		sleep(data, False)
	elif choice == "17":
		webhook(data, False)
	else:
		print(f"{color.red}[INFO] Invalid!{color.reset}")

#Token
def token(data, all):
	data['token'] = input(f"{color.gray} - Enter Your Account Token: {color.reset}")
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Nickname
def nickname(data, all):
	data['nickname'] = input(f"{color.gray} - Enter Your Discord Display Name (Nickname If Available): {color.reset}")
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Channel
def channel(data, all):
	channel = []
	try:
		num = int(input(f"{color.gray} - How Many Channels Do You Want To Use: {color.reset}"))
	except ValueError:
		print(f"{color.red}[INFO] Invalid!{color.reset}")
	for i in range(1, num + 1):
		add = input(f"{color.gray}  +  Enter Channel ID {i}: {color.reset}")
		channel += [add]
	data['channel'] = channel
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Prefix
def prefix(data, all):
	data['prefix'] = input(f"{color.gray} - Enter OwO's Prefix: {color.reset}")
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#OwO
def owo(data, all):
	data['owo'] = input(f"{color.gray} - Toggle Spamming OwO/UwU (YES/NO): {color.reset}")
	data['owo'] = data['owo'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Grind
def grind(data, all):
	data['grind'] = input(f"{color.gray} - Toggle Grinding (YES/NO): {color.reset}")
	data['grind'] = data['grind'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Quote
def quote(data, all):
	data['quote'] = input(f"{color.gray} - Toggle Sending Quote (YES/NO): {color.reset}")
	data['quote'] = data['quote'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Coinflip
def coinflip(data, all):
	data['coinflip'] = input(f"{color.gray} - Toggle Playing Coinflip (YES/NO): {color.reset}")
	data['coinflip'] = data['coinflip'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Coinflip Bet
def cfbet(data, all):
	data['cfbet'] = input(f"{color.gray} - Enter Coinflip Bet: {color.reset}")
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Coinflip Rate
def cfrate(data, all):
	data['cfrate'] = input(f"{color.gray} - Enter Coinflip Rate: {color.reset}")
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Slot
def slot(data, all):
	data['slot'] = input(f"{color.gray} - Toggle Playing Slot (YES/NO): {color.reset}")
	data['slot'] = data['slot'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()


#Slot Bet
def sbet(data, all):
	data['sbet'] = input(f"{color.gray} - Enter Slot Bet: {color.reset}")
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()

#Slot Rate
def srate(data, all):
	data['srate'] = input(f"{color.gray} - Enter Slot Rate: {color.reset}")
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()

#Daily
def daily(data, all):
	data['daily'] = input(f"{color.gray} - Toggle Claim Daily (YES/NO): {color.reset}")
	data['daily'] = data['daily'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()

#Gem
def gem(data, all):
	data['gem'] = input(f"{color.gray} - Toggle Using Gem (YES/NO): {color.reset}")
	data['gem'] = data['gem'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()

#Sleep
def sleep(data, all):
	data['sleep'] = input(f"{color.gray} - Toggle Sleeping Mode (YES/NO): {color.reset}")
	data['sleep'] = data['sleep'].lower() == "yes"
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()

#Webhook
def webhook(data, all):
	data['webhook'] = input(f"{color.gray} - Enter Your Webhook's URL: {color.reset}")
	file = open("config.json", "w")
	dump(data, file, indent = 4)
	file.close()
	print(f"{color.green}[INFO] Saved!{color.reset}")
	main()

if __name__ == "__main__":
	main()
