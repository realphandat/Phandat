import discord, logging, logging.handlers, logging.config, asyncio, re, os, io, glob, json, random, aiohttp, time, datetime, threading, numpy as np
from discord import Webhook, ButtonStyle, Button
from discord.ext import tasks
from aiohttp import ClientSession, CookieJar
from requests import get
from PIL import Image
from base64 import b64encode
from twocaptcha import TwoCaptcha
from selenium_driverless import webdriver
from selenium.webdriver.common.by import By

class color:
	bold = '\033[1m'
	gray = "\x1b[38;5;240m"
	red = "\x1b[38;5;196m"
	green = "\x1b[38;5;10m"
	yellow = "\x1b[38;5;227m"
	blue = "\x1b[38;5;39m"
	cyan = "\x1b[38;5;44m"
	pink = "\x1b[38;5;218m"
	purple = "\x1b[38;5;141m"
	reset = "\x1b[0m"

class CustomFormatter(logging.Formatter):
	template = "\x1b[43m%(asctime)s\x1b[0m - \x1b[38;5;212m%(name)s\x1b[0m - {}[%(levelname)s]{} %(message)s"

	formats = {
		logging.DEBUG: template.format(color.gray, color.reset) + " (%(filename)s:%(lineno)d)",
		logging.INFO: template.format(color.blue, color.reset),
		logging.WARNING: template.format(color.yellow, color.reset),
		logging.ERROR: template.format(color.red, color.reset) + " (%(filename)s:%(lineno)d)",
		logging.CRITICAL: template.format(color.purple, color.reset) + " (%(filename)s:%(lineno)d)",
	}

	def format(self, record):
		log_fmt = self.formats.get(record.levelno)
		formatter = logging.Formatter(fmt = log_fmt, datefmt='%d %b %Y %H:%M:%S')
		return formatter.format(record)


class FileFormatter(logging.Formatter):
	def format(self, record):
		format = "%(asctime)s - %(name)s - [%(levelname)s] %(message)s"
		formatter = logging.Formatter(fmt = format, datefmt='%d %b %Y %H:%M:%S')
		return formatter.format(record)

class MyClient(discord.Client):
	def __init__(self, token, *args, **kwargs):
		discord.Client.__init__(self, *args, **kwargs)
		super().__init__(*args, **kwargs)
		self.token = token
		with open("config.json", "r") as file:
			data = json.load(file)
			self.get_owo_prefix = data[token]['get_owo_prefix']
			self.channel_id = data[token]['channel_id']
			self.someone_mentions = data[token]['someone_mentions']
			self.image_captcha = data[token]['image_captcha']
			self.hcaptcha = data[token]['hcaptcha']
			self.twocaptcha_balance = data[token]['twocaptcha_balance']
			self.top_gg = data[token]['top_gg']
			self.grind = data[token]['grind']
			self.huntbot = data[token]['huntbot']
			self.gem = data[token]['gem']
			self.distorted_animals = data[token]['distorted_animals']
			self.animals = data[token]['animals']
			self.daily = data[token]['daily']
			self.sleep = data[token]['sleep']
			self.gamble = data[token]['gamble']
			self.pray_curse = data[token]['pray_curse']
			self.entertainment = data[token]['entertainment']
			self.command = data[token]['command']
			self.webhook = data[token]['webhook']
			self.join_giveaway = data[token]['join_giveaway']
			self.someone_challenges = data[token]['someone_challenges']
			self.music_notification = data[token]['music_notification']

		self.tasks = [
			self.check_owo_status,
			self.check_2captcha_balance,
			self.vote_top_gg,
			self.change_channel,
			self.start_grind,
			self.claim_submit_huntbot,
			self.check_distorted_animal,
			self.sell_sac_animal,
			self.claim_daily,
			self.go_to_sleep,
			self.play_gamble,
			self.start_pray_curse,
			self.start_entertainment
		]

		self.arrow = "<a:Arrow:1065047400714088479>"

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
			"user_nickname": "None",
			"inventory": "gem1 gem3 gem4 star",
			"giveaway_entered": []
		}

		self.selfbot = {
			"on_ready": True,
			"work_status": True,
			"turn_on_time": time.time(),
			"work_time": random.randint(600, 1200),
			"sleep_time": "",
			"huntbot_time": 0,
			"glitch_time": 0,
			"daily_time": 0,
			"mentioner": ""
		}

		self.checking = {
			"captcha_attempts": 0,
			"is_captcha": False,
			"no_gem": False,
			"is_blackjack": False,
			"run_limit": False,
			"pup_limit": False,
			"piku_limit": False
		}
		
		self.current_loop = {
			"change_channel": 0,
			"check_distorted_animal": 0,
			"daily": 0
		}

		self.current_gamble_bet = {
			"slot": int(self.gamble['slot']['bet']),
			"coinflip": int(self.gamble['coinflip']['bet']),
			"blackjack": int(self.gamble['blackjack']['bet'])
		}

		self.animals_list = {
			"legendary": ['gdeer', 'gfox', 'glion', 'gowl', 'gsquid'],
			"gem": ['gcamel', 'gfish', 'gpanda', 'gshrimp', 'gspider'],
			"bot": ['dinobot', 'giraffbot', 'hedgebot', 'lobbot', 'slothbot'],
			"distorted": ['glitchflamingo', 'glitchotter', 'glitchparrot', 'glitchraccoon', 'glitchzebra'],
			"fabled": ['dboar', 'deagle', 'dfrog', 'dgorilla', 'dwolf'],
			"hidden": ['hkoala', 'hlizard','hmonkey', 'hsnake', 'hsquid']
		}

		self.amount = {
			"command": 0,
			"captcha": 0,
			"huntbot": 0,
			"gem": 0,
			"gamble": 0,
			"change_channel": 0,
			"sleep": 0
		}

	async def log(self):
		self.logger = logging.getLogger(str(self.user))
		file_log = logging.handlers.WatchedFileHandler(f"logs/{str(self.user)}.log", encoding='utf-8', mode='a+')
		file_log.setFormatter(FileFormatter())
		print_log = logging.StreamHandler()
		print_log.setFormatter(CustomFormatter())
		self.logger.addHandler(file_log)
		self.logger.addHandler(print_log)
		self.logger.setLevel(logging.DEBUG)

	async def notify(self):
		if self.music_notification:
			try:
				os.startfile('music.mp3')
			except:
				pass

	async def on_ready(self):
		if self.selfbot['on_ready']:
			self.selfbot['on_ready'] = False
			self.owo['name'] = self.get_user(self.owo['id'])
			self.owo['dm_channel_id'] = self.owo['name'].dm_channel.id
			for i in self.webhook['mentioner_id']:
				self.selfbot['mentioner'] = self.selfbot['mentioner'] + f"<@{i}>"
			if str(self.user.id) not in self.selfbot['mentioner']:
				self.selfbot['mentioner'] = self.selfbot['mentioner'] + f"<@{self.user.id}>"
			await self.startup_channel()
			await self.log()
			webhook = f"{self.arrow}<#{self.discord['channel_id']}>"
			if self.sleep:
				webhook = f"{self.arrow}Work for **__{self.selfbot['work_time']}__ seconds**\n" + webhook
			if self.command['mode']:
				webhook = f"{self.arrow}**Send `help`** or **`<@{self.user.id}> help`**\n" + webhook
			cmd = f"Start at channel {self.discord['channel']}"
			if self.sleep:
				cmd = cmd + f" for {self.selfbot['work_time']} seconds"
			self.logger.info(cmd)
			await self.send_webhooks(
				title = f"🚀 STARTED <t:{int(self.selfbot['turn_on_time'])}:R> 🚀",
				description = webhook,
				color = discord.Colour.random()
				)
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
				try:
					task.cancel()
				except RuntimeError:
					pass

	async def send_webhooks(self, content = None, title = None, description = None, color = None, image = None, thumnail = None):
		if self.webhook['mode']:
			async with aiohttp.ClientSession() as session:
				webhook = Webhook.from_url(self.webhook['url'], session=session)
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
		member = await self.discord['channel'].guild.fetch_member(self.user.id)
		if member.nick:
			self.discord['user_nickname'] = str(member.nick)
		elif not member.nick:
			self.discord['user_nickname'] = str(member.display_name)
		if self.get_owo_prefix['mode']:
			await self.discord['channel'].send(f"{self.owo['prefix']}prefix")
			self.logger.info(f"Sent {self.owo['prefix']}prefix")
			self.amount['command'] += 1
			owo_prefix_message = None
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id'] and "the current prefix is set to" in message.content:
					owo_prefix_message = message
					break
			if owo_prefix_message:
				self.owo['prefix'] = re.findall(r"`(.*?)`", owo_prefix_message.content)[0]
				self.logger.info(f"OwO prefix is currently {self.owo['prefix']}")
			else:
				self.logger.error(f"Couldn't get OwO prefix ({self.owo['prefix']})")
		else:
			self.owo['prefix'] = self.get_owo_prefix['default']

	@tasks.loop(seconds = random.randint(600, 1200))
	async def change_channel(self):
		if len(self.channel_id) > 1 and self.selfbot['work_status'] and self.owo['status'] and self.current_loop['change_channel'] > 0:
			await self.startup_channel()
			self.logger.info(f"Changed channel to {self.discord['channel']}")
			await self.send_webhooks(
				title = "🏠 CHANGED CHANNEL 🏠",
				description = f"{self.arrow}<#{self.discord['channel_id']}>",
				color = discord.Colour.random()
			)
			self.amount['change_channel'] += 1
		self.current_loop['change_channel'] += 1

	async def solve_image_captcha(self, image, captcha, lenghth, wrong_answer = []):
		result = None
		for api_key in self.image_captcha['twocaptcha']:
			twocaptcha = TwoCaptcha(**{
						"server": "2captcha.com",
						"apiKey": str(api_key),
						"defaultTimeout": 300,
						"pollingInterval": 5
			})
			retry_times = 0
			while retry_times <= 10:
				try:
					balance = twocaptcha.balance()
					self.logger.info(f"TwoCaptcha API ({api_key}) currently have {balance}$")
					result = twocaptcha.normal(captcha, numeric = 2, minLen = lenghth, maxLen = lenghth, phrase = 0, caseSensitive = 0, calc = 0, lang = "en")
					if result['code'].lower() in wrong_answer:
						twocaptcha.report(result['captchaId'], False)
						await self.solve_image_captcha(image, captcha, lenghth, wrong_answer)
					break
				except Exception as e:
					await self.send_webhooks(
						content = self.selfbot['mentioner'],
						title = "⚙️ TWOCAPTCHA API ⚙️",
						description = f"{self.arrow}Error: {str(e)}",
						color = discord.Colour.random()
					)
					if str(e) == "ERROR_KEY_DOES_NOT_EXIST" or str(e) == "ERROR_WRONG_USER_KEY":
						self.logger.error(f"TwoCaptcha API ({api_key}) is invalid")
						break
					elif str(e) == "ERROR_ZERO_BALANCE":
						self.logger.error(f"TwoCaptcha API ({api_key}) ran out of money")
						break
					else:
						self.logger.error(f"!!! TwoCaptcha API ({api_key}) has the problem !!! | {e}")
						retry_times += 1
						await asyncio.sleep(random.randint(3, 5))
			if result: break
		else:
			await self.notify()
		if result:
			await self.owo['name'].send(result['code'])
			self.logger.info(f"Sent {result['code']}")
			self.amount['command'] += 1
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.owo['name'].dm_channel.history(limit = 1):
				if message.author.id == self.user.id:
					self.checking['is_captcha'] = False
					self.checking['captcha_attempts'] = 0
					await self.worker(True)
				elif "👍" in message.content:
					self.logger.info(f"Solved Image Captcha successfully")
					await self.send_webhooks(
						title = "🎉 CORRECT SOLUTION 🎉",
						description = f"{self.arrow}**Answer:** {result['code']}\n{self.arrow}**Continue To Work**",
						color = discord.Colour.random(),
						thumnail = image
					)
					twocaptcha.report(result['captchaId'], True)
					self.amount['captcha'] += 1
					self.checking['is_captcha'] = False
					self.checking['captcha_attempts'] = 0
					await self.worker(True)
				elif "🚫" in message.content:
					self.logger.info(f"Solved Image Captcha failed")
					await self.send_webhooks(
						content = self.selfbot['mentioner'],
						title = "🚫 INCORRECT SOLUTION 🚫",
						description = f"{self.arrow}**Answer:** {result['code']}\n{self.arrow}Try To **Solve It Again**",
						color = discord.Colour.random(),
						thumnail = image
					)
					twocaptcha.report(result['captchaId'], False)
					self.checking['captcha_attempts'] += 1
					if self.checking['captcha_attempts'] <= int(self.image_captcha['attempts']):
						wrong_answer.append(result['code'].lower())
						await self.solve_image_captcha(image, captcha, lenghth, wrong_answer)
					else:
						await self.notify()

	async def submit_oauth(self, res):
		retry_times = 0
		while retry_times <= 10:
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
					self.logger.error(f"!!! Failed to add token to HCaptcha oauth !!! | {res2.status}")
					await self.send_webhooks(
						content = self.selfbot['mentioner'],
						title = "⚙️ SUMBIT HCAPTCHA OAUTH ⚙️",
						description = f"{self.arrow}Error: {res2.status}",
						color = discord.Colour.random()
					)
			retry_times += 1
			await asyncio.sleep(random.randint(3, 5))
		else:
			await self.notify()


	async def get_oauth(self):
		retry_times = 0
		while retry_times <= 10:
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
						self.logger.error(f"!!! Getting HCaptcha oauth has the problem !!! | {await res.text()}")
						await self.send_webhooks(
							content = self.selfbot['mentioner'],
							title = "⚙️ GET HCAPTCHA OAUTH ⚙️",
							description = f"{self.arrow}Error: {await res.text()}",
							color = discord.Colour.random()
						)
			retry_times += 1
			await asyncio.sleep(random.randint(3, 5))
		else:
			await self.notify()

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
		result = None
		for api_key in self.hcaptcha['twocaptcha']:
			twocaptcha = TwoCaptcha(**{
						"server": "2captcha.com",
						"apiKey": str(api_key),
						"defaultTimeout": 300,
						"pollingInterval": 5
			})
			retry_times = 0
			while retry_times <= 10:
				try:
					balance = twocaptcha.balance()
					self.logger.info(f"TwoCaptcha API ({api_key}) currently have {balance}$")
					result = twocaptcha.hcaptcha(sitekey = "a6a1d5ce-612d-472d-8e37-7601408fbc09", url = "https://owobot.com/captcha")
					break
				except Exception as e:
					await self.send_webhooks(
						content = self.selfbot['mentioner'],
						title = "⚙️ TWOCAPTCHA API ⚙️",
						description = f"{self.arrow}Error: {str(e)}",
						color = discord.Colour.random()
					)
					if str(e) == "ERROR_KEY_DOES_NOT_EXIST" or str(e) == "ERROR_WRONG_USER_KEY":
						self.logger.error(f"TwoCaptcha API ({api_key}) is invalid")
						break
					elif str(e) == "ERROR_ZERO_BALANCE":
						self.logger.error(f"TwoCaptcha API ({api_key}) run out of money")
						break
					else:
						self.logger.error(f"!!! TwoCaptcha API ({api_key}) has the problem !!! | {e}")
						retry_times += 1
						await asyncio.sleep(random.randint(3, 5))
			if result: break
		else:
			await self.notify()
		if result:
			result_session = await self.get_oauth()
			if result_session:
				async with result_session as session:
					cookies = {cookie.key: cookie.value for cookie in session.cookie_jar}
					async with session.post("https://owobot.com/api/captcha/verify", headers=headers, json={"token": result['code']}, cookies=cookies) as res:
						if res.status == 200:
							self.logger.info(f"Solved HCaptcha successfully")
							await self.send_webhooks(
								title = "🎉 CORRECT SOLUTION 🎉",
								description = f"**{self.arrow}Continue To Work**",
								color = discord.Colour.random()
							)
							twocaptcha.report(result['captchaId'], True)
							self.amount['captcha'] += 1
							self.checking['is_captcha'] = False
							self.checking['captcha_attempts'] = 0
							await self.worker(True)
						else:
							self.logger.info(f"Solved HCaptcha failed")
							await self.send_webhooks(
								content = self.selfbot['mentioner'],
								title = "🚫 INCORRECT SOLUTION 🚫",
								description = f"{self.arrow}Try To **Solve It Again**",
								color = discord.Colour.random()
							)
							twocaptcha.report(result['captchaId'], False)
							self.checking['captcha_attempts'] += 1
							if self.checking['captcha_attempts'] <= int(self.hcaptcha['attempts']):
								await self.solve_hcaptcha()
							else:
								await self.notify()

	async def on_message(self, message):
		#Someone mentions
		if self.someone_mentions and message.mentions and self.selfbot['work_status'] and self.owo['status'] and not message.author.bot and message.channel.id == self.discord['channel_id']:
			if message.mentions[0].id == self.user.id or f"<@{self.user.id}>" in message.content:
				self.logger.info(f"Someone mentions")
				await self.send_webhooks(
					title = "🏷️ SOMEONE MENTIONS 🏷️",
					description = f"{self.arrow}{message.jump_url}",
					color = discord.Colour.random()
				)
				await self.change_channel()

		#Detect Image Captcha
		if not self.checking['is_captcha'] and "⚠️" in message.content and "letter word" in message.content and message.attachments and (message.channel.id == self.owo['dm_channel_id'] or str(self.user) in message.content) and message.author.id == self.owo['id']:
			self.checking['is_captcha'] = True
			await self.worker(False)
			self.logger.warning(f"!!! Image Captcha appears !!!")
			await self.send_webhooks(
				content = self.selfbot['mentioner'],
				title = "🚨 IMAGE CAPTCHA APPEARS 🚨",
				description = f"{self.arrow}{message.jump_url}",
				color = discord.Colour.random(),
				image = message.attachments[0]
			)
			if self.image_captcha['mode']:
				captcha = b64encode(await message.attachments[0].read()).decode("utf-8")
				lenghth = message.content[message.content.find("letter word") - 2]
				await self.solve_image_captcha(message.attachments[0], captcha, lenghth)
			else:
				await self.notify()

		#Detect HCaptcha
		if not self.checking['is_captcha'] and "⚠️" in message.content and "https://owobot.com/captcha" in message.content and f"<@{self.user.id}>" in message.content and message.author.id == self.owo['id']:
			self.checking['is_captcha'] = True
			await self.worker(False)
			self.logger.warning(f"!!! HCaptcha appears !!!")
			await self.send_webhooks(
				content = self.selfbot['mentioner'],
				title = "🚨 HCAPTCHA APPEARS 🚨",
				description = f"{self.arrow}{message.jump_url}",
				color = discord.Colour.random()
			)
			if self.hcaptcha['mode']:
				await self.solve_hcaptcha()
			else:
				await self.notify()

		#Detect Unknown Captcha
		if not self.checking['is_captcha'] and "Please complete your captcha to verify that you are human!" in message.content and not message.attachments and not "https://owobot.com/captcha" in message.content and f"<@{self.user.id}>" in message.content and message.author.id == self.owo['id']:
			await self.notify()
			self.checking['is_captcha'] = True
			await self.worker(False)
			self.logger.warning(f"!!! Unknown Captcha appears !!!")
			await self.send_webhooks(
				content = self.selfbot['mentioner'],
				title = "🔒 UNKNOWN CAPTCHA APPEARS 🔒",
				description = f"{self.arrow}{message.jump_url}",
				color = discord.Colour.random()
			)

		#Detect problem
		if (str(self.user) in message.content or self.discord['user_nickname'] in message.content) and message.author.id == self.owo['id']:
			if "You have been banned" in message.content:
				await self.notify()
				self.logger.warning(f"!!! Has been banned !!!")
				await self.send_webhooks(
					content = self.selfbot['mentioner'],
					title = "🔨 HAS BEEN BANNED 🔨",
					description = f"{self.arrow}{message.jump_url}",
					color = discord.Colour.random()
				)
				await self.worker(False)
			if "don't have enough cowoncy!" in message.content and not "you silly hooman" in message.content:
				await self.notify()
				self.logger.warning(f"!!! Out of cowoncy !!!")
				await self.send_webhooks(
					content = self.selfbot['mentioner'],
					title = "💸 OUT OF COWONCY 💸",
					description = f"{self.arrow}{message.jump_url}",
					color = discord.Colour.random()
				)
				await self.worker(False)

		#Check and use gem
		if self.selfbot['work_status'] and self.owo['status'] and (self.gem['mode'] or (self.distorted_animals and not self.selfbot['glitch_time'] - time.time() <= 0 and self.current_loop['check_distorted_animal'] > 0)) and (not self.checking['no_gem'] or (self.sleep and self.daily and int(self.selfbot['daily_time']) - time.time() <= 0 and self.current_loop['daily'] > 0)) and "🌱" in message.content and "gained" in message.content and self.discord['user_nickname'] in message.content and message.channel.id == self.discord['channel_id'] and message.author.id == self.owo['id']:
			empty = []
			if not "gem1" in message.content and "gem1" in self.discord['inventory']:
				empty.append("gem1")
			if not "gem3" in message.content and "gem3" in self.discord['inventory']:
				empty.append("gem3")
			if not "gem4" in message.content and "gem4" in self.discord['inventory']:
				empty.append("gem4")
			if not "star" in message.content and "star" in self.discord['inventory'] and self.gem['star']:
				empty.append("star")
			if empty:
				await self.discord['channel'].send(f"{self.owo['prefix']}inv")
				self.logger.info(f"Sent {self.owo['prefix']}inv")
				self.amount['command'] += 1
				inv = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit = 10):
					if message.author.id == self.owo['id'] and f"{self.discord['user_nickname']}'s Inventory" in message.content:
						inv = message
						self.discord['inventory'] = inv.content
						break
				if inv:
					inv = [int(item) for item in re.findall(r"`(.*?)`", inv.content) if item.isnumeric()]
					if self.gem['open_box'] and 50 in inv:
						await self.discord['channel'].send(f"{self.owo['prefix']}lb all")
						self.logger.info(f"Sent {self.owo['prefix']}lb all")
						self.amount['command'] += 1
						await asyncio.sleep(random.randint(3, 5))
					if self.gem['open_crate'] and 100 in inv:
						await self.discord['channel'].send(f"{self.owo['prefix']}wc all")
						self.logger.info(f"Sent {self.owo['prefix']}wc all")
						self.amount['command'] += 1
						await asyncio.sleep(random.randint(3, 5))
					gems_in_inv = None
					if self.gem['sort'].lower() == "min":
						gems_in_inv = [sorted([gem for gem in inv if range[0] < gem < range[1]]) for range in [(50, 58), (64, 72), (71, 79), (79, 86)]]
					else:
						gems_in_inv = [sorted([gem for gem in inv if range[0] < gem < range[1]], reverse=True) for range in [(50, 58), (64, 72), (71, 79), (79, 86)]]
					if gems_in_inv != [[], [], [], []]:
						use_gem = ""
						if "gem1" in empty and gems_in_inv[0] != []:
							use_gem = use_gem + str(gems_in_inv[0][0]) + " "
						if "gem3" in empty and gems_in_inv[1] != []:
							use_gem = use_gem + str(gems_in_inv[1][0]) + " "
						if "gem4" in empty and gems_in_inv[2] != []:
							use_gem = use_gem + str(gems_in_inv[2][0]) + " "
						if "star" in empty and gems_in_inv[3] != []:
							use_gem = use_gem + str(gems_in_inv[3][0]) + " "
						await self.discord['channel'].send(f"{self.owo['prefix']}use {use_gem}")
						self.logger.info(f"Sent {self.owo['prefix']}use {use_gem}")
						self.amount['command'] += 1
						self.amount['gem'] += 1
						self.checking['no_gem'] = False
					else:
						self.logger.info(f"Inventory doesn't have enough gems")
						self.checking['no_gem'] = True
				else:
					self.logger.error(f"Couldn't get inventory")

		#Commands
		if self.command['mode'] and (message.author.id in self.command['owner_id'] or message.author.id == self.user.id):
			#Help
			if message.content.lower() == "help" or message.content.lower() == f"<@{self.user.id}> help":
				self.logger.info(f"Sent command menu via webhook")
				await self.send_webhooks(
					title = f"📋 COMMAND MENU 📋",
					description = "**`help`\n`say` + `text`\n`start`\n`pause`\n`stat`\n`setting`\n`give` + `amount`**",
					color = discord.Colour.random()
				)
			#Say
			if message.content.lower().startswith("say") or message.content.lower().startswith(f"<@{self.user.id}> say"):
				if message.content.lower().startswith(f"<@{self.user.id}>"):
					text = message.content.replace(f"<@{self.user.id}> ", "", 1)
				else:
					text = message.content
				text = text[4:]
				await message.channel.send(text)
				self.logger.info(f"Sent {text}")
			#Start
			if message.content.lower() == "start" or message.content.lower() == f"<@{self.user.id}> start":
				self.checking['is_captcha'] = False
				await self.worker(True)
				self.logger.info(f"Start selfbot")
				await self.send_webhooks(
					title = f"🌤️ START SELFBOT 🌤️",
					color = discord.Colour.random()
				)
			#Pause
			if message.content.lower() == "pause" or message.content.lower() == f"<@{self.user.id}> pause":
				await self.worker(False)
				self.logger.info(f"Pause selfbot")
				await self.send_webhooks(
					title = f"🌙 PAUSE SELFBOT 🌙",
					color = discord.Colour.random()
				)
			#Stat
			if message.content.lower() == "stat" or message.content.lower() == f"<@{self.user.id}> stat":
				self.logger.info(f"Sent stat via webhook")
				await self.send_webhooks(
					title = f"📊 STAT 📊",
					description = f"Worked **<t:{int(self.selfbot['turn_on_time'])}:R>** with:\n{self.arrow}Sent **__{self.amount['command']}__ Commands**\n{self.arrow}Solved **__{self.amount['captcha']}__ Captchas**\n{self.arrow}Claimed Huntbot **__{self.amount['huntbot']}__ Times**\n{self.arrow}Used Gem **__{self.amount['gem']}__ Times**\n{self.arrow}Gambled **__{self.amount['gamble']}__ Cowoncy**\n{self.arrow}Changed Channel **__{self.amount['change_channel']}__ Times**\n{self.arrow}Slept **__{self.amount['sleep']}__ Times**",
					color = discord.Colour.random()
				)
			#Setting
			if message.content.lower() == "setting" or message.content.lower() == f"<@{self.user.id}> setting":
				await self.send_webhooks(
					title = f"🔥 CONFIRM `YES` IN 10S 🔥",
					description = "**Send setting via webhook including __token__, __TwoCaptcha API__, __webhook url__, ...**",
					color = discord.Colour.random()
				)
				try:
					await self.wait_for("message", check=lambda m: m.content.lower() in ['yes', 'y'] and m.author.id in self.command['owner_id'], timeout = 10)
				except asyncio.TimeoutError:
					pass
				else:
					self.logger.info(f"Sent setting via webhook")
					config = json.load(open("config.json"))
					await self.send_webhooks(
						title = f"💾 SETTING 💾",
						description = config[self.token],
						color = discord.Colour.random()
					)
			#Give
			if message.author.id != self.user.id and message.content.lower().startswith("give") or message.content.lower().startswith(f"<@{self.user.id}> give"):
				amount = int(re.findall("[0-9]+", message.content)[0])
				if message.channel.id == self.discord['channel_id']:
					await message.channel.send(f"{self.owo['prefix']}give <@{message.author.id}> {amount}")
					self.logger.info(f"Sent {self.owo['prefix']}give <@{message.author.id}> {amount}")
				else:
					await message.channel.send(f"owogive <@{message.author.id}> {amount}")
					self.logger.info(f"Sent owogive <@{message.author.id}> {amount}")
				self.amount['command'] += 1
				await asyncio.sleep(random.randint(3, 5))
				async for m in message.channel.history(limit = 10):
					if m.author.id == self.owo['id'] and m.embeds:
						channel = self.get_channel(message.channel.id)
						member = await channel.guild.fetch_member(self.user.id)
						if member.nick:
							nickname = str(member.nick)
						elif not member.nick:
							nickname = str(member.display_name)
						if nickname in m.embeds[0].author.name and "you are about to give cowoncy" in m.embeds[0].author.name:
							button = m.components[0].children[0]
							await button.click()
							self.logger.info(f"Gived cowoncy successfully")
							break
					elif m.author.id == self.owo['id'] and nickname in m.content and "you can only send" in m.content:
						self.logger.info(f"Amount of giving cowoncy for today is over")
						break
					elif m.author.id == self.owo['id'] and nickname in m.content and "you silly hooman" in m.content:
						self.logger.info(f"Don't have enough cowoncy to give")
						break
				else:
					self.logger.error(f"Couldn't get send cowoncy message")

		#Check the caught animals
		if self.selfbot['work_status'] and self.owo['status'] and self.discord['user_nickname'] in message.content and "🌱" in message.content and "gained" in message.content and message.channel.id == self.discord['channel_id'] and message.author.id == self.owo['id']:
			filter = message.content.split("**|**")
			pet = filter[0]
			#Legendary
			for i in range(len(self.animals_list['legendary'])):
				if self.animals_list['legendary'][i] in pet:
					self.logger.info(f"Found Legendary pet")
					await self.send_webhooks(
						title = "<a:legendary:417955061801680909> LEGENDARY PET <a:legendary:417955061801680909>",
						description = f"{self.arrow}{message.jump_url}",
						color = discord.Colour.random()
					)
					break
			#Gem
			for i in range(len(self.animals_list['gem'])):
				if self.animals_list['gem'][i] in pet:
					self.logger.info(f"Found Gem pet")
					await self.send_webhooks(
						title = "<a:gem:510023576489951232> GEM PET <a:gem:510023576489951232>",
						description = f"{self.arrow}{message.jump_url}",
						color = discord.Colour.random()
					)
					break
			#Fabled
			for i in range(len(self.animals_list['fabled'])):
				if self.animals_list['fabled'][i] in pet:
					self.logger.info(f"Found Fabled pet")
					await self.send_webhooks(
						title = "<a:fabled:438857004493307907> FABLED PET <a:fabled:438857004493307907>",
						description = f"{self.arrow}{message.jump_url}",
						color = discord.Colour.random()
					)
					break
			#Distorted
			for i in range(len(self.animals_list['distorted'])):
				if self.animals_list['distorted'][i] in pet:
					self.logger.info(f"Found Distorted pet")
					await self.send_webhooks(
						title = "<a:distorted:728812986147274835> DISTORTED PET <a:distorted:728812986147274835>",
						description = f"{self.arrow}{message.jump_url}",
						color = discord.Colour.random()
					)
					break
			#Hidden
			for i in range(len(self.animals_list['hidden'])):
				if self.animals_list['hidden'][i] in pet:
					self.logger.info(f"Found Hidden pet")
					await self.send_webhooks(
						title = "<a:hidden:459203677438083074> HIDDEN PET <a:hidden:459203677438083074>",
						description = f"{self.arrow}{message.jump_url}",
						color = discord.Colour.random()
					)
					break

		#Someone challenges
		if self.someone_challenges and self.selfbot['work_status'] and self.owo['status'] and message.embeds and f"<@{self.user.id}>" in message.content and message.author.id == self.owo['id']:
			if "owo ab" in message.embeds[0].description and "owo db" in message.embeds[0].description:
				self.logger.info(f"Someone challenges")
				await self.send_webhooks(
					title = "🥊 SOMEONE CHALLENGES 🥊",
					description = f"{self.arrow}{message.jump_url}",
					color = discord.Colour.random()
				)
				choice = random.choice([1, 2])
				await asyncio.sleep(random.randint(3, 5))
				if choice == 1:
					if message.channel.id == self.discord['channel_id']:
						await message.channel.send(f"{self.owo['prefix']}ab")
						self.logger.info(f"Sent {self.owo['prefix']}ab")
					else:
						await message.channel.send(f"owoab")
						self.logger.info(f"Sent owoab")
					self.amount['command'] += 1
				if choice == 2:
					button = message.components[0].children[0]
					await button.click()
					self.logger.info(f"Clicked accept button")

	async def on_message_edit(self, before, after):
		if self.selfbot['work_status'] and self.owo['status'] and after.channel.id == self.discord['channel_id'] and after.author.id == self.owo['id']:
			#Slot
			if self.gamble['slot']['mode'] and self.discord['user_nickname'] in after.content:
				#Lost
				if "won nothing" in after.content:
					self.logger.info(f"Slot turn lost {self.current_gamble_bet['slot']} cowoncy")
					self.amount['gamble'] -= self.current_gamble_bet['slot']
					self.current_gamble_bet['slot'] *= int(self.gamble['slot']['rate'])
				#Draw
				if "<:eggplant:417475705719226369> <:eggplant:417475705719226369> <:eggplant:417475705719226369>" in after.content:
					self.logger.info(f"Slot turn draw {self.current_gamble_bet['slot']} cowoncy")
				#Won x2
				if "<:heart:417475705899712522> <:heart:417475705899712522> <:heart:417475705899712522>" in after.content:
					self.logger.info(f"Slot turn won {self.current_gamble_bet['slot']} cowoncy (x2)")
					self.amount['gamble'] += self.current_gamble_bet['slot']
					self.current_gamble_bet['slot'] = int(self.gamble['slot']['bet'])
				#Won x3
				if "<:cherry:417475705178161162> <:cherry:417475705178161162> <:cherry:417475705178161162>" in after.content:
					self.logger.info(f"Slot turn won {self.current_gamble_bet['slot'] * 2} cowoncy (x3)")
					self.amount['gamble'] += self.current_gamble_bet['slot'] * 2
					self.current_gamble_bet['slot'] = int(self.gamble['slot']['bet'])
				#Won x4
				if "<:cowoncy:417475705912426496> <:cowoncy:417475705912426496> <:cowoncy:417475705912426496>" in after.content:
					self.logger.info(f"Slot turn won {self.current_gamble_bet['slot'] * 3} cowoncy (x4)")
					self.amount['gamble'] += self.current_gamble_bet['slot'] * 3
					self.current_gamble_bet['slot'] = int(self.gamble['slot']['bet'])
				#Won x10
				if "<:o_:417475705899843604> <:w_:417475705920684053> <:o_:417475705899843604>" in after.content:
					self.logger.info(f"Slot turn won {self.current_gamble_bet['slot'] * 9} cowoncy (x10)")
					self.amount['gamble'] += self.current_gamble_bet['slot'] * 9
					self.current_gamble_bet['slot'] = int(self.gamble['slot']['bet'])

			#Coinflip
			if self.gamble['coinflip']['mode'] and self.discord['user_nickname'] in after.content:
				#Lost
				if "you lost" in after.content:
					self.logger.info(f"Coinflip turn lost {self.current_gamble_bet['coinflip']} cowoncy")
					self.amount['gamble'] -= self.current_gamble_bet['coinflip']
					self.current_gamble_bet['coinflip'] *= int(self.gamble['coinflip']['rate'])
				#Won
				if "you won" in after.content:
					self.logger.info(f"Coinflip turn won {self.current_gamble_bet['coinflip']} cowoncy")
					self.amount['gamble'] += self.current_gamble_bet['coinflip']
					self.current_gamble_bet['coinflip'] = int(self.gamble['coinflip']['bet'])

		#Join giveaway
		if self.join_giveaway and after.embeds and after.id not in self.discord['giveaway_entered'] and after.author.id == self.owo['id']:
			if "New Giveaway" in str(after.embeds[0].author.name) and len(after.components) > 0:
				try:
					button = after.components[0].children[0]
					await button.click()
					self.discord['giveaway_entered'].append(after.id)
					await self.send_webhooks(
						title = "🎁 JOINED GIVEAWAY 🎁",
						description = f"{self.arrow}{after.jump_url}",
						color = discord.Colour.random()
					)
					self.logger.info(f"Joined A New Giveaway")
				except Exception as e:
					if "COMPONENT_VALIDATION_FAILED" in str(e):
						self.discord['giveaway_entered'].append(after.id)
					pass

	@tasks.loop(minutes = 1)
	async def check_owo_status(self):
		if self.selfbot['work_status'] and self.owo['status'] and self.check_owo_status.current_loop != 0:
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id']:
					break
			else:
				command = random.choice(['h', 'b'])
				await self.discord['channel'].send(f"{self.owo['prefix']}{command}")
				self.logger.info(f"Sent {self.owo['prefix']}{command}")
				self.amount['command'] += 1
				try:
					await self.wait_for("message", check=lambda m: m.channel.id == self.discord['channel_id'] and m.author.id == self.owo['id'], timeout = 10)
				except asyncio.TimeoutError:
					self.logger.warning(f"!!! OwO doesn't respond !!!")
					self.logger.info(f"Wait for 10 minutes")
					await self.send_webhooks(
						content = self.selfbot['mentioner'],
						title = "**💀 OWO'S OFFLINE 💀**",
						description = f"{self.arrow}Wait For **10 Minutes**",
						color = discord.Colour.random()
					)
					self.owo['status'] = False
					self.selfbot['work_status'] = False
					await asyncio.sleep(600)
					self.owo['status'] = True
					self.selfbot['work_status'] = True

	@tasks.loop(minutes = 1)
	async def check_2captcha_balance(self):
		if self.selfbot['work_status'] and self.twocaptcha_balance['mode']:
			if self.image_captcha['mode']:
				enoguh_balance = False
				for api_key in self.image_captcha['twocaptcha']:
					twocaptcha = TwoCaptcha(**{
								"server": "2captcha.com",
								"apiKey": str(api_key),
								"defaultTimeout": 300,
								"pollingInterval": 5
					})
					retry_times = 0
					while retry_times <= 10:
						try:
							balance = twocaptcha.balance()
							if balance >= self.twocaptcha_balance['amount']:
								enoguh_balance = True
								break
							else:
								break
						except Exception as e:
							if str(e) == "ERROR_KEY_DOES_NOT_EXIST" or str(e) == "ERROR_WRONG_USER_KEY":
								break
							else:
								retry_times += 1
								await asyncio.sleep(random.randint(3, 5))
					if enoguh_balance: break
				else:
					await self.notify()
					self.logger.warning(f"!!! Image Captcha's TwoCaptcha API has under {self.twocaptcha_balance['amount']}$ !!!")
					await self.send_webhooks(
						content = self.selfbot['mentioner'],
						title = "💸 NOT ENOUGH BALANCE 💸",
						description = f"{self.arrow}Image Captcha's TwoCaptcha API has **under {self.twocaptcha_balance['amount']}$**",
						color = discord.Colour.random()
					)
					self.selfbot['work_status'] = False
					return
			if self.hcaptcha['mode']:
				enoguh_balance = False
				for api_key in self.hcaptcha['twocaptcha']:
					twocaptcha = TwoCaptcha(**{
								"server": "2captcha.com",
								"apiKey": str(api_key),
								"defaultTimeout": 300,
								"pollingInterval": 5
					})
					retry_times = 0
					while retry_times <= 10:
						try:
							balance = twocaptcha.balance()
							if balance >= self.twocaptcha_balance['amount']:
								enoguh_balance = True
								break
							else:
								continue
						except Exception as e:
							if str(e) == "ERROR_KEY_DOES_NOT_EXIST" or str(e) == "ERROR_WRONG_USER_KEY":
								break
							else:
								retry_times += 1
								await asyncio.sleep(random.randint(3, 5))
					if enoguh_balance: break
				else:
					await self.notify()
					self.logger.warning(f"!!! HCaptcha's TwoCaptcha API has under {self.twocaptcha_balance['amount']}$ !!!")
					await self.send_webhooks(
						content = self.selfbot['mentioner'],
						title = "💸 NOT ENOUGH BALANCE 💸",
						description = f"{self.arrow}HCaptcha's TwoCaptcha API has **under {self.twocaptcha_balance['amount']}$**",
						color = discord.Colour.random()
					)
					self.selfbot['work_status'] = False
					return

	async def oauth_top_gg(self, oauth, oauth_req):
		retry_times = 0
		while retry_times <= 10:
			async with ClientSession() as session:
				payload = {"permissions": "0", "authorize": True}
				headers = {
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
					"Accept": "*/*",
					"Accept-Language": "en-US,en;q=0.5",
					"Accept-Encoding": "gzip, deflate, br",
					"Content-Type": "application/json",
					"Authorization": self.token,
					"X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExMS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTg3NTk5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
					"X-Debug-Options": "bugReporterEnabled",
					"Origin": "https://discord.com",
					"Connection": "keep-alive",
					"Referer": oauth,
					"Sec-Fetch-Dest": "empty",
					"Sec-Fetch-Mode": "cors",
					"Sec-Fetch-Site": "same-origin",
					"TE": "trailers",
				}
				async with session.post(oauth_req, headers = headers, json = payload) as res:
					if res.status == 200:
						response = await res.json()
						result_session = response.get("location")
						return result_session
					else:
						self.logger.error(f"!!! Getting top.gg oauth has the problem !!! | {await res.text()}")
						await self.send_webhooks(
							content = self.selfbot['mentioner'],
							title = "⚙️ TOP.GG OAUTH ⚙️",
							description = f"{self.arrow}Error: {await res.text()}",
							color = discord.Colour.random()
						)
			retry_times += 1
			await asyncio.sleep(random.randint(3, 5))
		else:
			await self.notify()

	@tasks.loop(hours = 12)
	async def vote_top_gg(self):
		if self.top_gg:
			options = webdriver.ChromeOptions()
			options.add_argument("--start-maximized")
			oauth = "https://discord.com/oauth2/authorize?scope=identify%20guilds%20email&redirect_uri=https%3A%2F%2Ftop.gg%2Flogin%2Fcallback&response_type=code&client_id=422087909634736160&state=Lw=="
			oauth_req = (oauth.split("/oauth2")[0] + "/api/v9/oauth2" + oauth.split("/oauth2")[1])
			top_gg = await self.oauth_top_gg(oauth, oauth_req)
			async with webdriver.Chrome(options=options) as driver:
				await driver.get(top_gg, wait_load = True, timeout = 10)
				self.logger.info(f"Loaded top.gg homepage")
				await asyncio.sleep(20)
				button = await driver.find_element(by = By.XPATH, value = '//a[@href="/bot/408785106942164992/vote"]')
				await button.click()
				self.logger.info(f"Loaded OwO vote page on top.gg")
				await asyncio.sleep(20)
				button = await driver.find_element(by=By.XPATH, value=".//button[contains(text(),'Vote')]")
				await button.click()
				self.logger.info(f"Voted OwO on top.gg")
				await asyncio.sleep(20)

	@tasks.loop(seconds = random.randint(18, 25))
	async def start_grind(self):
		try:
			if self.grind['owo'] and self.selfbot['work_status'] and self.owo['status']:
				say = random.choice(['owo', 'Owo', 'uwu', 'Uwu'])
				await self.discord['channel'].send(say)
				self.logger.info(f"Sent {say}")
				self.amount['command'] += 1
				await asyncio.sleep(random.randint(5, 10))
			if self.grind['hunt'] and self.selfbot['work_status'] and self.owo['status']:
				await self.discord['channel'].send(f"{self.owo['prefix']}h")
				self.logger.info(f"Sent {self.owo['prefix']}h")
				self.amount['command'] += 1
				await asyncio.sleep(random.randint(5, 10))
			if self.grind['battle'] and self.selfbot['work_status'] and self.owo['status']:
				await self.discord['channel'].send(f"{self.owo['prefix']}b")
				self.logger.info(f"Sent {self.owo['prefix']}b")
				self.amount['command'] += 1
				await asyncio.sleep(random.randint(5, 10))
			if self.grind['quote'] and self.selfbot['work_status'] and self.owo['status']:
				try:
					response = get("https://zenquotes.io/api/random")
					if response.status_code == 200:
						json_data = response.json()
						data = json_data[0]
						quote = data['q']
						await self.discord['channel'].send(quote)
						self.logger.info(f"Sent {quote[0:30]}...")
						self.amount['command'] += 1
				except:
					pass
		except:
			pass

	@tasks.loop(minutes = 1)
	async def claim_submit_huntbot(self):
		if self.huntbot['claim_submit'] and self.selfbot['work_status'] and self.owo['status'] and int(self.selfbot['huntbot_time']) - time.time() <= 0:
			await self.discord['channel'].send(f"{self.owo['prefix']}hb 1d")
			self.logger.info(f"Sent {self.owo['prefix']}hb 1d")
			self.amount['command'] += 1
			huntbot_message = None
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id'] and ("Please include your password" in message.content or "Here is your password!" in message.content or "BACK IN" in message.content or "BACK WITH" in message.content):
					huntbot_message = message
					break
			if huntbot_message:
				#Lost huntbot captcha
				if self.discord['user_nickname'] in message.content and "Please include your password" in huntbot_message.content:
					next_huntbot = re.findall(r"(?<=Password will reset in )(\d+)", huntbot_message.content)
					next_huntbot = int(int(next_huntbot[0]) * 60)
					self.selfbot['huntbot_time'] = next_huntbot + time.time()
					self.logger.info(f"Lost huntbot message, retry after {str(datetime.timedelta(seconds = int(next_huntbot)))} seconds")
				#Solve huntbot captcha
				if self.discord['user_nickname'] in message.content and "Here is your password!" in huntbot_message.content:
					await self.send_webhooks(
						title = "🤖 HUNTBOT CAPTCHA APPEARS 🤖",
						description = f"{self.arrow}{huntbot_message.jump_url}",
						color = discord.Colour.random(),
						image = huntbot_message.attachments[0]
					)
					checks = []
					check_images = glob.glob("huntbot/**/*.png")
					for check_image in sorted(check_images):
						img = Image.open(check_image)
						checks.append((img, img.size, check_image.split(".")[0].split(os.sep)[-1]))
					async with aiohttp.ClientSession() as session:
						async with session.get(message.attachments[0].url) as resp:
							large_image = Image.open(io.BytesIO(await resp.read()))
							large_array = np.array(large_image)

					matches = []
					for img, (small_w, small_h), letter in checks:
						small_array = np.array(img)
						mask = small_array[:, :, 3] > 0
						for y in range(large_array.shape[0] - small_h + 1):
							for x in range(large_array.shape[1] - small_w + 1):
								segment = large_array[y:y + small_h, x:x + small_w]
								if np.array_equal(segment[mask], small_array[mask]):
									if not any((m[0] - small_w < x < m[0] + small_w) and (m[1] - small_h < y < m[1] + small_h) for m in matches):
										matches.append((x, y, letter))
					matches = sorted(matches, key=lambda tup: tup[0])
					answer = "".join([i[2] for i in matches])
					await self.discord['channel'].send(f"{self.owo['prefix']}hb 1d {answer}")
					self.logger.info(f"Sent {self.owo['prefix']}hb 1d {answer}")
					self.amount['command'] += 1
					huntbot_verification_message = None
					await asyncio.sleep(random.randint(3, 5))
					async for message in self.discord['channel'].history(limit = 10):
						if message.author.id == self.owo['id'] and ("YOU SPENT" in message.content or "Wrong password" in message.content):
							huntbot_verification_message = message
							break
					if huntbot_verification_message:
						#Correct
						if self.discord['user_nickname'] in message.content and "YOU SPENT" in huntbot_verification_message.content:
							self.logger.info(f"Submitted huntbot successfully")
							await self.send_webhooks(
								title = "🎉 CORRECT SOLUTION 🎉",
								description = f"{self.arrow}**Answer:** {answer}",
								color = discord.Colour.random(),
								thumnail = huntbot_message.attachments[0]
							)
						#Incorrect
						if self.discord['user_nickname'] in message.content and "Wrong password" in huntbot_verification_message.content:
							self.logger.info(f"Submitted huntbot failed")
							await self.send_webhooks(
								title = "🚫 INCORRECT SOLUTION 🚫",
								description = f"{self.arrow}**Answer:** {answer}",
								color = discord.Colour.random(),
								thumnail = huntbot_message.attachments[0]
							)
					else:
						self.logger.error(f"Couldn't get huntbot verification message")
				#Sumbit huntbot
				elif "STILL HUNTING" in huntbot_message.content:
					next_huntbot = re.findall("[0-9]+", re.findall("`(.*?)`", huntbot_message.content)[0])
					if len(next_huntbot) == 1:
						next_huntbot = int(int(next_huntbot[0]) * 60)
					else:
						next_huntbot = int(int(next_huntbot[0]) * 3600 + int(next_huntbot[1]) * 60)
					self.selfbot['huntbot_time'] = next_huntbot + time.time()
					self.logger.info(f"Huntbot'll be back in {str(datetime.timedelta(seconds = int(next_huntbot)))} seconds")
					await self.send_webhooks(
						title = "📌 SUBMITTED HUNTBOT 📌",
						description = huntbot_message.content,
						color = discord.Colour.random()
						)
				#Claim huntbot
				elif "BACK WITH" in huntbot_message.content:
					self.logger.info(f"Claimed huntbot")
					await self.send_webhooks(
						title = "📦 CLAIMED HUNTBOT 📦",
						description = huntbot_message.content,
						color = discord.Colour.random()
						)
					self.amount['huntbot'] += 1
					if self.huntbot['upgrade']['mode']:
						await self.discord['channel'].send(f"{self.owo['prefix']}upgrade {self.huntbot['upgrade']['type']} all")
						self.logger.info(f"Sent {self.owo['prefix']}upgrade {self.huntbot['upgrade']['type']} all")
						self.amount['command'] += 1
			else:
				self.logger.error(f"Couldn't get huntbot message")

	@tasks.loop(seconds = random.randint(600, 1200))
	async def check_distorted_animal(self):
		if self.distorted_animals and self.selfbot['work_status'] and self.owo['status'] and self.selfbot['glitch_time'] - time.time() <= 0:
			await self.discord['channel'].send(f"{self.owo['prefix']}dt")
			self.logger.info(f"Sent {self.owo['prefix']}dt")
			self.amount['command'] += 1
			glitch_message = None
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id'] and ("are available" in message.content or "not available" in message.content):
					glitch_message = message
					break
			if glitch_message:
				if "are available" in glitch_message.content:
					glitch_end = [i for i in re.findall("[0-9]+", glitch_message.content) if int(i) <= 60]
					if len(glitch_end) == 1:
						glitch_end = int(glitch_end[0])
					elif len(glitch_end) == 2:
						glitch_end = int(int(glitch_end[0]) * 60 + int(glitch_end[1]))
					elif len(glitch_end) == 3:
						glitch_end = int(int(glitch_end[0]) * 3600 + int(glitch_end[1]) * 60 + int(glitch_end[2]))
					self.selfbot['glitch_time'] = glitch_end + time.time()
					self.logger.info(f"Distorted animals are available for {str(datetime.timedelta(seconds = int(glitch_end)))} seconds")
				elif "not available" in glitch_message.content:
					self.logger.info(f"Distorted animals aren't available")
			else:
				self.logger.error(f"Couldn't get distorted animals message")
		self.current_loop['check_distorted_animal'] += 1

	@tasks.loop(seconds = random.randint(1200, 3600))
	async def sell_sac_animal(self):
		if self.animals['mode'] and self.selfbot['work_status'] and self.owo['status']:
			await self.discord['channel'].send(f"{self.owo['prefix']}{self.animals['type']} {self.animals['rank']}")
			self.logger.info(f"Sent {self.owo['prefix']}{self.animals['type']} {self.animals['rank']}")
			self.amount['command'] += 1

	@tasks.loop(minutes = 1)
	async def claim_daily(self):
		if self.daily and self.selfbot['work_status'] and self.owo['status'] and int(self.selfbot['daily_time']) - time.time() <= 0:
			await self.discord['channel'].send(f"{self.owo['prefix']}daily")
			self.logger.info(f"Sent {self.owo['prefix']}daily")
			self.amount['command'] += 1
			daily_message = None
			await asyncio.sleep(random.randint(3, 5))
			async for message in self.discord['channel'].history(limit = 10):
				if message.author.id == self.owo['id'] and self.discord['user_nickname'] in message.content and ("next daily" in message.content or "Nu" in message.content):
					daily_message = message
					break
			if daily_message:
				if "Nu" in daily_message.content:
					next_daily = re.findall("[0-9]+", daily_message.content)
					next_daily = int(int(next_daily[0]) * 3600 + int(next_daily[1]) * 60 + int(next_daily[2]))
					self.selfbot['daily_time'] = next_daily + time.time()
					self.logger.info(f"Claim daily after {str(datetime.timedelta(seconds = int(next_daily)))} seconds")
				elif "Your next daily" in daily_message.content:
					self.logger.info(f"Claimed daily")
			else:
				self.logger.error(f"Couldn't get daily message")
		self.current_loop['daily'] += 1

	@tasks.loop(minutes = 1)
	async def go_to_sleep(self):
		if self.sleep and self.selfbot['work_status'] and self.owo['status'] and int(self.selfbot['work_time']) - time.time() <= 0:
			self.selfbot['sleep_time'] = random.randint(300, 600)
			self.logger.info(f"Take A Break For {self.selfbot['sleep_time']} Seconds")
			await self.send_webhooks(
				title = "🛌 TAKE A BREAK 🛌",
				description = f"{self.arrow}Take a break for **__{self.selfbot['sleep_time']}__ seconds**",
				color = discord.Colour.random()
				)
			self.selfbot['work_status'] = False
			await asyncio.sleep(self.selfbot['sleep_time'])
			self.selfbot['work_time'] = random.randint(600, 1200)
			self.logger.info(f"Done! Work for {self.selfbot['work_time']} seconds")
			await self.send_webhooks(
				title = "🌄 WOKE UP 🌄",
				description = f"{self.arrow}Work for **__{self.selfbot['work_time']}__ seconds**",
				color = discord.Colour.random()
			)
			self.selfbot['work_time'] += time.time()
			self.selfbot['work_status'] = True
			self.amount['sleep'] += 1

	@tasks.loop(seconds = random.randint(60, 120))
	async def play_gamble(self):
		#Slot
		if self.gamble['slot']['mode'] and self.selfbot['work_status'] and self.owo['status']:
			if self.current_gamble_bet['slot'] >= int(self.gamble['slot']['max']):
				self.current_gamble_bet['slot'] = int(self.gamble['slot']['bet'])
			await self.discord['channel'].send(f"{self.owo['prefix']}s {self.current_gamble_bet['slot']}")
			self.logger.info(f"Sent {self.owo['prefix']}s {self.current_gamble_bet['slot']}")
			self.amount['command'] += 1
			await asyncio.sleep(random.randint(3, 5))
		#Coinflip
		if self.gamble['coinflip']['mode'] and self.selfbot['work_status'] and self.owo['status']:
			if self.current_gamble_bet['coinflip'] >= int(self.gamble['coinflip']['max']):
				self.current_gamble_bet['coinflip'] = int(self.gamble['coinflip']['bet'])
			side = random.choice(['h', 't'])
			await self.discord['channel'].send(f"{self.owo['prefix']}cf {self.current_gamble_bet['coinflip']} {side}")
			self.logger.info(f"Sent {self.owo['prefix']}cf {self.current_gamble_bet['coinflip']} {side}")
			self.amount['command'] += 1
			await asyncio.sleep(random.randint(3, 5))
		#Blackjack
		if self.gamble['blackjack']['mode'] and self.selfbot['work_status'] and self.owo['status']:
			if self.current_gamble_bet['blackjack'] >= int(self.gamble['blackjack']['max']):
				self.current_gamble_bet['blackjack'] = int(self.gamble['blackjack']['bet'])
			await self.discord['channel'].send(f"{self.owo['prefix']}bj {self.current_gamble_bet['blackjack']}")
			self.logger.info(f"Sent {self.owo['prefix']}bj {self.current_gamble_bet['blackjack']}")
			self.amount['command'] += 1
			self.checking['is_blackjack'] = False
			while not self.checking['is_blackjack']:
				blackjack_message = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit = 10):
					if message.channel.id == self.discord['channel_id'] and message.author.id == self.owo['id'] and message.embeds:
						if str(self.user) in message.embeds[0].author.name and "play blackjack" in message.embeds[0].author.name:
							blackjack_message = message
							break
				if blackjack_message:
					if "in progress" in blackjack_message.embeds[0].footer.text or "resuming previous" in blackjack_message.embeds[0].footer.text:
						my_blackjack_point = int(re.findall(r"\[(.*?)\]", blackjack_message.embeds[0].fields[1].name)[0])
						if my_blackjack_point <= 17:
							try:
								if blackjack_message.reactions[0].emoji == "👊":
									if blackjack_message.reactions[0].me:
										await blackjack_message.remove_reaction('👊', self.user)
									else:
										await blackjack_message.add_reaction('👊')
								else:
									if blackjack_message.reactions[1].me:
										await blackjack_message.remove_reaction('👊', self.user)
									else:
										await blackjack_message.add_reaction('👊')
								self.logger.info(f"Blackjack turn has {my_blackjack_point} points (Hit)")
							except IndexError:
								pass
						else:
							await blackjack_message.add_reaction('🛑')
							self.logger.info(f"Blackjack turn has {my_blackjack_point} points (Stand)")
					elif "You won" in blackjack_message.embeds[0].footer.text:
						self.logger.info(f"Blackjack turn won {self.current_gamble_bet['blackjack']} cowoncy")
						self.amount['gamble'] += self.current_gamble_bet['blackjack']
						self.current_gamble_bet['blackjack'] = int(self.gamble['blackjack']['bet'])
						self.checking['is_blackjack'] = True
					elif "You lost" in blackjack_message.embeds[0].footer.text:
						self.logger.info(f"Blackjack turn lost {self.current_gamble_bet['blackjack']} cowoncy")
						self.amount['gamble'] -= self.current_gamble_bet['blackjack']
						self.current_gamble_bet['blackjack'] *= int(self.gamble['blackjack']['rate'])
						self.checking['is_blackjack'] = True
					elif "You tied" in blackjack_message.embeds[0].footer.text or "You both bust" in blackjack_message.embeds[0].footer.text:
						self.logger.info(f"Blackjack turn draw {self.current_gamble_bet['blackjack']} cowoncy")
						self.checking['is_blackjack'] = True
				else:
					break

	@tasks.loop(seconds = random.randint(300, 600))
	async def start_pray_curse(self):
		if self.pray_curse['mode'] and self.selfbot['work_status'] and self.owo['status']:
			#Pray
			if self.pray_curse['type'].lower() == "pray":
				await self.discord['channel'].send(f"{self.owo['prefix']}pray {self.pray_curse['user_id']}")
				self.logger.info(f"Sent {self.owo['prefix']}pray {self.pray_curse['user_id']}")
				self.amount['command'] += 1
			#Curse
			else:
				await self.discord['channel'].send(f"{self.owo['prefix']}curse <@{self.pray_curse['user_id']}>")
				self.logger.info(f"Sent {self.owo['prefix']}curse <@{self.pray_curse['user_id']}>")
				self.amount['command'] += 1

	@tasks.loop(seconds = random.randint(60, 120))
	async def start_entertainment(self):
		if self.selfbot['work_status'] and self.owo['status']:
			if self.daily and int(self.selfbot['daily_time']) - time.time() <= 0 and self.current_loop['daily'] > 0:
				self.checking['run_limit'] = False
				self.checking['pup_limit'] = False
				self.checking['piku_limit'] = False
			#Run
			if self.entertainment['run'] and not self.checking['run_limit']:
				await self.discord['channel'].send(f"{self.owo['prefix']}run")
				self.logger.info(f"Sent {self.owo['prefix']}run")
				self.amount['command'] += 1
				run_message = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit = 10):
					if message.author.id == self.owo['id'] and "tired to run" in message.content:
						run_message = message
						break
				if run_message:
					self.logger.info(f"Run for today is over")
					self.checking['run_limit'] = True
			#Pup
			if self.entertainment['pup'] and not self.checking['pup_limit']:
				await self.discord['channel'].send(f"{self.owo['prefix']}pup")
				self.logger.info(f"Sent {self.owo['prefix']}pup")
				self.amount['command'] += 1
				pup_message = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit = 10):
					if message.author.id == self.owo['id'] and "no puppies" in message.content:
						pup_message = message
						break
				if pup_message:
					self.logger.info(f"Pup for today is over")
					self.checking['pup_limit'] = True
			#Piku
			if self.entertainment['piku'] and not self.checking['piku_limit']:
				await self.discord['channel'].send(f"{self.owo['prefix']}piku")
				self.logger.info(f"Sent {self.owo['prefix']}piku")
				self.amount['command'] += 1
				piku_message = None
				await asyncio.sleep(random.randint(3, 5))
				async for message in self.discord['channel'].history(limit = 10):
					if message.author.id == self.owo['id'] and "out of carrots" in message.content:
						piku_message = message
						break
				if piku_message:
					self.logger.info(f"Piku for today is over")
					self.checking['piku_limit'] = True

print()
print(f"{color.bold}You Are Using{color.reset} {color.red}OwO's Selfbot{color.reset} {color.bold}By{color.reset} {color.blue}Phandat (realphandat){color.reset} {color.bold}And{color.reset} {color.pink}His Love (selena){color.reset}")
print(f"{color.bold}Created With{color.reset} {color.yellow}Great Contributions{color.reset} {color.bold}From{color.reset} {color.green}aduck (ahihiyou20){color.reset} {color.bold}And{color.reset} {color.green}Cex (cesxos){color.reset} {color.bold}And{color.reset} {color.green}Nouzanlong - 努赞龙 (tcb_nouzanlong){color.reset}")
print()

config = json.load(open("config.json"))
threads = []
for token in config:
	Client = MyClient(token)
	thread = threading.Thread(target=Client.run, args=(token,))
	threads.append(thread)
	thread.start()
for thread in threads:
	thread.join()