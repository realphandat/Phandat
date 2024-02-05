#!/usr/bin/python
import discum
from requests import get
from os import system
import time
start_time = time.time()
from time import sleep, strftime, localtime
import random
import atexit
import json
from re import findall, sub
try:
	from os import startfile
except:
	pass

#Data
class client:
	with open('config.json', "r") as file:
		data = json.load(file)
		token = data["token"]
		channel = data["channel"]
		prefix = data["prefix"]
		owo = data["owo"]
		grind = data["grind"]
		quote = data["quote"]
		coinflip = data["coinflip"]
		coinflip_bet = int(data["cfbet"])
		coinflip_rate = int(data["cfrate"])
		slot = data["slot"]
		slot_bet = int(data["sbet"])
		slot_rate = int(data["srate"])
		gem = data["gem"]
		change = data["change"]
		sleep = data["sleep"]
		spam = ["owo","uwu"]
		side = ["h","t"]
		run = True
		gem_check = True
		gem_amount = 0
		grind_amount = 0
		quote_amount = 0
		benefit_amount = 0
		current_coinflip_bet = coinflip_bet
		current_slot_bet = slot_bet
		OwOID = "408785106942164992"
		user_id = ""
		user_name = ""
		guild_id = ""
		guild_name = ""

prefix = client.prefix
        
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

#Time
def timelog():
	return f'\033[104m{strftime("%H:%M:%S", localtime())}\033[0m'
def timerun():
	timerun = time.time() - start_time
	return f'{strftime("**__%H__h** **__%M__m** **__%S__s**",time.gmtime(timerun))}'

#Sign In
bot = discum.Client(token=client.token, log=False, build_num=0, x_fingerprint="None", user_agent=[
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36/PAsMWa7l-11',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.7.2) Gecko/20100101 / Firefox/60.7.2'])

#Log In
@bot.gateway.command
def on_ready(resp):
	if resp.event.ready_supplemental:
		user = bot.gateway.session.user
		client.user_id = user['id']
		client.user_name = user['username']
		client.guild_id = bot.getChannel(client.channel).json()['guild_id']
		client.guild_name = bot.gateway.session.guild(client.guild_id).name
		input("Press Enter to continue...")
		print()
		print("""{}    █▀█ █ █ █ █▀█{}""".format(color.blue, color.reset))
		print("""{}    █▄█ ▀▄▀▄▀ █▄█{}""".format(color.blue, color.reset))
		print("{}Logged in as {}{}{}{}".format(color.red, color.reset, color.bold, client.user_name, color.reset))
		print()
		start()

#Get Messages
def getMessages(num: int = 1, channel: str = client.channel) -> object:
	messageObject = None
	retries = 0
	while not messageObject:
		if not retries > 10:
			messageObject = bot.getMessages(channel, num=num)
			messageObject = messageObject.json()
			if not type(messageObject) is list:
				messageObject = None
			else:
				break
			retries += 1
			continue
		if type(messageObject) is list:
			break
		else:
			retries = 0
	return messageObject

#Captcha Bypass
@bot.gateway.command
def anticaptcha(resp):
	if resp.event.message:
		m = resp.parsed.auto()
		if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
			if '⚠' in m['content'] or 'real human' in m['content'] or 'https://owobot.com/captcha' in m['content'] or 'don\'t have enough cowoncy!' in m['content']:
				bot.gateway.close()

#Coinflip Check
@bot.gateway.command
def coinflip_check(resp):
	if client.run and client.coinflip:
		if resp.event.message_updated:
			m = resp.parsed.auto()
			try:
				if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
					#Lost
					if 'you lost' in m['content']:
						print("{} {}[INFO] Coinflip Lost {} Cowoncy{}".format(timelog(), color.red, client.current_coinflip_bet, color.reset))
						client.benefit_amount -= client.current_coinflip_bet
						client.current_coinflip_bet *= client.coinflip_rate
					#Won
					if 'you won' in m['content']:
						print("{} {}[INFO] Coinflip Won {} Cowoncy{}".format(timelog(), color.green, client.current_coinflip_bet, color.reset))
						client.benefit_amount += client.current_coinflip_bet
						client.current_coinflip_bet = client.coinflip_bet
			except KeyError:
				pass

#Slot Check
@bot.gateway.command
def slot_check(resp):
	if client.run and client.slot:
		if resp.event.message_updated:
			m = resp.parsed.auto()
			try:
				if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
					#Lost
					if 'won nothing' in m['content']:
						print("{} {}[INFO] Slot Lost {} Cowoncy{}".format(timelog(), color.red, client.current_slot_bet, color.reset))
						client.benefit_amount -= client.current_slot_bet
						client.current_slot_bet *= client.slot_rate
					#Draw
					if '<:eggplant:417475705719226369> <:eggplant:417475705719226369> <:eggplant:417475705719226369>' in m['content']:
						print("{} {}[INFO] Slot Draw{}".format(timelog(), color.bold, color.reset))
					#Won x2
					if '<:heart:417475705899712522> <:heart:417475705899712522> <:heart:417475705899712522>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x2){}".format(timelog(), color.green, client.current_slot_bet, color.reset))
						client.benefit_amount += client.current_slot_bet
						client.current_slot_bet = client.slot_bet
					#Won x3
					if '<:cherry:417475705178161162> <:cherry:417475705178161162> <:cherry:417475705178161162>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x3){}".format(timelog(), color.green, client.current_slot_bet * 2, color.reset))
						client.benefit_amount += client.current_slot_bet * 2
						client.current_slot_bet = client.slot_bet
					#Won x4
					if '<:cowoncy:417475705912426496> <:cowoncy:417475705912426496> <:cowoncy:417475705912426496>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x4){}".format(timelog(), color.green, client.current_slot_bet * 3, color.reset))
						client.benefit_amount += client.current_slot_bet * 3
						client.current_slot_bet = client.slot_bet
					#Won x10
					if '<:o_:417475705899843604> <:w_:417475705920684053> <:o_:417475705899843604>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x10){}".format(timelog(), color.green, client.current_slot_bet * 9, color.reset))
						client.benefit_amount += client.current_slot_bet * 9
						client.current_slot_bet = client.slot_bet
			except KeyError:
				pass

#Gem Check
@bot.gateway.command
def gem_check(resp):
	if client.run and client.gem and client.gem_check:
		if resp.event.message:
			m = resp.parsed.auto()
			if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
				if "and caught" in m['content']:
					gem()
				

#Grind
def grind():
	if client.run and client.owo:
		spam = random.choice(client.spam)
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}".format(spam))
		print("{} {}[SENT] {}{}".format(timelog(), color.yellow, spam, color.reset))
		sleep(random.randint(1, 2))
	if client.run and client.grind:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}h".format(prefix))
		print("{} {}[SENT] {}h{}".format(timelog(), color.yellow, prefix, color.reset))
		sleep(random.randint(1, 2))
	if client.run and client.gem and client.gem_check:
		print("{} {}[SELF] I'm Checking Gem Status{}".format(timelog(), color.gray, color.reset))
	if client.run and client.grind:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}b".format(prefix))
		print("{} {}[SENT] {}b{}".format(timelog(), color.yellow, prefix, color.reset))
		client.grind_amount += 1
		sleep(random.randint(1, 2))

#Quote
def quote():
	if client.quote and client.run:
		try:	
			response = get("https://zenquotes.io/api/random")
			if response.status_code == 200:
				json_data = response.json()
				data = json_data[0]
				bot.typingAction(client.channel)
				bot.sendMessage(client.channel, data['q'])
				print("{} {}[SENT] Quote{}".format(timelog(), color.yellow, color.reset))
				client.quote_amount += 1
				sleep(random.randint(1, 2))
		except:
			pass

#Coinflip
def coinflip():
	if client.current_coinflip_bet  > 250000:
		client.current_coinflip_bet = client.coinflip_bet
	if client.run and client.coinflip:
		side = random.choice(client.side)
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}cf {} {}".format(prefix, client.current_coinflip_bet, side))
		print("{} {}[SENT] {}cf {} {}{}".format(timelog(), color.yellow, prefix, client.current_coinflip_bet, side, color.reset))
		sleep(random.randint(1, 2))

#Slot
def slot():
	if client.current_slot_bet  > 250000:
		client.current_slot_bet = client.slot_bet
	if client.run and client.slot:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}s {}".format(prefix, client.current_slot_bet))
		print("{} {}[SENT] {}s {}{}".format(timelog(), color.yellow, prefix, client.current_slot_bet, color.reset))
		sleep(random.randint(1, 2))

#Gem
def gem():
	if client.run and client.gem and client.gem_check:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}inv".format(prefix))
		print("{} {}[SENT] {}inv{}".format(timelog(), color.yellow, prefix, color.reset))
		msg = bot.getMessages(str(client.channel), num=10)
		msg = msg.json()
		inv = ""
		for i in range(len(msg)):
			if msg[i]['author']['id'] == client.OwOID and 'Inventory' in msg[i]['content']:
				inv = findall(r'`(.*?)`', msg[i]['content'])
		sleep(random.randint(3, 5))
		if not inv:
			sleep(random.randint(1, 2))
			return
		else:
			#Common
			if "051" and "065" and "072" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), "{}use 51 65 72".format(prefix))
				print("{} {}[SENT] {}use 51 65 72{}".format(timelog(), color.yellow, prefix, color.reset))
				print("{} {}[SELF] I Used{} {}Common Gem{} {}For 25 Turns{}".format(timelog(), color.gray, color.reset, color.blue, color.reset, color.gray, color.reset))
				client.gem_amount += 1
			#Uncommon
			elif "052" and "066" and "073" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), "{}use 52 66 73".format(prefix))
				print("{} {}[SENT] {}use 52 66 73{}".format(timelog(), color.yellow, prefix, color.reset))
				print("{} {}[SELF] I Used{} {}Uncommon Gem{} {}For 25 Turns{}".format(timelog(), color.gray, color.reset, color.blue, color.reset, color.gray, color.reset))
				client.gem_amount += 1
			#Rare
			elif "053" and "067" and "074" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), "{}use 53 67 74".format(prefix))
				print("{} {}[SENT] {}use 53 67 74{}".format(timelog(), color.yellow, prefix, color.reset))
				print("{} {}[SELF] I Used{} {}Rare Gem{} {}For 50 Turns{}".format(timelog(), color.gray, color.reset, color.blue, color.reset, color.gray, color.reset))
				client.gem_amount += 1
			#Epic
			elif "054" and "068" and "075" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), "{}use 54 68 75".format(prefix))
				print("{} {}[SENT] {}use 54 68 75{}".format(timelog(), color.yellow, prefix, color.reset))
				print("{} {}[SELF] I Used{} {}Epic Gem{} {}For 75 Turns{}".format(timelog(), color.gray, color.reset, color.blue, color.reset, color.gray, color.reset))
				client.gem_amount += 1
			#Mythical
			elif "055" and "069" and "076" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), "{}use 55 69 76".format(prefix))
				print("{} {}[SENT] {}use 55 69 76{}".format(timelog(), color.yellow, prefix, color.reset))
				print("{} {}[SELF] I Used{} {}Mythical Gem{} {}For 75 Turns{}".format(timelog(), color.gray, color.reset, color.blue, color.reset, color.gray, color.reset))
				client.gem_amount += 1
			#Legendary
			elif "056" and "070" and "077" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), "{}use 56 70 77".format(prefix))
				print("{} {}[SENT] {}use 56 70 77{}".format(timelog(), color.yellow, prefix, color.reset))
				print("{} {}[SELF] I Used{} {}Legendary Gem{} {}For 100 Turns{}".format(timelog(), color.gray, color.reset, color.blue, color.reset, color.gray, color.reset))
				client.gem_amount += 1
			#Fabled
			elif "057" and "071" and "078" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), "{}use 57 71 78".format(prefix))
				print("{} {}[SENT] {}use 57 71 78{}".format(timelog(), color.yellow, prefix, color.reset))
				print("{} {}[SELF] I Used{} {}Fabled Gem{} {}For 100 Turns{}".format(timelog(), color.gray, color.reset, color.blue, color.reset, color.gray, color.reset))
				client.gem_amount += 1
			#Don't Have Enough Gem
			else:
				print("{} {}[SELF]{} {}Stop Using!{} {}I Don\'t Have Enough Gems{}".format(timelog(), color.gray, color.reset, color.red, color.reset, color.gray, color.reset))
				client.gem_check = False

#Change
def change():
	if client.run and client.change:
		other_channel = []
		channels = bot.gateway.session.guild(client.guild_id).channels
		for i in channels:
			if channels[i]['type'] == "guild_text":
				other_channel.append(i)
		other_channel = random.choice(other_channel)
		return other_channel, channels[other_channel]['name']

#Sleep
def die():
	if client.run and client.sleep:
		die = random.randint(300, 600)
		print("{} {}[SELF] I'm Taking A Break For{} {}{} Seconds{}".format(timelog(), color.gray, color.reset, color.bold, die, color.reset))
		sleep(die)

#Start
def start():
	grind_time = 0
	quote_time = 0
	coinflip_time = 0
	slot_time = 0
	change_time = time.time()
	sleep_time = time.time()
	grind_spam = 0
	quote_spam = 0
	coinflip_spam = 0
	slot_spam = 0
	change_spam = random.randint(600, 1200)
	sleep_spam = random.randint(600, 1200)
	while True:
		if client.run:
			#Grind
			if time.time() - grind_time > grind_spam:
				grind_time = time.time()
				grind_spam = random.randint(17, 25)
				grind()
			#Quote
			if time.time() - quote_time > quote_spam:
				quote_time = time.time()
				quote_spam = random.randint(30, 60)
				quote()
			#Coinflip
			if time.time() - coinflip_time > coinflip_spam:
				coinflip_time = time.time()
				coinflip_spam = random.randint(20, 30)
				coinflip()
			#Slot
			if time.time() - slot_time > slot_spam:
				slot_time = time.time()
				slot_spam = random.randint(20, 30)
				slot()
			#Change
			if time.time() - change_time > change_spam and client.change:
				change_time = time.time()
				change_spam = random.randint(600, 1200)
				channel = change()
				client.channel = channel[0]
				print("{} {}[SELF] I Changed The Channel To{} {}{}{}".format(timelog(), color.gray, color.reset, color.bold, channel[1], color.reset))
			#Sleep
			if time.time() - sleep_time > sleep_spam and client.sleep:
				die()
				sleep_time = time.time()
				sleep_spam = random.randint(600, 1200)
				print("{} {}[SELF] Done! I'll Work For{} {}{} Seconds{}".format(timelog(), color.gray, color.reset, color.bold, sleep_spam, color.reset))
			sleep(1)
bot.gateway.run()

#Exit
@atexit.register
def exit():
	client.run = False
	try:
		startfile('music.mp3')
	except:
		pass
	print("{} {}[SELF] I Found Some Problem".format(timelog(), color.gray, color.reset))
	print()
	print("    {}Gem:{}    {}{} Sets {}".format(color.green, color.reset, color.bold, client.gem_amount, color.reset))
	print("    {}Grind:{}  {}{} Times {}".format(color.green, color.reset, color.bold, client.grind_amount, color.reset))
	print("    {}Quote:{}  {}{} Quotes {}".format(color.green, color.reset, color.bold, client.quote_amount, color.reset))
	print("    {}Gamble:{} {}{} Cowoncys {}".format(color.green, color.reset, color.bold, client.benefit_amount, color.reset))
	exit = input("{}Enter 'OK' to Reset: {}".format(color.blue, color.reset))
	if exit.lower() == 'ok':
		system('python "main.py"')
