import discord
import asyncio
import os
import requests
import json
import YahooFinanceScrubber as scrubber
from bs4 import BeautifulSoup
import DotabuffCounters as dbc

client = discord.Client()
token = 'NjExNzM4NzQ5NjIwOTc3NzE0.XVYMtw.TiIvQJ1nUStn2_FtKmOvYFNSlpg'

@client.event
async def on_ready():
    print("Initializing bot...")

    print("Logged in with:")
    print("Name: " + client.user.name)
    print("ID: " + str(client.user.id))
    print("------")

@client.event
async def on_message(message):
    splitMessage = message.content.split()

    if message.author.id == client.user.id:
        return
    else:
        print(message.author.name + " (" + str(message.author.id) + "): \"" + message.content + "\"")

    if message.author == client.user:
        return

    if message.content.startswith('?hello'):
        channel = message.channel
        msg = 'Hello {0.author.mention}'.format(message)
        await channel.send(msg)

    if message.content.startswith('?help'):
        channel = message.channel
        await channel.send("Type '?hello' for a greeting")
        await channel.send("Type '?stock' to look up the current stock price using the stock symbol (ie AAPL, BA, GOOG)")
        await channel.send("Type '?dotacounter' to look up the counters to a DotA hero using the hero name or nickname (ie AM, Wyvern, QOP)")

    if message.content.startswith('?stock'):
        channel = message.channel
        msg = splitMessage
        if len(msg) >=2:
            msg_to_print = scrubber.stock_lookup(msg[1])
            name = scrubber.stock_name(msg[1])
            if isinstance(msg_to_print, dict):
                await channel.send('Please enter a correct stock symbol (ie AAPL, BA, GOOG).')
            else:
                await channel.send('The current price for ' + name + ' (' + msg[1].upper() + ')' + ' is $' + str(msg_to_print))
        else:
            await channel.send('Please enter a stock symbol.')


    if message.content.startswith('?dotacounter'):
        channel = message.channel
        msg = splitMessage
        if len(msg)>= 2:
            heroes_list = dbc.get_heroes_list()
            nickname_dict = dbc.heroes_nickname_dict()
            hero_name = dbc.get_hero_name(msg[1:], nickname_dict, heroes_list)
            msg_to_print = dbc.get_counter(hero_name, heroes_list, nickname_dict)
            if 'nickname' in msg_to_print:
                await channel.send(msg_to_print + '. ' + hero_name + ' is an invalid hero name or nickname.')
                return
            else:
                if 'Mage' in hero_name or 'mage' in hero_name:
                    await channel.send('The counters for ' + hero_name.title() + ' are ' + msg_to_print)
                else:
                    hero_name = hero_name.replace('-', ' ')
                    await channel.send('The counters for ' + hero_name.title() + ' are ' + msg_to_print)
        else:
            await channel.send('Please enter a DotA hero name.')
client.run(token)