import discord
from discord.ext import tasks, commands

import asyncio

import random
import requests
import json
import time



#Bot initialization, intents, client, prefix, etc.

intents = discord.Intents(
  messages = True,
  guilds = True,
  reactions = True,
  members = True,
  presences = True
)

client = commands.Bot(command_prefix = '!', intents = intents)

#Bot authorization
@client.event
async def on_ready():
  print("<Personal bot is functioning>")

@tasks.loop(seconds=10)
async def printer():
  await ctx.send('hi')
  
@client.command()
async def ping(ctx):
    await ctx.send("Pong")


client.run('TOKEN')
