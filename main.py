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
from bs4 import BeautifulSoup


load_dotenv()
CHANNELID = int(os.getenv('CHANNELID'))
TOKEN= os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Bot is ready')
    await supplements()
    await grabFreeGames()

@bot.command()
async def ping(ctx):
    await ctx.send('pooong')

@tasks.loop()
async def supplements():
    currentData = []

    while True:
        channel = bot.get_channel(CHANNELID)
        currentTime = time.time()
        thenTime = currentTime + 1800
        waitTime = thenTime - currentTime
        await asyncio.sleep(waitTime)

        url = 'https://supplementhunt.com/pages/last-chance'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        section = soup.find('div', attrs = {'id':'63adad6a-2628-45b7-85b8-50da266a21ad'}) 
        sectionItems = section.findAll('li')
        itemData = []

        for item in sectionItems:
            itemTitle = item.h2.get_text()
            itemOPriceDiv = item.find(class_= 'price__compare-at')
            itemOPrice= itemOPriceDiv.find(class_ = 'money').get_text()
            itemCPriceDiv = item.find(class_= 'price__current')
            itemCPrice= itemCPriceDiv.find(class_ = 'money').get_text()
            itemUrl = item.a['href']
            actualUrl = f'https://supplementhunt.com/{itemUrl}'

            itemData.append(itemUrl)

            if itemUrl not in currentData:
                await channel.send(f'{itemTitle}\nOrginal Price: {itemOPrice}\nSale Price: {itemCPrice}\n{actualUrl}')

        currentData = itemData
        itemData= []


@tasks.loop()
async def grabFreeGames():
    while True:
        channel = bot.get_channel(CHANNELID)
        currentTime = time.time()
        thenTime = currentTime + 43200
        waitTime = thenTime - currentTime
        await asyncio.sleep(waitTime)

        url = 'https://www.reddit.com/r/GameDeals/new/.json'
        # Do the HTTP get request
        response = requests.get(url, headers = {'User-agent': 'Your Friend Jack'}).json()
        i=0

        for games in response['data']['children']:
            
            postTime = response['data']['children'][i]['data']['created_utc']
            gameTitle = response['data']['children'][i]['data']['title']
            gameUrl = response['data']['children'][i]['data']['url']
            # check if the post is less than or equal to 12 hours old
            if currentTime - postTime <= 43200: 
                await channel.send(f"""{gameTitle}
                {gameUrl}""")
                i+=1
            else:
                break

bot.run(TOKEN)