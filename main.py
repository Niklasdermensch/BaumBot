#Discord imports
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
#Other imports
import time
#Own imports
import utils
import responses
import clients

class BaumBot:
    def __init__(self, token=None):
        self.token = token

        self.client = commands.Bot(command_prefix=".")
        self.slash = SlashCommand(self.client, sync_commands=True)
        self.voice_channel = None

        self.init_clients()
        self.init_events()
        self.init_commands()

    def run(self):
        self.client.run(self.token)

    def init_clients(self):
        self.responses = responses.Response()
        self.reddit_client = clients.RedditClient()
        self.porn_client = clients.PornClient()
        self.music_client = clients.MusicClient()
        self.stock_client = clients.StockClient()

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
        #DEBUG commands
        @self.slash.slash(name="test", description="A simple test function")
        async def test(context: SlashContext):
            await context.send('callback from client')

        @self.slash.slash(name="ping", description="Speed Test for the BaumBot")
        async def ping(context: SlashContext):
            await context.send('BaumBot Speed: {}ms'.format(round(self.client.latency * 1000), 0))

        @self.slash.slash(name="shutdown", description="Shuts down the BaumBot. Cannot be undone!")
        async def shutdown(context: SlashContext):
            await context.send('Goodbye 👋')
            quit()

        #Channel commands
        @self.slash.slash(name="join", description="BaumBot joins the channel of the command author")
        async def join(context: SlashContext):
            self.voice_channel = await utils.check_and_join(self.voice_channel, context)

        @self.slash.slash(name="leave", description="BaumBot leaves its current voice channel")
        async def leave(context: SlashContext):
            await utils.check_and_leave(self.voice_channel)
            await context.send('I am leaving: "{}"'.format(context.author.voice.channel.name))
            self.voice_channel = None

        #Reddit client calls
        @self.slash.slash(name="randomsubreddit", description="Gives back a random subreddit link",
                          options=[create_option(name="nsfw", description="Include, Exclude or Exclusive NSFW", option_type=3, required=False, choices=[
                                                 create_choice(name="Yes", value="yes"),
                                                 create_choice(name="No", value="no"),
                                                 create_choice(name="Only", value="only")]),
                                   create_option(name="count", description="Number of returned subreddit link", option_type=4, required=False),
                                   create_option(name="sort", description="Returned link sort by (e.g. new, hot, top)", option_type=3, required=False, choices=[
                                                 create_choice(name="New", value="/new"),
                                                 create_choice(name="Hot", value="/"),
                                                 create_choice(name="TopHour", value="/top/?t=hour"),
                                                 create_choice(name="TopDay", value="/top/?t=day"),
                                                 create_choice(name="TopMonth", value="/top/?t=month"),
                                                 create_choice(name="TopYear", value="top_year': '/top/?t=year"),
                                                 create_choice(name="TopAll", value="/top/?t=all")])])
        async def randomsubreddit(context: SlashContext, nsfw: str ="yes", count: int =1, sort: str ="/top/?t=all"):
            if count > self.reddit_client.max_responses:
                await context.send("Max. Responses are: " + str(self.reddit_client.max_responses))
            await context.defer()
            await context.send(self.reddit_client.get_random_subreddit(NSFW=nsfw, count=count, sort=sort))

        #TODO Random Post
        #TODO Memes of the day

        #Music client calls
        #TODO Play
        #TODO Stop
        #TODO Queue -> push -> yeet -> delete
        #TODO Spotify Ingetration
        #TODO Repeat
        #TODO radio <genre>

        #Porn client calls
        #TODO Random porn
        #TODO Random category
        #TODO Random porn star
        #TODO Random porn page

        #Stock client calls?
        #Finance system? <- pls no

        #Discord Bot Games (TicTacToe, Chess, etc) calls?


if __name__ == '__main__':
    token_file = open('safe/token.txt', 'r')
    Lines = token_file.readlines()
    for line in Lines:
        token = line.split('\n')[0]
    baumBot = BaumBot(token)
    baumBot.run()
