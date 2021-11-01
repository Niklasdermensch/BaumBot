import discord
import os
import platform
import requests
import json
import random
import asyncio
import nacl
import pandas as pd

import youtube_dl
import randomreddit
import all_commands

client = discord.Client()
vc = None # current voice channel

music_queue = []
sad_words = ["traurig", "deprimiert", "unglücklich", "wütend", "niedergeschlagen", "depressiv"]
starter_encouragements = ["Heul net rum!", "Heul leise!", "Is mir egal!"]
insults = [
	["Lieber", ", zur Zeit ist das Beleidigungs-Feature in Bearbeitung. Beleidige dich bitte in der Zwischenzeit selber. Danke."],
	["", " du bist so hässlich, als deine Mutter dich in der Schule absetzte, bekam sie eine Strafe für Müll."],
	["", " muss auf einer Autobahn geboren worden sein, denn dort passieren die meisten Unfälle."],
	["Rosen sind rot, Veilchen sind blau, Gott hat mich hübsch gemacht, was ist mit", " passiert?"],
	["Einige Babys wurden auf ihren Kopf fallen gelassen, aber", " wurde eindeutig an eine Wand geworfen."],
	["", ", warum spielst du nicht im Verkehr?"],
	["Ich weiß nicht, was", "'s Problem ist, aber ich wette, es ist schwer auszusprechen."],
	["Du", ", bist wie Montagmorgen, niemand mag dich."],
	["Du", ", bist so fett, du könntest Schatten verkaufen."],
	["Jedes Mal, wenn ich neben", " bin, bekomme ich den heftigen Wunsch, allein zu sein."],
	["", " wurde in einer finsteren Gasse gezeugt. Was ein Hurensohn!"],
	["", ", du bist so trash, dass du Müll bist"],
	["als", " erschaffen wurde, hatte Gott einen Schlaganfall. Bruh!"],
	["", "'s Geburtsurkunde ist ein Entschuldigungsschreiben von einem Kondom-Hersteller"],
	]
ydl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

def get_quote():
	response = requests.get('https://zenquotes.io/api/random')
	json_data = json.loads(response.text)
	#quote = translator.translate(json_data[0]['q']) + '\n\t-' + json_data[0]['a']
	quote = json_data[0]['q'] + '\n\t-' + json_data[0]['a']
	return quote

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	global vc

	if message.author == client.user:
		return

	if message.content.startswith('/help'): #v
		await message.channel.send(all_commands.print_all_commands())

	elif message.content.startswith('/hallo'): #v
		await message.channel.send('Hallo :)')

	elif message.content.startswith('/inspire'): #v
		await message.channel.send(get_quote())

	elif any(word in message.content for word in sad_words):
		await message.channel.send(random.choice(starter_encouragements))

	elif message.content.startswith('/insult'): #v
		username = message.content.split('/insult', 1)[1]
		choice = insults[0]
		await message.channel.send(choice[0] + username + choice[1])

	elif message.content.startswith('/randomreddit'): #v
		await message.channel.send(randomreddit.get_subreddit())

	elif message.content.startswith('/Sieg'): #v
		await message.channel.send('𝕳𝖊𝖎𝖑')

	elif message.content.startswith('/join'): #v
		vc = await message.author.voice.channel.connect()

	elif message.content.startswith('/leave'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()
		await vc.disconnect()
		vc = None

	elif message.content.startswith('/heehee'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('HeeHee.mp3'))

	elif message.content.startswith('/rrr'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('rrr.mp3'))

	elif message.content.startswith('/hoyaa'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('hoyaa.mp3'))

	elif("lmao" in message.content or "Lmao" in message.content or "LMAO" in message.content):
		await message.channel.send('lmao')


	elif message.content.startswith('/speakas'): #v
		name = message.content.split('/speakas ', 1)[1]
		if not vc:
			vc = await message.author.voice.channel.connect()

		if name == "Johannes" or name == "johannes":
			vc.play(discord.FFmpegPCMAudio('johannes.mp3'))


	elif message.content.startswith('/play'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()

		video_link = message.content.split('/play', 1)[1]

		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				info = ydl.extract_info(video_link, download=False)
				url = info['entries'][0]['url']
				vc.play(discord.FFmpegPCMAudio(url))
		except:
			music_queue.append(video_link)

		"""
		Allgemeine Queue implementieren
		-> D.h. jedes Video kommt in die Queue
		-> Thread schaut ob die Queue gefüllt ist und ob gerade ein song spielt, sonst nächster song in der queue

		+ next song command
		+ empty queue command
		+ now! command
		+ repeat_current [number]
		"""

	elif message.content.startswith('/stop'): #v
		try:
			vc.stop()
		except:
			pass

	elif message.content.startswith('/Yamete'):
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('Yamete.mp3'))

	elif message.content.startswith('/Moan'):
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('moan.mp3'))

client.run('ODkzNTU4MzM5Mjk0ODgzOTEw.YVdNDQ.eUttYwnWcuA2DuBYDpxWHcGCPyU')