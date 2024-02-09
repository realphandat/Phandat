#!/usr/bin/python
import discum
from requests import get
from os import system
import time
from datetime import timedelta
start_time = time.time()
from time import sleep, strftime, localtime
import random
import json
import atexit
from re import findall
from discord_webhook import DiscordWebhook
try:
	from os import startfile
except:
	pass

#Data
class client:
	with open('config.json', "r") as file:
		data = json.load(file)
		token = data["token"]
		nickname = data["nickname"]
		allchannel = data["channel"]
		prefix = data["prefix"]
		owo = data["owo"]
		grind = data["grind"]
		quote = data["quote"]
		slot = data["slot"]
		slot_bet = int(data["sbet"])
		slot_rate = int(data["srate"])
		coinflip = data["coinflip"]
		coinflip_bet = int(data["cfbet"])
		coinflip_rate = int(data["cfrate"])
		daily = data["daily"]
		gem = data["gem"]
		sleep = data["sleep"]
		webhook = data["webhook"]
		spam = ["owo","uwu"]
		side = ["h","t"]
		channel = ""
		channel_amount = 0
		channel_name = ""
		run = True
		run1time = True
		daily_wait_time = 0
		gem_check = True
		gem_recheck = True
		gem_amount = 0
		grind_amount = 0
		quote_amount = 0
		benefit_amount = 0
		current_slot_bet = slot_bet
		current_coinflip_bet = coinflip_bet
		OwOID = "408785106942164992"
		user_id = ""
		user_name = ""
		guild_id = ""
		legendary_list = ['gdeer', 'gfox', 'glion', 'gowl', 'gsquid']
		gem_list = ['gcamel', 'gfish', 'gpanda', 'gshrimp', 'gspider']
		fabled_list = ['dboar', 'deagle', 'dfrog', 'dgorilla', 'dwolf']
		distored_list = ['glitchflamingo', 'glitchotter', 'glitchparrot', 'glitchraccoon', 'glitchzebra']
		hidden_list = ['hkoala', 'hlizard','hmonkey', 'hsnake', 'hsquid']

#Change Prefix Style
prefix = client.prefix

#Get The First Channel
client.channel = random.choice(client.allchannel)

#Get Mumber Of Channel
for amount in client.allchannel:
	client.channel_amount += 1

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

#Log Time
def logtime():
	return f'\033[104m{strftime("%H:%M:%S", localtime())}\033[0m'

#Run Time In Discord
def runtime_discord():
	runtime = time.time() - start_time
	return f'{strftime("**__%H__h** **__%M__m** **__%S__s**",time.gmtime(runtime))}'

#Run Time In Cmd
def runtime_cmd():
	runtime = time.time() - start_time
	return f'{strftime("%H:%M:%S",time.gmtime(runtime))}'

#Sign In
bot = discum.Client(token=client.token, log=False, build_num=0, x_fingerprint="None", user_agent=[
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36/PAsMWa7l-11',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.7.2) Gecko/20100101 / Firefox/60.7.2'])

#Send Webhook
def webhook(message):
	webhook = DiscordWebhook(url = client.webhook, content=message)
	webhook = webhook.execute()

#Get Messages
def getMessages(num: int = 1, channel: str = client.channel):
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

#Log In
@bot.gateway.command
def on_ready(resp):
	if resp.event.ready_supplemental:
		if client.run1time == True:
			user = bot.gateway.session.user
			client.user_id = user['id']
			client.user_name = user['username']
			client.guild_id = bot.getChannel(client.channel).json()['guild_id']
			channels = bot.gateway.session.guild(client.guild_id).channels
			for i in channels:
				if channels[i]['type'] == "guild_text" and channels[i]['id'] == client.channel:
					client.channel_name = channels[i]['name']
			print()
			print(f"""{color.blue}    █▀█ █ █ █ █▀█
    █▄█ ▀▄▀▄▀ █▄█{color.reset}""")
			print(f"{color.red}Logged in as{color.reset} {color.bold}{client.user_name}{color.reset}")
			print()
			try:
				webhook(f"**🏠 | I\'ll Start Working At Channel __<#{client.channel}>__**")
			except:
				pass
			print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.purple}[INFO] I\'ll Start Working At Channel{color.reset} {color.bold}{client.channel_name}{color.reset}")
			run()

#Check Problems
@bot.gateway.command
def checking(resp):
	if resp.event.message:
		m = resp.parsed.auto()
		if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
			#Captcha
			if '⚠' in m['content'] or 'real human' in m['content'] or 'https://owobot.com/captcha' in m['content']:
				try:
					webhook(f"""** 🔢 | Are You A Real Human?
<:blank:427371936482328596> | Solve Captcha Within 10 Minutes __<@{client.user_id}>__
<:blank:427371936482328596> | https://discord.com/channels/{client.guild_id}/{m['channel_id']}/{m['id']} **""")
				except:
					pass
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.red}[INFO] !!! Captcha Appear !!!{color.reset}")
				bot.gateway.close()
			#Banned
			if 'You have been banned' in m['content']:
				try:
					webhook(f"""** 💀 | You Have Been Banned!
<:blank:427371936482328596> | Check The Truth __<@{client.user_id}>__
<:blank:427371936482328596> | https://discord.com/channels/{client.guild_id}/{m['channel_id']}/{m['id']} **""")
				except:
					pass
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.red}[INFO] !!! YOU HAVE BEEN BANNED !!!{color.reset}")
				bot.gateway.close()
			#Cowoncy
			if 'don\'t have enough cowoncy!' in m['content']:
				try:
					webhook(f"""** 💸 | You\'ve Run Out Of Cowoncy!
<:blank:427371936482328596> | Sell Your Zoo To Continue __<@{client.user_id}>__**""")
				except:
					pass
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.red}[INFO] !!! You\'ve Run Out Of Cowoncy !!!{color.reset}")
				bot.gateway.close()
			#Gem
			if client.nickname in m['content'] and client.run and client.gem and client.gem_check:
				if "and caught" in m['content']:
					gem()
			#Pet
			if client.nickname in m['content'] and client.run:
				if "🌱" in m['content']:
					filter = m['content'].split("**|**")
					hunt = filter[0]
					pet = findall(r':(.*?):', hunt)
					#Legendary Pet
					for i in range(len(client.legendary_list)):
						if client.legendary_list[i] in pet:
							try:
								webhook(f"""**<a:legendary:417955061801680909> | I\`ve Just Found A Legendary Pet
<:blank:427371936482328596> | https://discord.com/channels/{client.guild_id}/{m['channel_id']}/{m['id']} **""")
							except:
								pass
							print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.orange}[INFO] I\'ve Just Found A Legendary Pet{color.reset}")
							break
					#Gem Pet
					for i in range(len(client.gem_list)):
						if client.gem_list[i] in pet:
							try:
								webhook(f"""**<a:gem:510023576489951232> | I\`ve Just Found A Gem Pet
<:blank:427371936482328596> | https://discord.com/channels/{client.guild_id}/{m['channel_id']}/{m['id']} **""")
							except:
								pass
							print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.green}[INFO] I\'ve Just Found A Gem Pet{color.reset}")
							break
					#Fabled Pet
					for i in range(len(client.fabled_list)):
						if client.fabled_list[i] in pet:
							try:
								webhook(f"""**<a:fabled:438857004493307907> | I\`ve Just Found A Fabled Pet
<:blank:427371936482328596> | https://discord.com/channels/{client.guild_id}/{m['channel_id']}/{m['id']} **""")
							except:
								pass
							print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.cyan}[INFO] I\`ve Just Found A Fabled Pet{color.reset}")
							break
					#Distored Pet
					for i in range(len(client.distored_list)):
						if client.distored_list[i] in pet:
							try:
								webhook(f"""**<a:distorted:728812986147274835> | I\`ve Just Found A Distorted Pet
<:blank:427371936482328596> | https://discord.com/channels/{client.guild_id}/{m['channel_id']}/{m['id']} **""")
							except:
								pass
							print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.red}[INFO] I\`ve Just Found A Distored Pet{color.reset}")
							break
					#Hidden Pet
					for i in range(len(client.hidden_list)):
						if client.hidden_list[i] in pet:
							try:
								webhook(f"""**<a:hidden:459203677438083074> | I\`ve Just Found A Hidden Pet
<:blank:427371936482328596> | https://discord.com/channels/{client.guild_id}/{m['channel_id']}/{m['id']} **""")
							except:
								pass
							print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.purple}[INFO] I\`ve Just Found A Hidden Pet{color.reset}")
							break

#Check Status Slot
@bot.gateway.command
def check_slot(resp):
	if client.run and client.slot:
		if resp.event.message_updated:
			m = resp.parsed.auto()
			try:
				if client.nickname in m['content'] and m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
					#Lost
					if 'won nothing' in m['content']:
						print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.red}[INFO] Slot Lost {client.current_slot_bet} Cowoncy{color.reset}")
						client.benefit_amount -= client.current_slot_bet
						client.current_slot_bet *= client.slot_rate
					#Draw
					if '<:eggplant:417475705719226369> <:eggplant:417475705719226369> <:eggplant:417475705719226369>' in m['content']:
						print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.bold}[INFO] Slot Drew{color.reset}")
					#Won x2
					if '<:heart:417475705899712522> <:heart:417475705899712522> <:heart:417475705899712522>' in m['content']:
						print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.green}[INFO] Slot Won {client.current_slot_bet} Cowoncy (x2){color.reset}")
						client.benefit_amount += client.current_slot_bet
						client.current_slot_bet = client.slot_bet
					#Won x3
					if '<:cherry:417475705178161162> <:cherry:417475705178161162> <:cherry:417475705178161162>' in m['content']:
						print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.green}[INFO] Slot Won {client.current_slot_bet * 2} Cowoncy (x3){color.reset}")
						client.benefit_amount += client.current_slot_bet * 2
						client.current_slot_bet = client.slot_bet
					#Won x4
					if '<:cowoncy:417475705912426496> <:cowoncy:417475705912426496> <:cowoncy:417475705912426496>' in m['content']:
						print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.green}[INFO] Slot Won {client.current_slot_bet * 3} Cowoncy (x4){color.reset}")
						client.benefit_amount += client.current_slot_bet * 3
						client.current_slot_bet = client.slot_bet
					#Won x10
					if '<:o_:417475705899843604> <:w_:417475705920684053> <:o_:417475705899843604>' in m['content']:
						print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.green}[INFO] Slot Won {client.current_slot_bet * 9} Cowoncy (x10){color.reset}")
						client.benefit_amount += client.current_slot_bet * 9
						client.current_slot_bet = client.slot_bet
			except KeyError:
				pass

#Check Status Coinflip
@bot.gateway.command
def check_coinflip(resp):
	if client.run and client.coinflip:
		if resp.event.message_updated:
			m = resp.parsed.auto()
			try:
				if client.nickname in m['content'] and m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
					#Lost
					if 'you lost' in m['content']:
						print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.red}[INFO] Coinflip Lost {client.current_coinflip_bet} Cowoncy{color.reset}")
						client.benefit_amount -= client.current_coinflip_bet
						client.current_coinflip_bet *= client.coinflip_rate
					#Won
					if 'you won' in m['content']:
						print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.green}[INFO] Coinflip Won {client.current_coinflip_bet} Cowoncy{color.reset}")
						client.benefit_amount += client.current_coinflip_bet
						client.current_coinflip_bet = client.coinflip_bet
			except KeyError:
				pass

#Send Grind
def grind():
	if client.run and client.owo:
		spam = random.choice(client.spam)
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), f"{spam}")
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {spam}{color.reset}")
		sleep(random.randint(1, 2))
	if client.run and client.grind:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), f"{prefix}h")
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}h{color.reset}")
		sleep(random.randint(1, 2))
	if client.run and client.gem and client.gem_check:
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I'm Checking Gem Status{color.reset}")
	if client.run and client.grind:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), f"{prefix}b")
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}b{color.reset}")
		client.grind_amount += 1
		sleep(random.randint(1, 2))

#Send Quote
def quote():
	if client.quote and client.run:
		try:
			response = get("https://zenquotes.io/api/random")
			if response.status_code == 200:
				json_data = response.json()
				data = json_data[0]
				bot.typingAction(client.channel)
				bot.sendMessage(client.channel, data['q'])
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] Quote{color.reset}")
				client.quote_amount += 1
				sleep(random.randint(1, 2))
		except:
			pass

#Play Slot
def slot():
	if client.current_slot_bet  > 250000:
		client.current_slot_bet = client.slot_bet
	if client.run and client.slot:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), f"{prefix}s {client.current_slot_bet}")
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}s {client.current_slot_bet}{color.reset}")
		sleep(random.randint(1, 2))

#Play Coinflip
def coinflip():
	if client.current_coinflip_bet  > 250000:
		client.current_coinflip_bet = client.coinflip_bet
	if client.run and client.coinflip:
		side = random.choice(client.side)
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), f"{prefix}cf {client.current_coinflip_bet} {side}")
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}cf {client.current_coinflip_bet} {side}{color.reset}")
		sleep(random.randint(1, 2))

#Change Channel
def change():
	if client.run and client.channel_amount > 1:
		client.channel = random.choice(client.allchannel)
		channels = bot.gateway.session.guild(client.guild_id).channels
		for i in channels:
			if channels[i]['type'] == "guild_text" and channels[i]['id'] == client.channel:
				client.channel_name = channels[i]['name']
		try:
			webhook(f"**🏠 | I Changed Channel To __<#{client.channel}>__**")
		except:
			pass
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.purple}[INFO] I Changed Channel To{color.reset} {color.bold}{client.channel_name}{color.reset}")

#Daily
def daily():
	if client.run and client.daily:
		bot.typingAction(client.channel)
		sleep(random.randint(3, 5))
		bot.sendMessage(client.channel, f"{prefix}daily")
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}daily{color.reset}")
		daily_messages = getMessages(num=5)
		daily_string = ""
		length = len(daily_messages)
		i = 0
		while i < length:
			if daily_messages[i]['author']['id']==client.OwOID and daily_messages[i]['content'] != "" and "Nu" or "daily" in daily_messages[i]['content']:
				daily_string = daily_messages[i]['content']
				i = length
			else:
				i += 1
		if not daily_string:
			sleep(random.randint(1, 2))
			daily()
		else:
			if "Nu" in daily_string:
				daily_string = findall('[0-9]+', daily_string)
				client.daily_wait_time = str(int(daily_string[0]) * 3600 + int(daily_string[1]) * 60 + int(daily_string[2]))
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.orange}[INFO] You Can Claim Daily After{color.reset} {color.bold}{str(timedelta(seconds=int(client.daily_wait_time)))} Seconds{color.reset}")
			elif "Your next daily" in daily_string:
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.orange}[INFO] I Claimed Daily!{color.reset}")

#Use Gem
def gem():
	#Check Gem
	if client.run and client.gem and client.gem_check:
		bot.typingAction(client.channel)
		sleep(random.randint(3, 5))
		bot.sendMessage(str(client.channel), f"{prefix}inv")
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}inv{color.reset}")
		gem_messages = bot.getMessages(str(client.channel), num=5)
		gem_messages = gem_messages.json()
		inv = ""
		for i in range(len(gem_messages)):
			if gem_messages[i]['author']['id'] == client.OwOID and 'Inventory' in gem_messages[i]['content']:
				inv = findall(r'`(.*?)`', gem_messages[i]['content'])
		#Check Again
		if not inv:
			sleep(random.randint(1, 2))
			gem()
		else:
			#Common 051 065 072
			if "051" in inv and "065" in inv and "072" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), f"{prefix}use 51 65 72")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}use 51 65 72{color.reset}")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I Used{color.reset} {color.red}Common Gem{color.reset} {color.gray}For 25 Turns{color.reset}")
				client.gem_amount += 1
				client.gem_recheck = True
			#Uncommon 052 066 073
			elif "052" in inv and "066" in inv and "073" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), f"{prefix}use 52 66 73")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}use 52 66 73{color.reset}")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I Used{color.reset} {color.cyan}Uncommon Gem{color.reset} {color.gray}For 25 Turns{color.reset}")
				client.gem_amount += 1
				client.gem_recheck = True
			#Rare 053 067 074
			elif "053" in inv and "067" in inv and "074" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), f"{prefix}use 53 67 74")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}use 53 67 74{color.reset}")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I Used{color.reset} {color.orange}Rare Gem{color.reset} {color.gray}For 50 Turns{color.reset}")
				client.gem_amount += 1
				client.gem_recheck = True
			#Epic 054 068 075
			elif "054" in inv and "068" in inv and "075" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), f"{prefix}use 54 68 75")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}use 54 68 75{color.reset}")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I Used{color.reset} {color.blue}Epic Gem{color.reset} {color.gray}For 75 Turns{color.reset}")
				client.gem_amount += 1
				client.gem_recheck = True
			#Mythical 055 069 076
			elif "055" in inv and "069" in inv and "076" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), f"{prefix}use 55 69 76")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}use 55 69 76{color.reset}")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I Used{color.reset} {color.purple}Mythical Gem{color.reset} {color.gray}For 75 Turns{color.reset}")
				client.gem_amount += 1
				client.gem_recheck = True
			#Legendary 056 070 077
			elif "056" in inv and "070" in inv and "077" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), f"{prefix}use 56 70 77")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}use 56 70 77{color.reset}")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I Used{color.reset} {color.yellow}Legendary Gem{color.reset} {color.gray}For 100 Turns{color.reset}")
				client.gem_amount += 1
				client.gem_recheck = True
			#Fabled 057 071 078
			elif "057" in inv and "071" in inv and "078" in inv:
				bot.typingAction(client.channel)
				bot.sendMessage(str(client.channel), f"{prefix}use 57 71 78")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.yellow}[SENT] {prefix}use 57 71 78{color.reset}")
				print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I Used{color.reset} {color.cyan}Fabled Gem{color.reset} {color.gray}For 100 Turns{color.reset}")
				client.gem_amount += 1
				client.gem_recheck = True
			else:
				#Check Gem Again
				if client.gem_recheck:
					print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.gray}[INFO] I\'ll Check Your Inventory Again{color.reset}")
					client.gem_recheck = False
					gem()
				#Don't Have Enough Gems
				else:
					try:
						webhook(f"**❌ | You Don't Have Enough Gems!**")
					except:
						pass
					print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.red}[INFO] You Don't Have Enough Gems!{color.reset}")
					client.gem_check = False
					client.gem_recheck = False

#Sleep
def die():
	if client.run and client.sleep:
		die = random.randint(300, 600)
		try:
			webhook(f"**🛌 | I'm Taking A Break For __{die} Seconds__**")
		except:
			pass
		print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.cyan}[INFO] I'm Taking A Break For{color.reset} {color.bold}{die} Seconds{color.reset}")
		sleep(die)

#Run
def run():
	client.run1time = False
	grind_time = 0
	quote_time = 0
	slot_time = 0
	coinflip_time = 0
	daily_time = 0
	change_time = time.time()
	sleep_time = time.time()
	grind_spam = 0
	quote_spam = 0
	slot_spam = 0
	coinflip_spam = 0
	change_spam = random.randint(600, 1200)
	sleep_spam = random.randint(600, 1200)
	while client.run:
		#Grind
		if time.time() - grind_time > grind_spam and client.grind:
			grind_time = time.time()
			grind_spam = random.randint(17, 25)
			grind()
		#Quote
		if time.time() - quote_time > quote_spam and client.quote:
			quote_time = time.time()
			quote_spam = random.randint(30, 60)
			quote()
		#Slot
		if time.time() - slot_time > slot_spam and client.slot:
			slot_time = time.time()
			slot_spam = random.randint(20, 30)
			slot()
		#Coinflip
		if time.time() - coinflip_time > coinflip_spam and client.coinflip:
			coinflip_time = time.time()
			coinflip_spam = random.randint(20, 30)
			coinflip()
		#Change
		if time.time() - change_time > change_spam and client.channel_amount > 1:
			change_time = time.time()
			change_spam = random.randint(600, 1200)
			change()
		#Daily
		if time.time() - daily_time > int(client.daily_wait_time) and client.sleep:
			daily()
			daily_time = time.time()
		#Sleep
		if time.time() - sleep_time > sleep_spam and client.sleep:
			die()
			sleep_time = time.time()
			sleep_spam = random.randint(600, 1200)
			try:
				webhook(f"**🌄 | Done! I'll Work For __{sleep_spam} Seconds__**")
			except:
				pass
			print(f"{logtime()} - {color.blue}{client.user_name}{color.reset} - {color.cyan}[INFO] Done! I'll Work For{color.reset} {color.bold}{sleep_spam} Seconds{color.reset}")
		sleep(1)

bot.gateway.run()

@atexit.register
def problem():
	client.run = False
	try:
		startfile('music.mp3')
	except:
		pass
	print()
	try:
		webhook(f"""I Worked For {runtime_discord()} With:
💎 **|** Gem: __**{client.gem_amount}**__ Sets
🎯 **|** Grind: __**{client.grind_amount}**__ Times
✏️ **|** Send: __**{client.quote_amount}**__ Quotes
💵 **|** Gamble: __**{client.benefit_amount}**__ Cowoncy
""")
	except:
		pass
	print(f"{color.cyan}I Worked For{color.reset} {color.bold}{runtime_cmd()}{color.reset} {color.cyan}With:{color.reset}")
	print(f"    {color.green}Gem:{color.reset}    {color.bold}{client.gem_amount} Sets{color.reset}")
	print(f"    {color.green}Grind:{color.reset}  {color.bold}{client.grind_amount} Times{color.reset}")
	print(f"    {color.green}Quote:{color.reset}  {color.bold}{client.quote_amount} Quotes{color.reset}")
	print(f"    {color.green}Gamble:{color.reset} {color.bold}{client.benefit_amount} Cowoncy{color.reset}")
	problem = input(f"{color.blue}Enter 'OK' to Reset: {color.reset}")
	if problem.lower() == 'ok':
		system('python "main.py"')
