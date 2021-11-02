#Discord imports
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
#Other imports
import time
#Own imports
import utils
import responses

class BaumBot:
    def __init__(self, token=None):
        self.token = token

        self.client = commands.Bot(command_prefix=".")
        self.slash = SlashCommand(self.client, sync_commands=True)
        self.responses = responses.Response()
        self.voice_channel = None

        self.init_events()
        self.init_commands()

    def run(self):
        self.client.run(self.token)

    def init_events(self):
        @self.client.event
        async def on_ready(): #Show registration data on load-up e.g. 'BaumBot#4721' in console
        	print('We have logged in as {0.user}'.format(self.client))

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
            	return
            await message.channel.send(self.responses.responde(message.content))

    def init_commands(self):
        @self.slash.slash(name="join", description="BaumBot joins the channel of the command author")
        async def join(context: SlashContext):
            self.voice_channel = await utils.check_and_join(self.voice_channel, context)

        @self.slash.slash(name="leave", description="BaumBot leaves its current voice channel")
        async def leave(context: SlashContext):
            await utils.check_and_leave(self.voice_channel)
            await context.send('I am leaving: "{}"'.format(context.author.voice.channel.name))
            self.voice_channel = None

        @self.slash.slash(name="test", description="A simple test function")
        async def test(context: SlashContext):
            await context.send('callback from client')

        @self.slash.slash(name="ping", description="Speed Test for the BaumBot")
        async def ping(context: SlashContext):
            await context.send('BaumBot Speed: {}ms'.format(round(self.client.latency * 1000), 0))


if __name__ == '__main__':
    token = 'ODkzNTU4MzM5Mjk0ODgzOTEw.YVdNDQ.i-d5auCOMnXh2aH6J5nnxtMvoxs'
    baumBot = BaumBot(token)
    baumBot.run()
