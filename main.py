#!/usr/bin/python
import discum
from requests import get
from discord_webhook import DiscordWebhook
from os import system
import time
start_time = time.time()
from time import sleep, strftime, localtime
import random
import atexit
import json
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
		cfbet = int(data["cfbet"])
		cfrate = int(data["cfrate"])
		slot = data["slot"]
		sbet = int(data["sbet"])
		srate = int(data["srate"])
		command = data["command"]
		owner = data["owner"]
		webhook = data["webhook"]
		link = data["link"]
		ping = data["ping"]
		uwu = ["owo","uwu"]
		side = ["h","t"]
		stopped = False
		run = True
		owo_amount = 0
		grind_amount = 0
		quote_amount = 0
		benefit_amount = 0
		current_cfbet = cfbet
		current_sbet = sbet
		OwOID = "408785106942164992"
		owo_status = '❌'
		grind_status = '❌'
		quote_status = '❌'
		coinflip_status = '❌'
		slot_status = '❌'
		command_status = '❌'
		webhook_status = '❌'

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

#Status
if client.owo:
	client.owo_status = '✅'
if client.grind:
	client.grind_status = '✅'
if client.quote:
	client.quote_status = '✅'
if client.coinflip:
	client.coinflip_status = '✅'
if client.slot:
	client.slot_status = '✅'
if client.command:
	client.command_status = '✅'
if client.webhook:
	client.webhook_status = '✅'

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
		input("Press Enter to continue...")
		print("""{}    █▀█ █ █ █ █▀█{}""".format(color.blue, color.reset))
		print("""{}    █▄█ ▀▄▀▄▀ █▄█{}""".format(color.blue, color.reset))
		print("{}Logged in as {}{}{}{}".format(color.red, color.reset, color.bold, user['username'], color.reset))
		print()
		start()
		
#Webhook
def webhook(message):
	webhook = DiscordWebhook(url = client.link, content=message)
	webhook = webhook.execute()

#Captcha Bypass
@bot.gateway.command
def check(resp):
	if resp.event.message:
		m = resp.parsed.auto()
		if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
			if '⚠' in m['content'] or 'real human' in m['content'] or 'https://owobot.com/captcha' in m['content'] or 'don\'t have enough cowoncy!' in m['content']:
				client.stopped = True

#Coinflip Check
@bot.gateway.command
def cfcheck(resp):
	if not client.stopped and client.coinflip and client.run:
		if resp.event.message_updated:
			m = resp.parsed.auto()
			try:
				if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
					if 'you lost' in m['content']:
						print("{} {}[INFO] Coinflip Lost {} Cowoncy{}".format(timelog(), color.red, client.current_cfbet, color.reset))
						client.benefit_amount -= client.current_cfbet
						client.current_cfbet *= client.cfrate
					if 'you won' in m['content']:
						print("{} {}[INFO] Coinflip Won {} Cowoncy{}".format(timelog(), color.green, client.current_cfbet, color.reset))
						client.benefit_amount += client.current_cfbet
						client.current_cfbet = client.cfbet
			except KeyError:
				pass

#Slot Check
@bot.gateway.command
def scheck(resp):
	if not client.stopped and client.slot and client.run:
		if resp.event.message_updated:
			m = resp.parsed.auto()
			try:
				if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
					if 'won nothing' in m['content']:
						print("{} {}[INFO] Slot Lost {} Cowoncy{}".format(timelog(), color.red, client.current_sbet, color.reset))
						client.benefit_amount -= client.current_sbet
						client.current_sbet *= client.srate
					if '<:eggplant:417475705719226369> <:eggplant:417475705719226369> <:eggplant:417475705719226369>' in m['content']:
						print("{} {}[INFO] Slot Draw{}".format(timelog(), color.bold, color.reset))
					if '<:heart:417475705899712522> <:heart:417475705899712522> <:heart:417475705899712522>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x2){}".format(timelog(), color.green, client.current_sbet, color.reset))
						client.benefit_amount += client.current_sbet
						client.current_sbet = client.sbet
					if '<:cherry:417475705178161162> <:cherry:417475705178161162> <:cherry:417475705178161162>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x3){}".format(timelog(), color.green, client.current_sbet * 2, color.reset))
						client.benefit_amount += client.current_sbet * 2
						client.current_sbet = client.sbet
					if '<:cowoncy:417475705912426496> <:cowoncy:417475705912426496> <:cowoncy:417475705912426496>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x4){}".format(timelog(), color.green, client.current_sbet * 3, color.reset))
						client.benefit_amount += client.current_sbet * 3
						client.current_sbet = client.sbet
					if '<:o_:417475705899843604> <:w_:417475705920684053> <:o_:417475705899843604>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x10){}".format(timelog(), color.green, client.current_sbet * 9, color.reset))
						client.benefit_amount += client.current_sbet * 9
						client.current_sbet = client.sbet
			except KeyError:
				pass

#Command
@bot.gateway.command
def command(resp):
	if client.command:
		if resp.event.message:
			m = resp.parsed.auto()
			if m['author']['id'] == bot.gateway.session.user['id'] or m['author']['id'] == client.owner:
				#Help
				if m['content'].startswith(f"help"):
					bot.sendMessage(str(m['channel_id']), """
I have **__5__ Commands**:

> **`send`** + **`text`**
> **`setting`**
> **`stat`**
> **`start`**
> **`stop`**
""")
					print("{} {}[SELF] Help List{}".format(timelog(), color.gray, color.reset))
				#Send
				if m['content'].startswith(f"say"):
					message = m['content'].replace(f'say ', '')
					bot.sendMessage(str(m['channel_id']), message)
					print("{} {}[SELF] Say {}{}".format(timelog(), color.gray, message, color.reset))
				#Setting
				if m['content'].startswith(f"setting"):
					bot.sendMessage(str(m['channel_id']),
					"""
> __**OwO**__・{}
> __**Grind**__・{}
> __**Quote**__・{}
> __**Coinflip**__・{}
> __**Slot**__・{}
> __**Command**__・{}
> __**Webhook**__・{}
""".format(client.owo_status, client.grind_status, client.quote_status, client.coinflip_status, client.slot_status, client.command_status, client.webhook_status))
					print("{} {}[SELF] Setting{}".format(timelog(), color.gray, color.reset))
				#Stat
				if m['content'].startswith(f"stat"):
					bot.sendMessage(str(m['channel_id']),
					"""
I ran for {} with:
> Spamming __**{}**__ OwO 🐮
> Grinding __**{}**__ times 🎯
> Sending __**{}**__ quotes ✏️
> Gambling __**{}**__ cowoncys 💵
""".format(timerun(), client.grind_amount, client.quote_amount, client.benefit_amount))
					print("{} {}[SELF] Stat{}".format(timelog(), color.gray, color.reset))
				#Start
				if m['content'].startswith(f"start"):
					client.run = True
					bot.sendMessage(str(m['channel_id']), "> **Starting... 🔔**")
					print("{} {}[SELF] Start Selfbot{}".format(timelog(), color.gray, color.reset))
				#Stop
				if m['content'].startswith(f"stop"):
					client.run = False
					bot.sendMessage(str(m['channel_id']), "> **Stopping... 🚨**")
					print("{} {}[SELF] Stop Selfbot{}".format(timelog(), color.gray, color.reset))

#OwO
def owo():
	if not client.stopped and client.owo and client.run:
		owo = random.choice(client.uwu)
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}".format(owo))
		print("{} {}[SENT] {}{}".format(timelog(), color.yellow, owo, color.reset))
		client.owo_amount += 1

#Grind
def grind():
	if not client.stopped and client.grind and client.run:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}h".format(prefix))
		print("{} {}[SENT] {}h{}".format(timelog(), color.yellow, prefix, color.reset))
	if not client.stopped and client.grind and client.run:
		sleep(random.randint(1, 2))
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}b".format(prefix))
		print("{} {}[SENT] {}b{}".format(timelog(), color.yellow, prefix, color.reset))
		client.grind_amount += 1

#Quote
def quote():
	if not client.stopped and client.quote and client.run:
		try:	
			response = get("https://zenquotes.io/api/random")
			if response.status_code == 200:
				json_data = response.json()
				data = json_data[0]
				bot.sendMessage(client.channel, data['q'])
				print("{} {}[SENT] Quote{}".format(timelog(), color.yellow, color.reset))
				client.quote_amount += 1
		except:
			pass

#Coinflip
def cf():
	if client.current_cfbet  > 250000:
		client.current_cfbet = client.cfbet
	if not client.stopped and client.coinflip and client.run:
		side = random.choice(client.side)
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}cf {} {}".format(prefix, client.current_cfbet, side))
		print("{} {}[SENT] {}cf {} {}{}".format(timelog(), color.yellow, prefix, client.current_cfbet, side, color.reset))

#Slot
def s():
	if client.current_sbet  > 250000:
		client.current_sbet = client.sbet
	if not client.stopped and client.slot and client.run:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "{}s {}".format(prefix, client.current_sbet))
		print("{} {}[SENT] {}s {}{}".format(timelog(), color.yellow, prefix, client.current_sbet, color.reset))

#Run
def start():
	change = 0
	time1 = 0
	time2 = 0
	time3 = 0
	time4 = 0
	time5 = 0
	while True:
		if client.stopped:
			bot.gateway.close()
		if not client.stopped and client.run:
			if time.time() - change > 60:
				run1 = random.randint(10, 15)
				run2 = random.randint(15, 20)
				run3 = random.randint(30, 60)
				run4 = random.randint(15, 25)
				run5 = random.randint(15, 25)
			if time.time() - time1 > run1:
				owo()
				time1 = time.time()
			if time.time() - time2 > run2:
				grind()
				time2 = time.time()
			if time.time() - time3 > run3:
				quote()
				time3 = time.time()
			if time.time() - time4 > run4:
				cf()
				time4 = time.time()
			if time.time() - time5 > run5:
				s()
				time5 = time.time()

bot.gateway.run()

#Exit
@atexit.register
def exit():
	client.stopped = True
	try:
		startfile('music.mp3')
	except:
		pass
	if client.webhook:
		webhook(f"**<a:pepeintelligent:964835071595008000> I Found Some Problem In <#{client.channel}> <@{client.ping}>**")
		webhook(f"**<a:1096324489022808094:1098237958324236388> I Found Some Problem In <#{client.channel}> <@{client.ping}>**")
		webhook(f"**<a:quay:1086553810220089374> I Found Some Problem In <#{client.channel}> <@{client.ping}>**")
	bot.switchAccount(client.token[:-4] + 'FvBw')
	print("{} {}[INFO] I Found Some Problem".format(timelog(), color.red, color.reset))
	print()
	print("    {}Spam:{}   {}{} OwO {}".format(color.green, color.reset, color.bold, client.owo_amount, color.reset))
	print("    {}Grind:{}  {}{} Times {}".format(color.green, color.reset, color.bold, client.grind_amount, color.reset))
	print("    {}Quote:{}  {}{} Quotes {}".format(color.green, color.reset, color.bold, client.quote_amount, color.reset))
	print("    {}Gamble:{} {}{} Cowoncys {}".format(color.green, color.reset, color.bold, client.benefit_amount, color.reset))
	exit = input("{}Enter 'OK' to Reset: {}".format(color.blue, color.reset))
	if exit == 'OK':
		system('python "main.py"')
