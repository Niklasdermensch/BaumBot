#Discord imports
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
#Other imports
import time
#Own imports
import utils

class BaumBot:
    def __init__(self, token=None):
        self.token = token

        self.client = commands.Bot(command_prefix=".")
        self.slash = SlashCommand(self.client)
        self.voice_channel = None

        self.init_events()
        self.init_commands()

    def run(self):
        self.client.run(self.token)

    def init_events(self):
        @self.client.event
        async def on_ready(): #Show registration data on load-up e.g. 'BaumBot#4721'
        	print('We have logged in as {0.user}'.format(self.client))

        @self.client.event
        async def on_message(message):
            pass

    def init_commands(self):
        @self.slash.slash(name="join", description="BaumBot joins the channel of the message author")
        async def join(context: SlashContext):
            self.voice_channel = await utils.check_and_join(self.voice_channel, context)

        @self.slash.slash(name="leave", description="BaumBot leaves its current voice channel")
        async def leave(context: SlashContext):
            await utils.check_and_leave(self.voice_channel, context)
            self.voice_channel = None
            #- Not in any channel

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
