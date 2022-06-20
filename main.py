from lib2to3.pgen2 import token
import discord 
from discord.ext import commands, tasks 
import logging
import json
import requests
import time 
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
CHANNELID = int(os.getenv('CHANNELID'))
TOKEN= os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Bot is ready')
    await holywater()

@bot.command()
async def ping(ctx):
    await ctx.send('pooong')
    

@tasks.loop()
async def holywater():
    while True:
        channel = bot.get_channel(CHANNELID)
        currentTime = time.time()
        thenTime = currentTime + 28800
        waitTime = thenTime - currentTime
        await asyncio.sleep(waitTime)

        await channel.send("Fetching data")
        url = 'https://www.reddit.com/r/GameDeals/new/.json'
        # Do the HTTP get request
        response = requests.get(url, headers = {'User-agent': 'Your Friend Jack'}).json()
        i=0

        for games in response['data']['children']:
            
            postTime = response['data']['children'][i]['data']['created_utc']
            gameTitle = response['data']['children'][i]['data']['title']
            gameUrl = response['data']['children'][i]['data']['url']
            # check if the post is less than or equal to 8 hours old
            if currentTime - postTime <= 28800: 
                await channel.send(f"""{gameTitle}
                {gameUrl}""")
                i+=1
            else:
                break

bot.run(TOKEN)