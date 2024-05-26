import discord
from discord import Webhook
from discord.ext import tasks
import asyncio
from aiohttp import ClientSession, CookieJar
import re
import os
import io
import glob
import json
import random
import aiohttp
import numpy as np
from PIL import Image
from requests import get
from base64 import b64encode
from datetime import timedelta
from twocaptcha import TwoCaptcha
from time import strftime, localtime, time, sleep
import time
import datetime

class color:
	mark = '\033[104m'
	bold = '\033[1m'
	gray = '\033[90m'
	cyan = '\033[36m'
	blue = '\033[94m'
	orange = '\033[33m'
	yellow = '\033[93m'
	red = '\033[91m'
	green = '\033[92m'
	purple = '\033[95m'
	reset = '\033[0m'

print()
print(f"{color.bold}You Are Using{color.reset} {color.red}OwO's Selfbot{color.reset} {color.bold}By{color.reset} {color.blue}Phandat (realphandat){color.reset} {color.bold}| https://github.com/realphandat/OwO{color.reset}")
print(f"{color.bold}Created With{color.reset} {color.yellow}Great Contributions{color.reset} {color.bold}From{color.reset} {color.green}ahuhu (ahihiyou20){color.reset} {color.bold}And{color.reset} {color.green}ahehe (cesxos){color.reset}")
print()

class data:
	def __init__(self):
		with open("config.json", "r") as file:
			data = json.load(file)
			self.token = data['token']
			self.get_owo_prefix = data['get_owo_prefix']
			self.channel_id = data['channel_id']
			self.solve_captcha = data['solve_captcha']
			self.grind = data['grind']
			self.huntbot = data['huntbot']
			self.gem = data['gem']
			self.animal = data['animal']
			self.daily = data['daily']
			self.sleep = data['sleep']
			self.gamble = data['gamble']
			self.pray_curse = data['pray_curse']
			self.entertainment = data['entertainment']
			self.webhook = data['webhook']

		self.tasks = [
			self.check_owo_status,
			self.change_channel,
			self.start_grind,
			self.claim_submit_huntbot,
			self.sell_sac_animal,
			self.claim_daily,
			self.go_to_sleep,
			self.play_gamble,
			self.start_pray_curse,
			self.start_entertainment
		]

		self.emoji = {
			"arrow": "<a:Arrow:1065047400714088479>"
		}

		self.owo = {
			"name": None,
			"id": 408785106942164992,
			"dm_channel_id": None,
			"prefix": "owo",
			"status": True
		}
		
		self.discord = {
			"channel": None,
			"channel_id": None,
			"user": None,	
			"user_id": None,
			"user_nickname": None
		}

		self.selfbot = {
			"on_ready": True,
			"run_time": time.time(),
			"work_time": random.randint(600, 1200),
			"work_status": True,
			"sleep_time": None,
			"huntbot_time": 0,
			"daily_time": 0
		}

		self.checking = {
			"no_gem": False,
			"blackjack_end": False,
			"run_limit": False,
			"pup_limit": False,
			"piku_limit": False
		}

		self.current_gamble_bet = {
			"slot": int(self.gamble['slot']['bet']),
			"coinflip": int(self.gamble['coinflip']['bet']),
			"blackjack": int(self.gamble['blackjack']['bet'])
		}

		self.animal_list = {
			"legendary": ['gdeer', 'gfox', 'glion', 'gowl', 'gsquid'],
			"gem": ['gcamel', 'gfish', 'gpanda', 'gshrimp', 'gspider'],
			"bot": ['dinobot', 'giraffbot', 'hedgebot', 'lobbot', 'slothbot'],
			"distored": ['glitchflamingo', 'glitchotter', 'glitchparrot', 'glitchraccoon', 'glitchzebra'],
			"fabled": ['dboar', 'deagle', 'dfrog', 'dgorilla', 'dwolf'],
			"hidden": ['hkoala', 'hlizard','hmonkey', 'hsnake', 'hsquid']
		}

		self.amount = {
			"command": 0,
			"captcha": 0,
			"huntbot": 0,
			"gem": 0,
			"cash": 0,
			"gamble": 0
		}

		self.solver = TwoCaptcha(**{
			"server": "2captcha.com",
			"apiKey": self.solve_captcha['twocaptcha_api'],
			"defaultTimeout": 300,
			"pollingInterval": 5
		})

class MyClient(discord.Client, data):
	def __init__(self, *args, **kwargs):
		discord.Client.__init__(self, *args, **kwargs)
		super().__init__(*args, **kwargs)
		data.__init__(self)

	async def intro(self):
		return f"{color.mark}{strftime('%H:%M:%S', localtime())}{color.reset} - {color.red}{self.discord['user_nickname']}{color.reset} - "

	async def on_ready(self):
		if self.selfbot['on_ready']:
			self.selfbot['on_ready'] = False
			self.owo['name'] = self.get_user(self.owo['id'])
			self.owo['dm_channel_id'] = self.owo['name'].dm_channel.id
			self.discord['user'] = self.user
			self.discord['user_id'] = self.user.id
			await self.startup_channel()
			if self.selfbot['work_time']:
				x = f"<a:Arrow:1065047400714088479>I\'ll Work For **__{self.selfbot['work_time']}__ Seconds**\n<a:Arrow:1065047400714088479><#{self.discord['channel_id']}>"
				y = f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ll Start At Channel{color.reset} {color.purple}{self.discord['channel']}{color.reset} {color.bold}For{color.reset} {color.cyan}{self.selfbot['work_time']} Seconds{color.reset}"
			else:
				x = f"<a:Arrow:1065047400714088479><#{self.discord['channel_id']}>"
				y = f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ll Start At Channel{color.reset} {color.purple}{self.discord['channel']}{color.reset}"
			await self.send_webhooks(
				title = "**🌻 START WORKING 🌻**",
				description = x,
				color = 0xCDC0B0
				)
			print(y)
			self.selfbot['work_time'] += time.time()
			await self.worker(True)

	async def worker(self, mode, skip = []):
		if mode:
			self.selfbot['work_status'] = True
			for task in self.tasks:
				if task in skip:
					continue
				try:
					task.start()
					await asyncio.sleep(10)
				except RuntimeError:
					pass
		else:
			self.selfbot['work_status'] = False
			for task in self.tasks:
				if task in skip:
					continue
				task.cancel()

	async def get_messages(self, message, content, includes_self = False):
		if includes_self:
			return (content.lower() in message.content.lower() and self.user.display_name in message.content)
		return content.lower() in message.content.lower()

	async def send_webhooks(self, content = None, title = None, description = None, color = None, image = None, thumnail = None):
		if self.webhook['mode']:
			async with aiohttp.ClientSession() as session:
				webhook = Webhook.from_url(self.webhook['link'], session=session)
				if title:
					embed = discord.Embed(title = title, description = description, color = color)
					embed.set_author(name = self.user, icon_url = self.user.avatar)
					if image:
						embed.set_image(url = image)
					if thumnail:
						embed.set_thumbnail(url = thumnail)
					embed.timestamp = datetime.datetime.now()
					embed.set_footer(text = self.owo['name'], icon_url = self.owo['name'].avatar)
					await webhook.send(content = content, embed = embed)
				else:
					await webhook.send(content = content)

	async def startup_channel(self):
		self.discord['channel_id'] = int(random.choice(self.channel_id))
		self.discord['channel'] = self.get_channel(self.discord['channel_id'])
		member = await self.discord['channel'].guild.fetch_member(self.discord['user_id'])
		if member.nick:
			self.discord['user_nickname'] = str(member.nick)
		elif not member.nick:
			self.discord['user_nickname'] = str(member.display_name)
		await self.discord['channel'].typing()
		await self.discord['channel'].send(f"{self.owo['prefix']}prefix")
		print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}prefix{color.reset}")
		self.amount['command'] += 1
		if self.get_owo_prefix['mode']:
			owo_prefix_message = None
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id'] and (await self.get_messages(message, f"the current prefix is set to")):
					owo_prefix_message = message
					break
			if owo_prefix_message:
				self.owo['prefix'] = re.findall(r"`(.*?)`", owo_prefix_message.content)[0]
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}OwO\'s Prefix Is Currently{color.reset} {color.gray}{self.owo['prefix']}{color.reset}")
			else:
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.bold}I{color.reset} {color.red}Couldn't Get{color.reset} {color.bold}OwO\'s Prefix ({self.owo['prefix']}){color.reset}")
		else:
			self.owo['prefix'] = self.get_owo_prefix['default']

	@tasks.loop(seconds = random.randint(300, 600))
	async def change_channel(self):
		if len(self.channel_id) >= 1 and self.selfbot['work_status'] and self.owo['status'] and self.change_channel.current_loop != 0:
			await self.startup_channel()
			await self.send_webhooks(
				title = "**🏠 CHANGE CHANNEL 🏠**",
				description = f"{self.emoji['arrow']}<#{self.discord['channel_id']}>",
				color = 0x8B658B
			)
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Changed Channel To{color.reset} {color.purple}{self.discord['channel']}{color.reset}")

	async def solve_image_captcha(self, image, captcha, lenghth):
		try:
			balance = self.solver.balance()
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your 2Captcha API Currently Have{color.reset} {color.green}{balance}${color.reset}")
			result = self.solver.normal(captcha, numeric=2, minLen=lenghth, maxLen=lenghth, phrase=0, caseSensitive=0, calc=0, lang="en")
		except Exception as e:
			await self.send_webhooks(
				content = f"<@{self.discord['user_id']}>",
				title = "**⚙️ 2CAPTCHA API ⚙️**",
				description = f"{self.emoji['arrow']}Error: {str(e)}",
				color = 0xCDC9C9
			)
			if str(e) == "ERROR_KEY_DOES_NOT_EXIST" or str(e) == "ERROR_WRONG_USER_KEY":
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.bold}Your 2Captcha API Is{color.reset} {color.red}Invalid{color.reset}")
			if str(e) == "ERROR_ZERO_BALANCE":
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.bold}Your 2Captcha API{color.reset} {color.red}Run Out Of Money{color.reset}")
			if str(e) != "ERROR_KEY_DOES_NOT_EXIST" and str(e) != "ERROR_WRONG_USER_KEY" and str(e) != "ERROR_ZERO_BALANCE":
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}Your 2Captcha API Has The Problem{color.reset} {color.red}!!!{color.reset} | {e}")
				await self.solve_image_captcha()
		await self.owo['name'].typing()
		await self.owo['name'].send(result['code'])
		self.amount['command'] += 1
		await asyncio.sleep(random.randint(3, 5))
		captcha_verification_message = None
		async for message in self.owo['name'].dm_channel.history(limit = 1):
					if message.author.id == self.owo['id'] and (await self.get_messages(message, "verified") or await self.get_messages(message, "Wrong")):
						captcha_verification_message = message
		if "verified" in captcha_verification_message.content and captcha_verification_message.author.id == self.owo['id']:
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved Image Captcha{color.reset} {color.green}Successfully{color.reset}")
			await self.send_webhooks(
				title = "**🎉 CORRECT SOLUTION 🎉**",
				description = f"{self.emoji['arrow']}**Answer:** {result['code']}\n{self.emoji['arrow']}**Continue To Work**",
				color = 0x4EEE94,
				thumnail = image
			)
			self.solver.report(result['captchaId'], True)
			self.amount['captcha'] += 1
			await self.worker(True)
		elif "(2/3)" in captcha_verification_message.content and captcha_verification_message.author.id == self.owo['id']:
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved It{color.reset} {color.red}Wrong Twice{color.reset}")
			await self.send_webhooks(
				content = f"<@{self.discord['user_id']}>",
				title = "**⛔ INCORRECT SOLUTION ⛔**",
				description = f"{self.emoji['arrow']}**Answer:** {result['code']}\n{self.emoji['arrow']}I Solved It **Wrong Twice**",
				color = 0xEE2C2C,
				thumnail = image
			)
			self.solver.report(result['captchaId'], False)
		elif "Wrong" in captcha_verification_message.content and captcha_verification_message.author.id == self.owo['id']:
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved Image Captcha{color.reset} {color.red}Failed{color.reset}")
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ll Try To{color.reset} {color.red}Solve It Again{color.reset}")
			await self.send_webhooks(
				content = f"<@{self.discord['user_id']}>",
				title = "**⛔ INCORRECT SOLUTION ⛔**",
				description = f"{self.emoji['arrow']}**Answer:** {result['code']}\n{self.emoji['arrow']}I\'ll Try To **Solve It Again**",
				color = 0xEE2C2C,
				thumnail = image
			)
			self.solver.report(result['captchaId'], False)
			await self.solve_image_captcha(image, captcha, lenghth)

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
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.red}!!!{color.reset} {color.bold}Failed To Add Token To Oauth{color.reset} {color.red}!!!{color.reset} | {res2.status}")
				await self.send_webhooks(
					content = f"<@{self.discord['user_id']}>",
					title = "**⚙️ SUMBIT OAUTH ⚙️**",
					description = f"{self.emoji['arrow']}Error: {res2.status}",
					color = 0xCDC9C9
				)
				await self.submit_oauth(res)


	async def get_oauth(self):
		async with ClientSession() as session:
			oauth = "https://discord.com/api/v9/oauth2/authorize?response_type=code&redirect_uri=https%3A%2F%2Fowobot.com%2Fapi%2Fauth%2Fdiscord%2Fredirect&scope=identify%20guilds%20email%20guilds.members.read&client_id=408785106942164992"
			payload = {"permissions": "0", "authorize": True}
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
					print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.red}!!!{color.reset} {color.bold}Getting Oauth Has The Problem{color.reset} {color.red}!!!{color.reset} | {await res.text()}")
					await self.send_webhooks(
						content = f"<@{self.discord['user_id']}>",
						title = "**⚙️ GET OAUTH ⚙️**",
						description = f"{self.emoji['arrow']}Error: {await res.text()}",
						color = 0xCDC9C9
					)
					await self.get_oauth()

	async def solve_hcaptcha(self):
		headers = {
			"Accept": "application/json, text/plain, */*",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-US;en;q=0.8",
			"Content-Type": "application/json;charset=UTF-8",
			"Origin": "https://owobot.com",
			"Referer": "https://owobot.com/captcha",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
		}
		try:
			balance = self.solver.balance()
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your 2Captcha API Currently Have{color.reset} {color.green}{balance}${color.reset}")
			result = self.solver.hcaptcha(sitekey="a6a1d5ce-612d-472d-8e37-7601408fbc09", url="https://owobot.com/captcha")
		except Exception as e:
			await self.send_webhooks(
				content = f"<@{self.discord['user_id']}>",
				title = "**⚙️ 2CAPTCHA API ⚙️**",
				description = f"{self.emoji['arrow']}Error: {str(e)}",
				color = 0xCDC9C9
			)
			if str(e) == "ERROR_KEY_DOES_NOT_EXIST" or str(e) == "ERROR_WRONG_USER_KEY":
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.bold}Your 2Captcha API Is{color.reset} {color.red}Invalid{color.reset}")
			if str(e) == "ERROR_ZERO_BALANCE":
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.bold}Your 2Captcha API{color.reset} {color.red}Run Out Of Money{color.reset}")
			if str(e) != "ERROR_KEY_DOES_NOT_EXIST" and str(e) != "ERROR_WRONG_USER_KEY" and str(e) != "ERROR_ZERO_BALANCE":
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.red}!!!{color.reset} {color.bold}Your 2Captcha API Has The Problem{color.reset} {color.red}!!!{color.reset} | {e}")
				await self.solve_hcaptcha()
		async with (await self.get_oauth()) as session:
			cookies = {cookie.key: cookie.value for cookie in session.cookie_jar}
			async with session.post("https://owobot.com/api/captcha/verify", headers=headers, json={"token": result['code']}, cookies=cookies) as res:
				if res.status == 200:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved Hcaptcha{color.reset} {color.green}Successfully{color.reset}")
					await self.send_webhooks(
						title = "**🎉 CORRECT SOLUTION 🎉**",
						description = f"{self.emoji['arrow']}**Continue To Work**",
						color = 0x4EEE94
					)
					self.amount['captcha'] += 1
					await self.worker(True)
				else:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Solved Hcaptcha{color.reset} {color.red}Failed{color.reset}")
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ll Try To{color.reset} {color.red}Solve It Again{color.reset}")
					await self.send_webhooks(
						content = f"<@{self.discord['user_id']}>",
						title = "**⛔ INCORRECT SOLUTION ⛔**",
						description = f"{self.emoji['arrow']}I\'ll Try To **Solve It Again**",
						color = 0xEE2C2C
					)
					await self.solve_hcaptcha()

	async def on_message(self, message):
		#Detect image captchas
		if "⚠" in message.content and "letter word" in message.content and message.attachments and (message.channel.id == self.owo['dm_channel_id'] or str(self.discord['user']) in message.content) and message.author.id == self.owo['id']:
			await self.worker(False)
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}Image Captcha Appears{color.reset} {color.red}!!!{color.reset}")
			await self.send_webhooks(
				content = f"<@{self.discord['user_id']}>",
				title = "**🚨 IMAGE CAPTCHA APPEARS 🚨**",
				description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
				color = 0x7EC0EE,
				image = message.attachments[0]
			)
			if self.solve_captcha['image_captcha']:
				captcha = b64encode(await message.attachments[0].read()).decode("utf-8")
				lenghth = message.content[message.content.find("letter word") - 2]
				await self.solve_image_captcha(message.attachments[0], captcha, lenghth)
		#Detect hcaptchas
		if "⚠" in message.content and "https://owobot.com/captcha" in message.content and f"<@{self.discord['user_id']}>" in message.content and message.author.id == self.owo['id']:
			await self.worker(False)
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}Hcaptcha Appears{color.reset} {color.red}!!!{color.reset}")
			await self.send_webhooks(
				content = f"<@{self.discord['user_id']}>",
				title = "**🚨 HCAPTCHA APPEARS 🚨**",
				description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
				color = 0x7EC0EE
			)
			if self.solve_captcha['hcaptcha']:
				await self.solve_hcaptcha()
		#Detect problems
		if (str(self.discord['user']) in message.content or str(self.discord['user_nickname']) in message.content) and message.author.id == self.owo['id']:
			if "You have been banned" in message.content:
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}You Have Been Banned{color.reset} {color.red}!!!{color.reset}")
				await self.send_webhooks(
					content = f"<@{self.discord['user_id']}>",
					title = "**🔨 YOU\'VE BEEN BANNED 🔨**",
					description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
					color = 0xEE2C2C
				)
				await self.worker(False)
			if "don\'t have enough cowoncy!" in message.content:
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}You\'ve Run Out Of Cowoncy{color.reset} {color.red}!!!{color.reset}")
				await self.send_webhooks(
					content = f"<@{self.discord['user_id']}>",
					title = "**💸 RUN OUT OF COWONCY 💸**",
					description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
					color = 0xEE2C2C
				)
				await self.worker(False)

		#Someone challenge you
		if self.selfbot['work_status'] and self.owo['status'] and message.embeds and f"<@{self.discord['user_id']}>" in message.content and message.author.id == self.owo['id']:
			if "owo ab" in message.embeds[0].description and "owo db" in message.embeds[0].description:
				await self.send_webhooks(
					title = "**🥊 SOMEONE CHALLENGE YOU 🥊**",
					description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
					color = 0xEE2C2C
				)
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Someone{color.reset} {color.red}Challenges{color.reset} {color.bold}You{color.reset}")
				choice = random.choice([1, 2])
				await asyncio.sleep(random.randint(3, 5))
				if choice == 1:
					await message.channel.typing()
					await message.channel.send(f"{self.owo['prefix']}ab")
					self.amount['command'] += 1
				if choice == 2:
					components = message.components
					firstButton = components[0].children[0]
					await firstButton.click()

		#Check gems in use
		if self.gem['mode'] and self.selfbot['work_status'] and self.owo['status'] and "🌱" in message.content and "gained" in message.content and (not self.checking["no_gem"] or int(self.selfbot['work_time']) - time.time() <= -300) and str(self.discord['user_nickname']) in message.content and message.channel.id == self.discord['channel_id'] and message.author.id == self.owo['id']:
			empty = []
			if not "gem1" in message.content:
				empty.append("gem1")
			if not "gem3" in message.content:
				empty.append("gem3")
			if not "gem4" in message.content:
				empty.append("gem4")
			if not "star" in message.content and self.gem['star']:
				empty.append("star")
			if empty:
				await self.discord['channel'].typing()
				await self.discord['channel'].send(f"{self.owo['prefix']}inv")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}inv{color.reset}")
				self.amount['command'] += 1
				inv = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit = 10):
					if message.author.id == self.owo['id'] and (await self.get_messages(message, f"{self.discord['user_nickname']}'s Inventory")):
						inv = message
						break
				if inv:
					inv = [int(item) for item in  re.findall(r"`(.*?)`", inv.content) if item.isnumeric()]
					if self.gem['open_box'] and 50 in inv:
						await self.discord['channel'].typing()
						await self.discord['channel'].send(f"{self.owo['prefix']}lb all")
						print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}lb all{color.reset}")
						self.amount['command'] += 1
						await asyncio.sleep(random.randint(3, 5))
					if self.gem['open_crate'] and 100 in inv:
						await self.discord['channel'].typing()
						await self.discord['channel'].send(f"{self.owo['prefix']}wc all")
						print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}wc all{color.reset}")
						self.amount['command'] += 1
						await asyncio.sleep(random.randint(3, 5))
					gem_in_inv = None
					if self.gem['sort'].lower() == "best":
						gems_in_inv = [sorted([gem for gem in inv if range[0] < gem < range[1]], reverse=True) for range in [(50, 58), (64, 72), (71, 79), (79, 86)]]
					else:
						gems_in_inv = [sorted([gem for gem in inv if range[0] < gem < range[1]]) for range in [(50, 58), (64, 72), (71, 79), (79, 86)]]
					if gem_in_inv != [[], [], [], []]:
						use_gem = ""
						if "gem1" in empty and gems_in_inv[0] != []:
							use_gem = use_gem + str(gems_in_inv[0][0]) + " "
						if "gem3" in empty and gems_in_inv[1] != []:
							use_gem = use_gem + str(gems_in_inv[1][0]) + " "
						if "gem4" in empty and gems_in_inv[2] != []:
							use_gem = use_gem + str(gems_in_inv[2][0]) + " "
						if "star" in empty and gems_in_inv[3] != []:
							use_gem = use_gem + str(gems_in_inv[3][0]) + " "
						await self.discord['channel'].typing()
						await self.discord['channel'].send(f"{self.owo['prefix']}use {use_gem}")
						print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}use {use_gem}{color.reset}")
						self.amount['command'] += 1
						self.amount['gem'] += 1
						self.checking['no_gem'] = False
					else:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Inventory{color.reset} {color.red}Doesn't Have Enough Gems{color.reset}")
						self.checking['no_gem'] = True
				else:
					print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.bold}I{color.reset} {color.red}Couldn't Get{color.reset} {color.bold}Your Inventory{color.reset}")

		#Commands
		if self.webhook['mode'] and (message.author.id in self.webhook['owner_id'] or message.author.id == self.discord['user_id']):
			#Start
			if message.content.lower() == "start":
				if not self.selfbot['work_status']:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Start{color.reset} {color.gray}Selfbot{color.reset}")
					await self.send_webhooks(
						title = f"💼 START SELFBOT 💼",
						color = 0x8B4513
					)
					await self.worker(True)
				else:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}You Can\'t Start,{color.reset} {color.gray}I\'m Working{color.reset}")
					await self.send_webhooks(content = f"**🍁 | You Can\'t Resume, I\'m Working**")
			#Pause
			if message.content.lower() == "pause":
				if self.selfbot['work_status']:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Pause{color.reset} {color.gray}Selfbot{color.reset}")
					await self.send_webhooks(
						title = f"⏰ PAUSE SELFBOT ⏰",
						color = 0xCDC9C9
					)
					await self.worker(False)
				else:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Been{color.reset} {color.gray}Pause Before{color.reset}")
					await self.send_webhooks(content = f"**🍁 | I\'ve Been Pause Before**")
			#Stat
			if message.content.lower() == "stat":
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Send Stat{color.reset} {color.gray}Via Webhook{color.reset}")
				await self.send_webhooks(
					title = f"📊 {self.discord['user_nickname']}'s STAT 📊",
					description = f"I Worked For {strftime('**%H:%M:%S**',time.gmtime(time.time() - self.selfbot['run_time']))} With:\n{self.emoji['arrow']}Sent **__{self.amount['command']}__ Commands**\n{self.emoji['arrow']}Solved **__{self.amount['captcha']}__ Captchas**\n{self.emoji['arrow']}Claimed Huntbot **__{self.amount['huntbot']}__ Times**\n{self.emoji['arrow']}Used Gem **__{self.amount['gem']}__ Times**\n{self.emoji['arrow']}Got **__{self.amount['cash']}__ Cowoncy**\n{self.emoji['arrow']} Gambled **__{self.amount['gamble']}__ Cowoncy**",
					color = 0x4EEE94
				)

		#Check the caught animals
		if self.selfbot['work_status'] and self.owo['status'] and str(self.discord['user_nickname']) in message.content and "🌱" in message.content and "gained" in message.content and message.channel.id == self.discord['channel_id'] and message.author.id == self.owo['id']:
			filter = message.content.split("**|**")
			pet = filter[0]
			#Legendary pet
			for i in range(len(self.animal_list['legendary'])):
				if self.animal_list['legendary'][i] in pet:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.orange}The Legendary Pet{color.reset}")
					await self.send_webhooks(
						title = "**<a:legendary:417955061801680909> FOUND LEGENDARY PET <a:legendary:417955061801680909>**",
						description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
						color = 0xF1FC00
					)
					break
			#Gem pet
			for i in range(len(self.animal_list['gem'])):
				if self.animal_list['gem'][i] in pet:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.green}The Gem Pet{color.reset}")
					await self.send_webhooks(
						title = "**<a:gem:510023576489951232> FOUND GEM PET <a:gem:510023576489951232>**",
						description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
						color = 0x63FF78
					)
					break
			#Fabled pet
			for i in range(len(self.animal_list['fabled'])):
				if self.animal_list['fabled'][i] in pet:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.cyan}The Fabled Pet{color.reset}")
					await self.send_webhooks(
						title = "**<a:fabled:438857004493307907> FOUND FABLED PET <a:fabled:438857004493307907>**",
						description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
						color = 0xAEDFFF
					)
					break
			#Distored pet
			for i in range(len(self.animal_list['distored'])):
				if self.animal_list['distored'][i] in pet:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.red}The Distored Pet{color.reset}")
					await self.send_webhooks(
						title = "**<a:distorted:728812986147274835> FOUND DISTORED PET <a:distorted:728812986147274835>**",
						description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
						color = 0x9E4D4D
					)
					break
			#Hidden pet
			for i in range(len(self.animal_list['hidden'])):
				if self.animal_list['hidden'][i] in pet:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ve Just Found{color.reset} {color.purple}The Hidden Pet{color.reset}")
					await self.send_webhooks(
						title = "**<a:hidden:459203677438083074> FOUND HIDDEN PET <a:hidden:459203677438083074>**",
						description = f"{self.emoji['arrow']}https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
						color = 0xB400CB
					)
					break	

	async def on_message_edit(self, before, after):
		if self.selfbot['work_status'] and self.owo['status'] and after.channel.id == self.discord['channel_id'] and after.author.id == self.owo['id']:
			#Slot
			if self.gamble['slot']['mode'] and str(self.discord['user_nickname']) in after.content:
				#Lost
				if "won nothing" in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.red}Lost {self.current_gamble_bet['slot']} Cowoncy{color.reset}")
					self.amount['gamble'] -= self.current_gamble_bet['slot']
					self.current_gamble_bet['slot'] *= self.gamble['slot']['rate']
				#Draw
				if "<:eggplant:417475705719226369> <:eggplant:417475705719226369> <:eggplant:417475705719226369>" in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.gray}Draw {self.current_gamble_bet['slot']} Cowoncy{color.reset}")
				#Won x2
				if "<:heart:417475705899712522> <:heart:417475705899712522> <:heart:417475705899712522>" in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.green}Won {self.current_gamble_bet['slot']} Cowoncy (x2){color.reset}")
					self.amount['gamble'] += self.current_gamble_bet['slot']
					self.current_gamble_bet['slot'] = self.gamble['slot']['bet']
				#Won x3
				if "<:cherry:417475705178161162> <:cherry:417475705178161162> <:cherry:417475705178161162>" in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.green}Won {self.current_gamble_bet['slot'] * 2} Cowoncy (x3){color.reset}")
					self.amount['gamble'] += self.current_gamble_bet['slot'] * 2
					self.current_gamble_bet['slot'] = self.gamble['slot']['bet']
				#Won x4
				if "<:cowoncy:417475705912426496> <:cowoncy:417475705912426496> <:cowoncy:417475705912426496>" in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.green}Won {self.current_gamble_bet['slot'] * 3} Cowoncy (x4){color.reset}")
					self.amount['gamble'] += self.current_gamble_bet['slot'] * 3
					self.current_gamble_bet['slot'] = self.gamble['slot']['bet']
				#Won x10
				if "<:o_:417475705899843604> <:w_:417475705920684053> <:o_:417475705899843604>" in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Slot Turn{color.reset} {color.green}Won {self.current_gamble_bet['slot'] * 9} Cowoncy (x10){color.reset}")
					self.amount['gamble'] += self.current_gamble_bet['slot'] * 9
					self.current_gamble_bet['slot'] = self.gamble['slot']['bet']
			#Coinflip
			if self.gamble['coinflip']['mode'] and str(self.discord['user_nickname']) in after.content:
				#Lost
				if "you lost" in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Coinflip Turn{color.reset} {color.red}Lost {self.current_gamble_bet['coinflip']} Cowoncy{color.reset}")
					self.amount['gamble'] -= self.current_gamble_bet['coinflip']
					self.current_gamble_bet['coinflip'] *= self.gamble['coinflip']['rate']
				#Won
				if "you won" in after.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Coinflip Turn{color.reset} {color.green}Won {self.current_gamble_bet['coinflip']} Cowoncy{color.reset}")
					self.amount['gamble'] += self.current_gamble_bet['coinflip']
					self.current_gamble_bet['coinflip'] = self.gamble['coinflip']['bet']

	@tasks.loop(minutes = 1)
	async def check_owo_status(self):
		if self.selfbot['work_status'] and self.check_owo_status.current_loop != 0:
			status = False
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id']:
					status = True
					break
			if status:
				self.owo['status'] = True
			else:
				self.owo['status'] = False
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.red}!!!{color.reset} {color.bold}OwO Doesn\'t Respond{color.reset} {color.red}!!!{color.reset}")
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I\'ll Wait For{color.reset} {color.gray}10 Minutes{color.reset}")
				await self.send_webhooks(
					content = f"<@{self.discord['user_id']}>",
					title = "**💀 OWO IS OFFLINE 💀**",
					description = f"{self.emoji['arrow']}I\'ll Wait For **10 Minutes**",
					color = 0xCDC9C9
				)
				await self.worker(False, skip = [self.check_owo_status])
				sleep(600)
				self.owo['status'] = True
				await self.worker(True, skip = [self.check_owo_status])

	@tasks.loop(seconds = random.randint(18, 25))
	async def start_grind(self):
		if self.grind['owo'] and self.selfbot['work_status'] and self.owo['status']:
			say = random.choice(['owo', 'Owo', 'uwu', 'Uwu'])
			await self.discord['channel'].typing()
			await self.discord['channel'].send(say)
			print(f"{await self.intro()}{color.yellow}[SEND] {say}{color.reset}")
			self.amount['command'] += 1
			await asyncio.sleep(random.randint(6, 10))
		if self.grind['hunt'] and self.selfbot['work_status'] and self.owo['status']:
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}h")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}h{color.reset}")
			self.amount['command'] += 1
			await asyncio.sleep(random.randint(6, 10))
		if self.grind['battle'] and self.selfbot['work_status'] and self.owo['status']:
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}b")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}b{color.reset}")
			self.amount['command'] += 1
			await asyncio.sleep(random.randint(6, 10))
		if self.grind['quote'] and self.selfbot['work_status'] and self.owo['status']:
			try:
				response = get("https://zenquotes.io/api/random")
				if response.status_code == 200:
					json_data = response.json()
					data = json_data[0]
					quote = data['q']
					await self.discord['channel'].typing()
					await self.discord['channel'].send(quote)
					print(f"{await self.intro()}{color.yellow}[SEND] {quote[0:30]}...{color.reset}")
					self.amount['command'] += 1
			except:
				pass

	@tasks.loop(minutes = 1)
	async def claim_submit_huntbot(self):
		if self.huntbot['claim_submit'] and self.selfbot['work_status'] and self.owo['status'] and int(self.selfbot['huntbot_time']) - time.time() <= 0:
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}hb 1d")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}hb 1d{color.reset}")
			self.amount['command'] += 1
			huntbot_message = None
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id'] and (await self.get_messages(message, "Please include your password") or await self.get_messages(message, "Here is") or await self.get_messages(message, "BACK IN") or await self.get_messages(message, "BACK WITH")):
					huntbot_message = message
					break
			if huntbot_message:
				#Lost huntbot captchas
				if "Please include your password" in huntbot_message.content:
					next_huntbot = re.findall(r"(?<=Password will reset in )(\d+)", huntbot_message.content)
					next_huntbot = int(int(next_huntbot[0]) * 60)
					self.selfbot['huntbot_time'] = next_huntbot + time.time()
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Lost Huntbot Message, Retry After{color.reset} {color.yellow}{str(timedelta(seconds = int(next_huntbot)))} Seconds{color.reset}")
				#Solve huntbot captchas
				if "Here is" in huntbot_message.content:
					await self.send_webhooks(
						content = f"<@{self.discord['user_id']}>",
						title = "**🚨 HUNTBOT CAPTCHA 🚨**",
						description = f"{self.emoji['arrow']}https://discord.com/channels/{huntbot_message.guild.id}/{huntbot_message.channel.id}/{huntbot_message.id}",
						color = 0x7EC0EE,
						image = message.attachments[0]
					)
					checks = []
					check_images = glob.glob("huntbot/**/*.png")
					for check_image in sorted(check_images):
						img = Image.open(check_image)
						checks.append((img, img.size, check_image.split(".")[0].split(os.sep)[-1]))
					async with aiohttp.ClientSession() as session:
						async with session.get(message.attachments[0].url) as resp:
							large_array = np.array(Image.open(io.BytesIO(await resp.read())))
					matches = []
					for check in checks:
						small_array = np.array(check[0])
						large_h, large_w = large_array.shape[:2]
						small_h, small_w = small_array.shape[:2]
						for y in range(large_h - small_h + 1):
							for x in range(large_w - small_w + 1):
								segment = large_array[y:y + small_h, x:x + small_w]
								mask = (small_array[:, :, 3] > 0) 
								if np.array_equal(segment[mask], small_array[mask]):
									overlap = False
									for m in matches:
										if (m[0] - check[1][0] < x < m[0] + check[1][0]) and (m[1] - check[1][1] < y < m[1] + check[1][1]):
											overlap = True
											break
									if not overlap:
										matches.append((x, y, check[2]))
					matches = sorted(matches,key=lambda tup: tup[0])
					answer = "".join([i[2] for i in matches])
					await self.discord['channel'].typing()
					await self.discord['channel'].send(f"{self.owo['prefix']}hb 1d {answer}")
					print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}hb 1d {answer}{color.reset}")
					self.amount['command'] += 1
					try:
						await self.client.wait_for("message", check=lambda m: "Wrong password" in m.content and m.channel.id == self.discord['channel'] and self.discord['user_nickname'] in m.content, timeout = 10)
					except TimeoutError:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Submitted Huntbot{color.reset} {color.green}Successfully{color.reset}")
						await self.send_webhooks(
							title = "**🎉 CORRECT SOLUTION 🎉**",
							description = f"{self.emoji['arrow']}**Answer:** {answer}",
							color = 0xCDC0B0,
							thumnail = message.attachments[0]
						)
					else:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I Submitted Huntbot{color.reset} {color.green}Failed{color.reset}")
						await self.send_webhooks(
							title = "**⛔ INCORRECT SOLUTION ⛔**",
							description = f"{self.emoji['arrow']}**Answer:** {answer}",
							color = 0xEE2C2C,
							thumnail = message.attachments[0]
						)

				#Sumbit huntbot
				elif "STILL HUNTING" in huntbot_message.content:
					next_huntbot = re.findall("[0-9]+", re.findall("`(.*?)`", huntbot_message.content)[0])
					if len(next_huntbot) == 1:
						next_huntbot = int(int(next_huntbot[0]) * 60)
					else:
						next_huntbot = int(int(next_huntbot[0]) * 3600 + int(next_huntbot[1]) * 60)
					self.selfbot['huntbot_time'] = next_huntbot + time.time()
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Huntbot\'ll Be Back In{color.reset} {color.yellow}{str(timedelta(seconds = int(next_huntbot)))} Seconds{color.reset}")
					await self.send_webhooks(
						title = "**📌 SUBMITTED HUNTBOT 📌**",
						description = huntbot_message.content,
						color = 0xCDC0B0
						)
				#Claim huntbot
				elif "BACK WITH" in huntbot_message.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I{color.reset} {color.green}Claimed{color.reset} {color.bold}Your Huntbot{color.reset}")
					await self.send_webhooks(
						title = "**📦 CLAIMED HUNTBOT 📦**",
						description = huntbot_message.content,
						color = 0x4EEE94
						)
					if self.huntbot['upgrade']['mode']:
						await self.discord['channel'].typing()
						await self.discord['channel'].send(f"{self.owo['prefix']}upgrade {self.huntbot['upgrade']['type']} all")
						print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}upgrade {self.huntbot['upgrade']['type']} all{color.reset}")
						self.amount['command'] += 1
			else:
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.bold}I{color.reset} {color.red}Couldn't Get{color.reset} {color.bold}Huntbot Message{color.reset}")

	@tasks.loop(seconds = random.randint(300, 600))
	async def sell_sac_animal(self):
		if self.animal['mode'] and self.selfbot['work_status'] and self.owo['status']:
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}{self.animal['type']} {self.animal['rank']}")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}{self.animal['type']} {self.animal['rank']}{color.reset}")
			self.amount['command'] += 1
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}cash")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}cash{color.reset}")
			self.amount['command'] += 1
			cash_message = None
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id'] and (await self.get_messages(message, "you currently have")):
					cash_message = message
					break
			if cash_message:
				self.amount['cash'] = re.findall(r"__(.*?)__", cash_message.content)[0]
				print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}You Currently Have{color.reset} {color.green}{self.amount['cash']} Cowoncy{color.reset}")

	@tasks.loop(minutes = 1)
	async def claim_daily(self):
		if self.daily and self.selfbot['work_status'] and self.owo['status'] and int(self.selfbot['daily_time']) - time.time() <= 0:
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}daily")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}daily{color.reset}")
			self.amount['command'] += 1
			daily_message = None
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id'] and (await self.get_messages(message, "next daily") or await self.get_messages(message, "Nu")):
					daily_message = message
					break
			if daily_message:
				if "Nu" in daily_message.content:
					next_daily = re.findall("[0-9]+", daily_message.content)
					next_daily = int(int(next_daily[0]) * 3600 + int(next_daily[1]) * 60 + int(next_daily[2]))
					self.selfbot['daily_time'] = next_daily + time.time()
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}You Can Claim Daily After{color.reset} {color.orange}{str(timedelta(seconds = int(next_daily)))} Seconds{color.reset}")
				elif "Your next daily" in daily_message.content:
					print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I{color.reset} {color.green}Claimed{color.reset} {color.bold}Daily{color.reset}")
			else:
				print(f"{await self.intro()}{color.red}[ERROR]{color.reset} {color.bold}I{color.reset} {color.red}Couldn't Get{color.reset} {color.bold}Daily Message{color.reset}")

	@tasks.loop(minutes = 1)
	async def go_to_sleep(self):
		if self.sleep and self.selfbot['work_status'] and self.owo['status'] and int(self.selfbot['work_time']) - time.time() <= 0:
			self.selfbot['sleep_time'] = int(random.randint(300, 600))
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}I'm Taking A Break For{color.reset} {color.cyan}{self.selfbot['sleep_time']} Seconds{color.reset}")
			await self.send_webhooks(
				title = "**🛌 TAKE A BREAK 🛌**",
				description = f"{self.emoji['arrow']}I'm Taking A Break For **__{self.selfbot['sleep_time']}__ Seconds**",
				color = 0xA2B5CD
				)
			await self.worker(False, skip = [self.go_to_sleep])
			await asyncio.sleep(self.selfbot['sleep_time'])
			self.selfbot['work_time'] = random.randint(600, 1200)
			print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Done! I'll Work For{color.reset} {color.cyan}{self.selfbot['work_time']} Seconds{color.reset}")
			await self.send_webhooks(
				title = "**🌄 WAKE UP 🌄**",
				description = f"{self.emoji['arrow']}I'll Work For **__{self.selfbot['work_time']}__ Seconds**",
				color = 0xFFF68F
			)
			self.selfbot['work_time'] += time.time()
			await self.worker(True, skip = [self.go_to_sleep])

	@tasks.loop(seconds = random.randint(60, 120))
	async def play_gamble(self):
		#Slot
		if self.gamble['slot']['mode'] and self.selfbot['work_status'] and self.owo['status']:
			if self.current_gamble_bet['slot']  >= self.gamble['slot']['max']:
				self.current_gamble_bet['slot'] = self.gamble['slot']['bet']
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}s {self.current_gamble_bet['slot']}")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}s {self.current_gamble_bet['slot']}{color.reset}")
			self.amount['command'] += 1
			await asyncio.sleep(random.randint(3, 5))
		#Coinflip
		if self.gamble['coinflip']['mode'] and self.selfbot['work_status'] and self.owo['status']:
			if self.current_gamble_bet['coinflip']  >= self.gamble['coinflip']['max']:
				self.current_gamble_bet['coinflip'] = self.gamble['coinflip']['bet']
			side = random.choice(['h', 't'])
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}cf {self.current_gamble_bet['coinflip']} {side}")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}cf {self.current_gamble_bet['coinflip']} {side}{color.reset}")
			self.amount['command'] += 1
			await asyncio.sleep(random.randint(3, 5))
		#Blackjack
		if self.gamble['blackjack']['mode'] and self.selfbot['work_status'] and self.owo['status']:
			if self.current_gamble_bet['blackjack']  >= self.gamble['blackjack']['max']:
				self.current_gamble_bet['blackjack'] = self.gamble['blackjack']['bet']
			await self.discord['channel'].typing()
			await self.discord['channel'].send(f"{self.owo['prefix']}bj {self.current_gamble_bet['blackjack']}")
			print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}bj {self.current_gamble_bet['blackjack']}{color.reset}")
			self.amount['command'] += 1
			self.checking['blackjack_end'] = False
			while not self.checking['blackjack_end']:
				message = None
				await asyncio.sleep(random.randint(3, 5))
				async for m in self.discord['channel'].history(limit=10):
					if m.channel.id == self.discord['channel_id'] and m.author.id == self.owo['id'] and m.embeds:
						if str(self.discord['user']) in m.embeds[0].author.name and "play blackjack" in m.embeds[0].author.name:
							message = m
							break
				if message:
					if "in progress" in message.embeds[0].footer.text or "resuming previous" in message.embeds[0].footer.text:
						my_blackjack_point = int(re.findall(r"\[(.*?)\]", message.embeds[0].fields[1].name)[0])
						if my_blackjack_point <= 17:
							try:
								if message.reactions[0].emoji == "👊":
									if message.reactions[0].me:
										await message.remove_reaction('👊', self.discord['user'])
									else:
										await message.add_reaction('👊')
								else:
									if message.reactions[1].me:
										await message.remove_reaction('👊', self.discord['user'])
									else:
										await message.add_reaction('👊')
								print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Blackjack Turn Has{color.reset} {color.blue}{my_blackjack_point} Points (Hit){color.reset}")
							except IndexError:
								pass
						else:
							await message.add_reaction('🛑')
							print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Blackjack Turn Has{color.reset} {color.blue}{my_blackjack_point} Points (Stand){color.reset}")
					elif "You won" in message.embeds[0].footer.text:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Blackjack Turn{color.reset} {color.green}Won {self.current_gamble_bet['blackjack']} Cowoncy{color.reset}")
						self.amount['gamble'] += self.current_gamble_bet['blackjack']
						self.current_gamble_bet['blackjack'] = self.gamble['blackjack']['bet']
						self.checking['blackjack_end'] = True
					elif "You lost" in message.embeds[0].footer.text:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Blackjack Turn{color.reset} {color.red}Lost {self.current_gamble_bet['blackjack']} Cowoncy{color.reset}")
						self.amount['gamble'] -= self.current_gamble_bet['blackjack']
						self.current_gamble_bet['blackjack'] *= self.gamble['blackjack']['rate']
						self.checking['blackjack_end'] = True
					elif "You tied" in message.embeds[0].footer.text or "You both bust" in message.embeds[0].footer.text:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Blackjack Turn{color.reset} {color.gray}Draw {self.current_gamble_bet['blackjack']} Cowoncy{color.reset}")
						self.checking['blackjack_end'] = True
				else:
					break

	@tasks.loop(seconds = random.randint(300, 360))
	async def start_pray_curse(self):
		if self.pray_curse['mode'] and self.selfbot['work_status'] and self.owo['status']:
			#Pray
			if self.pray_curse['type'].lower() == "pray":
				await self.discord['channel'].typing()
				await self.discord['channel'].send(f"{self.owo['prefix']}pray {self.pray_curse['user_id']}")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}pray {self.pray_curse['user_id']}{color.reset}")
				self.amount['command'] += 1
			#Curse
			else:
				await self.discord['channel'].typing()
				await self.discord['channel'].send(f"{self.owo['prefix']}curse <@{self.pray_curse['user_id']}>")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}curse <@{self.pray_curse['user_id']}>{color.reset}")
				self.amount['command'] += 1

	@tasks.loop(seconds = random.randint(60, 120))
	async def start_entertainment(self):
		if self.selfbot['work_status'] and self.owo['status']:
			if int(self.selfbot['daily_time']) - time.time() <= 0:
				self.checking['run_limit'] = False
				self.checking['pup_limit'] = False
				self.checking['piku_limit'] = False
			#Run
			if self.entertainment['run'] and not self.checking['run_limit']:
				await self.discord['channel'].typing()
				await self.discord['channel'].send(f"{self.owo['prefix']}run")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}run{color.reset}")
				self.amount['command'] += 1
				run_message = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit=10):
					if message.author.id == self.owo['id'] and await self.get_messages(message, "tired to run"):
						run_message = message
						break
				if run_message:
					if "tired to run" in run_message.content:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Run For Today Is{color.reset} {color.red}Over{color.reset}")
						self.checking['run_limit'] = True
			#Pup
			if self.entertainment['pup'] and not self.checking['pup_limit']:
				await self.discord['channel'].typing()
				await self.discord['channel'].send(f"{self.owo['prefix']}pup")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}pup{color.reset}")
				self.amount['command'] += 1
				pup_message = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit=10):
					if message.author.id == self.owo['id'] and await self.get_messages(message, "no puppies"):
						pup_message = message
						break
				if pup_message:
					if "no puppies" in pup_message.content:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Pup For Today Is{color.reset} {color.red}Over{color.reset}")
						self.checking['pup_limit'] = True
			#Piku
			if self.entertainment['piku'] and not self.checking['piku_limit']:
				await self.discord['channel'].typing()
				await self.discord['channel'].send(f"{self.owo['prefix']}piku")
				print(f"{await self.intro()}{color.yellow}[SEND] {self.owo['prefix']}piku{color.reset}")
				self.amount['command'] += 1
				piku_message = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit=10):
					if message.author.id == self.owo['id'] and await self.get_messages(message, "out of carrots"):
						piku_message = message
						break
				if piku_message:
					if "out of carrots" in piku_message.content:
						print(f"{await self.intro()}{color.blue}[INFO]{color.reset} {color.bold}Your Piku For Today Is{color.reset} {color.red}Over{color.reset}")
						self.checking['piku_limit'] = True

Client = MyClient()
Client.run(Client.token)
