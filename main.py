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
        then = currentTime + 3600
        waitTime = then - currentTime
        await asyncio.sleep(waitTime)

        await channel.send("Fetching data")
        url = 'https://www.reddit.com/r/GameDeals/new/.json'
        # Do the HTTP get request
        response = requests.get(url, headers = {'User-agent': 'Your Friend Jack'}).json()
        i=0

        for games in response['data']['children']:
            
            postTime = response['data']['children'][i]['data']['created_utc']
            # check if the post is less than or equal to 24 hours old
            if currentTime - postTime <= 3600: 
                await channel.send(response['data']['children'][i]['data']['title'])
                await channel.send(response['data']['children'][i]['data']['url'])
                i+=1
            else:
                break

bot.run(TOKEN)