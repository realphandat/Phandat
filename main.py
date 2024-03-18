import json
import discord
import aiohttp
import asyncio
from discord.ext import tasks
import os
from requests import get
import random
from re import findall
from datetime import timedelta
from time import time
from discord import Webhook
from datetime import timedelta
import time
start_time = time.time()
from twocaptcha import TwoCaptcha
from aiohttp import ClientSession, CookieJar
from time import strftime, localtime
from base64 import b64encode

#Collect Data From Config
class data:
	def __init__(self):
		with open("config.json", "r") as file:
			data = json.load(file)
			self.token = data["token"]
			self.twocaptcha = data["twocaptcha"]
			self.all_channel = data["channel"]
			self.prefix = data["prefix"]
			self.fun = data["fun"]
			self.owo = data["owo"]
			self.grind = data["grind"]
			self.quote = data["quote"]
			self.slot = data["slot"]
			self.slot_bet = int(data["sbet"])
			self.slot_rate = int(data["srate"])
			self.coinflip = data["coinflip"]
			self.coinflip_bet = int(data["cfbet"])
			self.coinflip_rate = int(data["cfrate"])
			self.daily = data["daily"]
			self.gem = data["gem"]
			self.sleep = data["sleep"]
			self.webhook = data["webhook"]

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

#MyClient
class MyClient(discord.Client, data):
	def __init__(self, *args, **kwargs):
		discord.Client.__init__(self, *args, **kwargs)
		super().__init__(*args, **kwargs)
		data.__init__(self)
		self.tasks = [
			self.check_owo_status,
			self.entertainment,
			self.start_grind,
			self.start_quote,
			self.start_slot,
			self.start_coinflip,
			self.change_channel,
			self.claim_daily,
			self.bedtime
			]
		self.OwO = ""
		self.OwOID = 408785106942164992
		self.owo_status = True
		self.nickname = ""
		self.channel = ""
		self.channel_id = random.choice(self.all_channel)
		self.channel_amount = 0
		for self.amount in self.all_channel:
			self.channel_amount += 1
		self.work = True
		self.work1time = True
		self.runn = True
		self.pup = True
		self.piku = True
		self.daily_time = 0
		self.work_time = random.randint(600, 1200)
		self.gem_check = True
		self.gem_recheck = True
		self.captcha_amount = 0
		self.gem_amount = 0
		self.benefit_amount = 0
		self.current_slot_bet = self.slot_bet
		self.current_coinflip_bet = self.coinflip_bet
		self.legendary_list = ["gdeer", "gfox", "glion", "gowl", "gsquid"]
		self.gem_list = ["gcamel", "gfish", "gpanda", "gshrimp", "gspider"]
		self.fabled_list = ["dboar", "deagle", "dfrog", "dgorilla", "dwolf"]
		self.distored_list = ["glitchflamingo", "glitchotter", "glitchparrot", "glitchraccoon", "glitchzebra"]
		self.hidden_list = ["hkoala", "hlizard","hmonkey", "hsnake", "hsquid"]

	#Log Time
	async def intro(self):
		return f"{color.mark}{strftime("%H:%M:%S", localtime())}{color.reset} - {color.red}{self.nickname}{color.reset} - "

	#Run Time In Discord
	async def discord_stat(self):
		runtime = time.time() - start_time
		return f"""I Worked For {strftime("**__%H__h** **__%M__m** **__%S__s**",time.gmtime(runtime))} With:
🤖 **|** Solved __**{self.captcha_amount}**__ Captchas
💎 **|** Used Gem __**{self.gem_amount}**__ Times
📊 **|** Earned __**{self.benefit_amount}**__ Cowoncy
"""

	#Run Time In Cmd
	async def cmd_stat(self):
		runtime = time.time() - start_time
		return f"""{color.bold}I Worked For{color.reset} {color.blue}{strftime("%H:%M:%S",time.gmtime(runtime))}{color.reset} {color.bold}With:{color.reset}
    {color.bold}Solved{color.reset} {color.green}{self.captcha_amount} Captchas{color.reset}
    {color.bold}Used Gem{color.reset} {color.green}{self.gem_amount} Times{color.reset}
    {color.bold}Earned{color.reset} {color.green}{self.benefit_amount} Cowoncy{color.reset}"""

	#Stop Working
	async def goodbye(self):
		await self.worker(False)
		os.startfile('music.mp3')
		print()
		await self.send_webhooks(f"{await self.discord_stat()}")
		print(f"{await self.cmd_stat()}")
		choice = input(f"{color.yellow}Enter 'OK' to Reset: {color.reset}")
		if choice.lower() == 'ok':
			os.system('python "main.py"')

	#Send Webhooks
	async def send_webhooks(self, message):
		try:
			async with aiohttp.ClientSession() as session:
				webhook = Webhook.from_url(self.webhook, session=session)
				await webhook.send(message)
		except Exception as e:
			if str(e) == "Invalid Webhook Token":
				pass

	#Get Messages
	async def get_messages(self, message, content, includes_self=False):
		if includes_self:
			return (content.lower() in message.content.lower() and self.user.display_name in message.content)
		return content.lower() in message.content.lower()

	#Control Tasks
	async def worker(self, status):
		try:
			if status:
				self.work = True
				for task in self.tasks:
					task.start()
					await asyncio.sleep(5)
			else:
				self.work = False
				for task in self.tasks:
					task.cancel()
		except RuntimeError:
			pass

	#Get Nickname From Another Guild
	async def get_nickname(self):
		self.channel = self.get_channel(self.channel_id)
		guild = self.channel.guild
		member = await guild.fetch_member(self.user.id)
		if member.nick:
			self.nickname = member.nick
		elif not member.nick:
			self.nickname = member.display_name

	#On Ready Then Run
	async def on_ready(self):
		if self.work1time:
			self.OwO = self.get_user(self.OwOID)
			await self.get_nickname()
			await self.send_webhooks(f"**🌻 | I\'ll Start At Channel <#{self.channel_id}> For __{self.work_time}__ Seconds**")
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ll Start At Channel{color.reset} {color.purple}{self.channel}{color.reset} {color.bold}For{color.reset} {color.cyan}{self.work_time} Seconds{color.reset}")
			self.work_time += time.time()
			await self.worker(True)
			self.work1time = False

	#Solve OwO's Image Captcha
	async def solve_icaptcha(self, image, lenghth):
		solver = TwoCaptcha(**{
			'server': "2captcha.com",
			'apiKey': self.twocaptcha,
			'defaultTimeout': 300,
			'pollingInterval': 5,
		})
		balance = solver.balance()
		print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your 2Captcha API Currently Have{color.reset} {color.green}{balance}${color.reset}")
		try:
			result = solver.normal(image, numeric=2, minLen=lenghth, maxLen=lenghth, phrase=0, caseSensitive=0, calc=0, lang='en')
			await self.OwO.send(result["code"])
			await asyncio.sleep(random.randint(3, 5))
			check = None
			async for message in self.OwO.dm_channel.history(limit=1):
						if message.author.id == self.OwOID and (await self.get_messages(message, "verified") or await self.get_messages(message, "Worry")):
							check = message
			if "verified" in check.content and check.author.id == self.OwOID:
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved Image Captcha{color.reset} {color.green}Successfully!{color.reset}")
				solver.report(result['captchaId'], True)
				self.captcha_amount += 1
			elif "(2/3)" in check.content and check.author.id == self.OwOID:
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.gray}I Solved It Wrong Twice{color.reset} {color.red}!!!{color.reset}")
				solver.report(result['captchaId'], False)
				await self.goodbye()
			elif "Wrong" in check.content and check.author.id == self.OwOID:
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved Image Captcha{color.reset} {color.red}Failed!{color.reset}")
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Will Try To{color.reset} {color.red}Solve It Again!{color.reset}")
				solver.report(result['captchaId'], False)
				await self.solve_icaptcha(image, lenghth)
		except Exception as e:
			#Invalid Key
			if str(e) == "ERROR_KEY_DOES_NOT_EXIST":
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your 2Captcha API Is{color.reset} {color.red}Invalid!{color.reset}")
				await self.goodbye()
			#Out Of Money
			if str(e) == "ERROR_ZERO_BALANCE":
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your 2Captcha API Is{color.reset} {color.red}Out Of Money!{color.reset}")
				await self.goodbye()
			#Timeout
			if str(e) == "timeout 300.0 exceeded":
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Hcaptcha{color.reset} {color.red}Isn\'t Solved So Far!{color.reset}")
				await self.goodbye()

	#Sumbit Oauth To OwO's Website
	async def submit_oauth(self, res):
		response = await res.json()
		locauri = response.get("location")
		headers = {
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.5", "connection": "keep-alive",
			"host": "owobot.com",
			"referer": "https://discord.com/", "sec-fetch-dest": "document", "sec-fetch-mode": "navigate", "sec-fetch-site": "cross-site", "sec-fetch-user": "?1", "upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
		}
		session = ClientSession(cookie_jar=CookieJar())
		async with session.get(locauri, headers=headers, allow_redirects=False) as res2:
			if res2.status in (302, 307):
				return session
			else:
				print(res2.status)
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}The System Failure Occurred{color.reset} {color.red}!!!{color.reset}")
				await self.goodbye()

	#Get Oauth To Sumbit Oauth
	async def get_oauth(self):
		async with ClientSession() as session:
			oauth = "https://discord.com/api/v9/oauth2/authorize?response_type=code&redirect_uri=https%3A%2F%2Fowobot.com%2Fapi%2Fauth%2Fdiscord%2Fredirect&scope=identify%20guilds%20email%20guilds.members.read&client_id=408785106942164992"
			payload = {
				"permissions": "0",
				"authorize": True
			}
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
				'Accept': '*/*',
				'Accept-Language': 'en-US,en;q=0.5',
				'Accept-Encoding': 'gzip, deflate, br',
				'Content-Type': 'application/json',
				'Authorization': self.token,
				'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExMS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTg3NTk5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
				'X-Debug-Options': 'bugReporterEnabled',
				'Origin': 'https://discord.com',
				'Connection': 'keep-alive',
				'Referer': "https://discord.com//oauth2/authorize?response_type=code&redirect_uri=https%3A%2F%2Fowobot.com%2Fapi%2Fauth%2Fdiscord%2Fredirect&scope=identify%20guilds%20email%20guilds.members.read&client_id=408785106942164992",
				'Sec-Fetch-Dest': 'empty',
				'Sec-Fetch-Mode': 'cors',
				'Sec-Fetch-Site': 'same-origin',
				'TE': 'trailers',
			}
			async with session.post(oauth, headers=headers, json=payload) as res:
				if res.status == 200:
					result_session = await self.submit_oauth(res)
					return result_session
				else:
					print(await res.text())
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}The System Failure Occurred{color.reset} {color.red}!!!{color.reset}")
					await self.goodbye()

	#Solve OwO's HCaptcha
	async def solve_hcaptcha(self):
		solver = TwoCaptcha(**{
			'server': "2captcha.com",
			'apiKey': self.twocaptcha,
			'defaultTimeout': 300,
			'pollingInterval': 5,
		})
		balance = solver.balance()
		print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your 2Captcha API Currently Have{color.reset} {color.green}{balance}${color.reset}")
		try:
			result = solver.hcaptcha(sitekey='a6a1d5ce-612d-472d-8e37-7601408fbc09', url="https://owobot.com/captcha")
			headers = {
				"Accept": "application/json, text/plain, */*",
				"Accept-Encoding": "gzip, deflate, br",
				"Accept-Language": "en-US;en;q=0.8",
				"Content-Type": "application/json;charset=UTF-8",
				"Origin": "https://owobot.com",
				"Referer": "https://owobot.com/captcha",
				'Sec-Fetch-Dest': 'empty',
				'Sec-Fetch-Mode': 'cors',
				'Sec-Fetch-Site': 'same-origin',
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
			}
			async with (await self.get_oauth()) as session:
				cookies = {cookie.key: cookie.value for cookie in session.cookie_jar}
				async with session.post("https://owobot.com/api/captcha/verify",
										headers=headers,
										json={
											"token": result["code"]
										},
										cookies=cookies) as res:
					if res.status == 200:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved Hcaptcha{color.reset} {color.green}Successfully!{color.reset}")
						solver.report(result['captchaId'], True)
						self.captcha_amount += 1
						await self.worker(True)
					else:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved Hcaptcha{color.reset} {color.red}Failed!{color.reset}")
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Will Try To{color.reset} {color.red}Solve It Again!{color.reset}")
						solver.report(result['captchaId'], False)
						await self.solve_hcaptcha()
		except Exception as e:
			#Invalid Key
			if str(e) == "ERROR_KEY_DOES_NOT_EXIST":
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your 2Captcha API Is{color.reset} {color.red}Invalid!{color.reset}")
				await self.goodbye()
			#Out Of Money
			if str(e) == "ERROR_ZERO_BALANCE":
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your 2Captcha API Is{color.reset} {color.red}Out Of Money!{color.reset}")
				await self.goodbye()
			#Timeout
			if str(e) == "timeout 300.0 exceeded":
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Hcaptcha{color.reset} {color.red}Isn\'t Solved So Far!{color.reset}")
				await self.goodbye()

	#Collect All Sent Messages
	async def on_message(self, message):
		#Someone Challenges You
		if f"<@{self.user.id}>" in message.content and self.work and message.author.id == self.OwOID:
			embeds = message.embeds
			for embed in embeds:
				if "owo ab" in embed.description and "owo db" in embed.description:
					await self.send_webhooks(f"""**🥊 | Someone Challenges You!
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Someone{color.reset} {color.red}Challenges{color.reset} {color.bold}You!{color.reset}")
					choice = random.choice([1, 2])
					await asyncio.sleep(random.randint(3, 5))
					if choice == 1:
						await message.channel.typing()
						await message.channel.send(f"{self.prefix}ab")
					if choice == 2:
						components = message.components
						firstButton = components[0].children[0]
						await firstButton.click()
		#Check User's Problems
		if f"<@{self.user.id}>" in message.content or self.nickname in message.content or self.user.display_name in message.content and self.work and message.author.id == self.OwOID:
			#Check Captcha
			if "⚠" in message.content and "letter word" in message.content or "https://owobot.com/captcha" in message.content:
				await self.send_webhooks(f"""**🔢 | Are You A Real Human?
<:blank:427371936482328596> | Solve Captcha Within 10 Minutes <@{self.user.id}>
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
				await self.worker(False)
				#Identify Image Captcha
				if "letter word" in message.content and message.attachments:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}Image Captcha Appears{color.reset} {color.red}!!!{color.reset}")
					captcha_image = b64encode(await message.attachments[0].read()).decode("utf-8")
					lenghth = message.content[message.content.find("letter word") - 2]
					await self.solve_icaptcha(captcha_image, lenghth)
				#Identify HCaptcha
				if "https://owobot.com/captcha" in message.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}Hcaptcha Appears{color.reset} {color.red}!!!{color.reset}")
					await self.solve_hcaptcha()
			#Check Ban
			if "You have been banned" in message.content:
				await self.send_webhooks(f"""**💀 | You Have Been Banned!
<:blank:427371936482328596> | Check The Truth <@{self.user.id}>
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}You Have Been Banned{color.reset} {color.red}!!!{color.reset}")
				await self.goodbye()
			#Check Cowoncy
			if "don\'t have enough cowoncy!" in message.content:
				await self.send_webhooks(f"""**💸 | You\'ve Run Out Of Cowoncy!
<:blank:427371936482328596> | Sell Your Zoo To Continue <@{self.user_id}>
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}You\'ve Run Out Of Cowoncy{color.reset} {color.red}!!!{color.reset}")
				await self.goodbye()
		#Check Gem Status
		if self.gem and self.nickname in message.content and self.gem_check and self.work and message.channel.id == self.channel_id and message.author.id == self.OwOID:
			if "and caught" in message.content:
				await self.use_gem()
		#Check Hunt Pet
		if self.nickname in message.content and "🌱" in message.content and "gained" in message.content and self.work and message.channel.id == self.channel_id and message.author.id == self.OwOID:
			filter = message.content.split("**|**")
			pet = filter[0]
			#Legendary Pet
			for i in range(len(self.legendary_list)):
				if self.legendary_list[i] in pet:
					await self.send_webhooks(f"""**<a:legendary:417955061801680909> | I\'ve Just Found The Legendary Pet
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.orange}The Legendary Pet{color.reset}")
					break
			#Gem Pet
			for i in range(len(self.gem_list)):
				if self.gem_list[i] in pet:
					await self.send_webhooks(f"""**<a:gem:510023576489951232> | I\'ve Just Found The Gem Pet
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.green}The Gem Pet{color.reset}")
					break
			#Fabled Pet
			for i in range(len(self.fabled_list)):
				if self.fabled_list[i] in pet:
					await self.send_webhooks(f"""**<a:fabled:438857004493307907> | I\'ve Just Found The Fabled Pet
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.cyan}The Fabled Pet{color.reset}")
					break
			#Distored Pet
			for i in range(len(self.distored_list)):
				if self.distored_list[i] in pet:
					await self.send_webhooks(f"""**<a:distorted:728812986147274835> | I\'ve Just Found The Distorted Pet
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.red}The Distored Pet{color.reset}")
					break
			#Hidden Pet
			for i in range(len(self.hidden_list)):
				if self.hidden_list[i] in pet:
					await self.send_webhooks(f"""**<a:hidden:459203677438083074> | I\'ve Just Found The Hidden Pet
<:blank:427371936482328596> | https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id} **""")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.purple}The Hidden Pet{color.reset}")
					break

	#Collect Edited Messages
	async def on_message_edit(self, before, after):
		if self.work and self.nickname in after.content and self.channel_id == after.channel.id and self.OwOID == after.author.id:
			#Slot
			if self.slot:
				#Lost
				if 'won nothing' in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.red}Lost {self.current_slot_bet} Cowoncy{color.reset}")
					self.benefit_amount -= self.current_slot_bet
					self.current_slot_bet *= self.slot_rate
				#Draw
				if '<:eggplant:417475705719226369> <:eggplant:417475705719226369> <:eggplant:417475705719226369>' in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.gray}Draw {self.current_slot_bet} Cowoncy{color.reset}")
				#Won x2
				if '<:heart:417475705899712522> <:heart:417475705899712522> <:heart:417475705899712522>' in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.green}Won {self.current_slot_bet} Cowoncy (x2){color.reset}")
					self.benefit_amount += self.current_slot_bet
					self.current_slot_bet = self.slot_bet
				#Won x3
				if '<:cherry:417475705178161162> <:cherry:417475705178161162> <:cherry:417475705178161162>' in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.green}Won {self.current_slot_bet * 2} Cowoncy (x3){color.reset}")
					self.benefit_amount += self.current_slot_bet * 2
					self.current_slot_bet = self.slot_bet
				#Won x4
				if '<:cowoncy:417475705912426496> <:cowoncy:417475705912426496> <:cowoncy:417475705912426496>' in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.green}Won {self.current_slot_bet * 3} Cowoncy (x4){color.reset}")
					self.benefit_amount += self.current_slot_bet * 3
					self.current_slot_bet = self.slot_bet
				#Won x10
				if '<:o_:417475705899843604> <:w_:417475705920684053> <:o_:417475705899843604>' in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.green}Won {self.current_slot_bet * 9} Cowoncy (x10){color.reset}")
					self.benefit_amount += self.current_slot_bet * 9
					self.current_slot_bet = self.slot_bet
			#Coinflip
			if self.coinflip:
				#Lost
				if 'you lost' in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Coinflip Turn{color.reset} {color.red}Lost {self.current_coinflip_bet} Cowoncy{color.reset}")
					self.benefit_amount -= self.current_coinflip_bet
					self.current_coinflip_bet *= self.coinflip_rate
				#Won
				if 'you won' in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Coinflip Turn{color.reset} {color.green}Won {self.current_coinflip_bet} Cowoncy{color.reset}")
					self.benefit_amount += self.current_coinflip_bet
					self.current_coinflip_bet = self.coinflip_bet

	#Get Refesh Time
	async def get_refresh_time(self):
		await self.claim_daily(True)
		if self.daily_time - time.time() >= 0:
			return True
		else:
			await self.get_refresh_time()

	#Get OwO's Status
	@tasks.loop(minutes = 1)
	async def check_owo_status(self):
		if self.work and self.check_owo_status.current_loop != 0:
			status = False
			async for message in self.channel.history(limit=25):
				if message.author.id == self.OwOID:
					status = True
					break
			if status:
				self.owo_status = True
			else:
				self.owo_status = False
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}OwO Doesn\'t Respond{color.reset} {color.red}!!!{color.reset}")
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ll Wait For{color.reset} {color.gray}An Hour{color.reset}")
				await self.worker(False)
				await asyncio.sleep(3600)
				self.owo_status = True
				await self.worker(True)

	#Use Fun Commands
	@tasks.loop(seconds = random.randint(60, 120))
	async def entertainment(self):
		if self.work and self.owo_status and self.fun:
			if not self.daily and self.daily_time - time.time() <= 0:
				if (await self.get_refresh_time()):
					self.runn = True
					self.pup = True
					self.piku = True
			choice = random.choice(["run", "pup", "piku"])
			if choice == "run" and self.runn:
				await self.channel.typing()
				await self.channel.send(f"{self.prefix}run")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}run{color.reset}")
			if choice == "pup" and self.pup:
				await self.channel.typing()
				await self.channel.send(f"{self.prefix}pup")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}pup{color.reset}")
			if choice == "piku" and self.piku:
				await self.channel.typing()
				await self.channel.send(f"{self.prefix}piku")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}piku{color.reset}")
			if self.runn or self.pup or self.piku:
				fun_message = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.channel.history(limit=10):
					if message.author.id == self.OwOID and (await self.get_messages(message, "tired to run") or await self.get_messages(message, "no puppies") or await self.get_messages(message, "out of carrots")):
						fun_message = message
						break
				if fun_message:
					#Run Limit
					if "tired to run" in fun_message.content:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Run For Today Is{color.reset} {color.red}Over!{color.reset}")
						self.runn = False
					#Pup Limit
					if "no puppies" in fun_message.content:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Pup For Today Is{color.reset} {color.red}Over!{color.reset}")
						self.pup = False
					#Piku Limit
					if "out of carrots" in fun_message.content:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Piku For Today Is{color.reset} {color.red}Over!{color.reset}")
						self.piku = False

	#Start Grinding
	@tasks.loop(seconds = random.randint(17, 25))
	async def start_grind(self):
		try:
			if self.owo_status:
				if self.work and self.owo:
					say = random.choice(["owo", "uwu"])
					await self.channel.typing()
					await self.channel.send(say)
					print(f"{await self.intro()}{color.yellow}[SEND] {say}{color.reset}")
					await asyncio.sleep(random.randint(1, 2))
				if self.work and self.grind:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}h")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}h{color.reset}")
					await asyncio.sleep(random.randint(1, 2))
				if self.work and self.grind:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}b")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}b{color.reset}")
		except:
			pass

	#Start Sending Quote
	@tasks.loop(seconds = random.randint(30, 60))
	async def start_quote(self):
		if self.work and self.owo_status and self.quote:
			try:
				response = get("https://zenquotes.io/api/random")
				if response.status_code == 200:
					json_data = response.json()
					data = json_data[0]
					quote = data["q"]
					await self.channel.typing()
					await self.channel.send(quote)
					print(f"{await self.intro()}{color.yellow}[SEND] {quote[0:30]}...{color.reset}")
			except:
				pass

	#Start Playing Slot
	@tasks.loop(seconds = random.randint(30, 60))
	async def start_slot(self):
		if self.current_slot_bet  >= 250000:
			self.current_slot_bet = self.slot_bet
		if self.work and self.owo_status and self.slot:
			await self.channel.typing()
			await self.channel.send(f"{self.prefix}s {self.current_slot_bet}")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}s {self.current_slot_bet}{color.reset}")

	#Start Playing Coinflip
	@tasks.loop(seconds = random.randint(30, 60))
	async def start_coinflip(self):
		if self.current_coinflip_bet  >= 250000:
			self.current_coinflip_bet = self.coinflip_bet
		if self.work and self.coinflip:
			side = random.choice(["h", "t"])
			await self.channel.typing()
			await self.channel.send(f"{self.prefix}cf {self.current_coinflip_bet} {side}")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}cf {self.current_coinflip_bet} {side}{color.reset}")

	#Change Channel
	@tasks.loop(seconds = random.randint(300, 600))
	async def change_channel(self):
		if self.work and self.owo_status and self.channel_amount > 1 and self.change_channel.current_loop != 0:
			self.channel_id = random.choice(self.all_channel)
			await self.get_nickname()
			await self.send_webhooks(f"**🏠 | I Changed Channel To <#{self.channel_id}>**")
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Changed Channel To{color.reset} {color.purple}{self.channel}{color.reset}")


	#Claim Daily
	@tasks.loop(minutes = 1)
	async def claim_daily(self, ignore_request = False):
		if self.work and self.owo_status and self.daily or ignore_request and self.daily_time - time.time() <= 0:
			await self.channel.typing()
			await self.channel.send(f"{self.prefix}daily")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}daily{color.reset}")
			daily_message = None
			#Get Messages
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.channel.history(limit=10):
				if message.author.id == self.OwOID and (await self.get_messages(message, "next daily") or await self.get_messages(message, "Nu")):
					daily_message = message
					break
			if daily_message:
				#Waiting
				if "Nu" in daily_message.content:
					next_daily = findall('[0-9]+', daily_message.content)
					next_daily = int(int(next_daily[0]) * 3600 + int(next_daily[1]) * 60 + int(next_daily[2]))
					self.daily_time = next_daily + time.time()
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}You Can Claim Daily After{color.reset} {color.orange}{str(timedelta(seconds=int(next_daily)))} Seconds{color.reset}")
				#Claimed
				elif "Your next daily" in daily_message.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I{color.reset} {color.green}Claimed{color.reset} {color.bold}Daily!{color.reset}")

	#Use Gem
	async def use_gem(self):
		if self.work and self.owo_status and self.gem and self.gem_check:
			await self.channel.typing()
			await self.channel.send(f"{self.prefix}inv")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}inv{color.reset}")
			gem_message = None
			#Get Gem Messages
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.channel.history(limit=10):
				if message.author.id == self.OwOID and (await self.get_messages(message, f"{self.nickname}'s Inventory")):
					gem_message = message
					break
			#Filter Objects
			if gem_message:
				gem_message = findall(r'`(.*?)`', gem_message.content)
				#Common 051 065 072
				if "051" in gem_message and "065" in gem_message and "072" in gem_message:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}use 51 65 72")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}use 51 65 72{color.reset}")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Used{color.reset} {color.red}Common Gem{color.reset} {color.bold}For 25 Turns{color.reset}")
					self.gem_amount += 1
					self.gem_recheck = True
				#Uncommon 052 066 073
				elif "052" in gem_message and "066" in gem_message and "073" in gem_message:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}use 52 66 73")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}use 52 66 73{color.reset}")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Used{color.reset} {color.cyan}Uncommon Gem{color.reset} {color.bold}For 25 Turns{color.reset}")
					self.gem_amount += 1
					self.gem_recheck = True
				#Rare 053 067 074
				elif "053" in gem_message and "067" in gem_message and "074" in gem_message:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}use 53 67 74")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}use 53 67 74{color.reset}")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Used{color.reset} {color.orange}Rare Gem{color.reset} {color.bold}For 50 Turns{color.reset}")
					self.gem_amount += 1
					self.gem_recheck = True
				#Epic 054 068 075
				elif "054" in gem_message and "068" in gem_message and "075" in gem_message:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}use 54 68 75")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}use 54 68 75{color.reset}")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Used{color.reset} {color.blue}Epic Gem{color.reset} {color.bold}For 75 Turns{color.reset}")
					self.gem_amount += 1
					self.gem_recheck = True
				#Mythical 055 069 076
				elif "055" in gem_message and "069" in gem_message and "076" in gem_message:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}use 55 69 76")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}use 55 69 76{color.reset}")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Used{color.reset} {color.purple}Mythical Gem{color.reset} {color.bold}For 75 Turns{color.reset}")
					self.gem_amount += 1
					self.gem_recheck = True
				#Legendary 056 070 077
				elif "056" in gem_message and "070" in gem_message and "077" in gem_message:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}use 56 70 77")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}use 56 70 77{color.reset}")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Used{color.reset} {color.yellow}Legendary Gem{color.reset} {color.bold}For 100 Turns{color.reset}")
					self.gem_amount += 1
					self.gem_recheck = True
				#Fabled 057 071 078
				elif "057" in gem_message and "071" in gem_message and "078" in gem_message:
					await self.channel.typing()
					await self.channel.send(f"{self.prefix}use 57 71 78")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.prefix}use 57 71 78{color.reset}")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Used{color.reset} {color.cyan}Fabled Gem{color.reset} {color.bold}For 100 Turns{color.reset}")
					self.gem_amount += 1
					self.gem_recheck = True
				else:
					#Check Gems Again
					if self.gem_recheck:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ll Check Your Inventory Again{color.reset}")
						self.gem_recheck = False
						await self.use_gem()
					#Don't Have Enough Gems
					else:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Inventory{color.reset} {color.red}Doesn't Have Enough Gems!{color.reset}")
						self.gem_check = False
						self.gem_recheck = False

	#Go To Bed
	@tasks.loop(minutes = 1)
	async def bedtime(self):
		if self.work and self.owo_status and self.sleep and self.work_time - time.time() <= 0:
			interval_before = [task.seconds for task in self.tasks]
			sleep_time = int(random.randint(300, 600))
			for task in self.tasks:
				task.change_interval(seconds = sleep_time)
			await self.send_webhooks(f"**🛌 | I'm Taking A Break For __{sleep_time} Seconds__**")
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I'm Taking A Break For{color.reset} {color.cyan}{sleep_time} Seconds{color.reset}")
			await asyncio.sleep(sleep_time)
			self.work_time = random.randint(600, 1200)
			await self.send_webhooks(f"**🌄 | Done! I'll Work For __{self.work_time} Seconds__**")
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Done! I'll Work For{color.reset} {color.cyan}{self.work_time} Seconds{color.reset}")
			self.work_time += time.time()
			for index, task in enumerate(self.tasks):
				task.change_interval(seconds=interval_before[index])

#Run Selfbot
Client = MyClient()
Client.run(Client.token)