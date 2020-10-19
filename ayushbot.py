#discord modules
import discord
from discord.ext import commands

#webscraping modules
import random
import requests
import json
from pprint import pprint


#Server ID: Cheese Land: 747893214521983066
#Server ID: GP Test Server: 753270708687077446

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '!', intents = intents)

channel = client.get_channel('753270708687077446')

#Bot authorization
@client.event
async def on_ready():
    print('Bot is ready.')



@client.event
async def on_message(message):
    #Kick user for spam
    limit = random.randint(250,1000)
    member = message.author
    if len(str(message.content)) > limit:
        limit_exceed = discord.Embed(
                title = 'Exceeded Character Limit - Spam Detected',
                description = f"{message.author} - You exceeded character limit idiot! - ({limit})",
                color = discord.Color.green()
            )
        try:
            if message.author != discord.Permissions.administrator:
                await member.kick(reason='Exceeded Character Limit')
                await message.channel.send(embed=limit_exceed)

        except:
            await message.channel.send("They're admin so I can't kick them smh...")

    #Ayush reaction
    if "Ayush" in message.content or "ayush" in message.content:
        emoji = '\N{THUMBS UP SIGN}'
        await message.add_reaction(emoji)

    await client.process_commands(message)

#Commands -- Ayush Bot -- Client Side -- Ping

#Ping Command
@client.command()
async def ping(ctx):
    await ctx.send("stfu loser stop bothering me")

#Predict Command
@client.command()
async def predict(ctx, *, question):
    responses = [
    "Definitely!",
    "Yes, more probable than you failing a test - 100",
    "Uhhhh...sure why not",
    "Yeah okay lets go with that",
    "Kinda sorta likely idk",
    "Idk why are you asking me",
    "Ask me later I'm playing minecraft",
    "If I told you I would have to kill you",
    "Don't count on it bud",
    "Hell no, def not",
    "Doubtful smh my head is shake is smh",
    "Nobody cares, don't use this function again"
    ]

    await ctx.send(random.choice(responses))

#WhoAsked Command
@client.command()
async def whoasked(ctx):
    f = discord.File('C:/Users/ayush/OneDrive/Desktop/didiask.png', filename="didiask.png")
    e = discord.Embed()
    await ctx.send(file=f,embed=e)

#Bedwars Hypixel Statistics
@client.command()
async def bedwars(ctx, userid):
    try:
        api_key = '5020df31-ed85-4bcb-b572-dfd3f03184d5'
        user = str(userid)
        complete_url = "https://api.hypixel.net/player?key=" + api_key + "&name=" + user
        data = requests.get(complete_url).json()
        '''
        pprint(data["player"]["stats"]["Bedwars"])
        '''
        #General Statistics
        coins = data["player"]["stats"]["Bedwars"]["coins"]
        final_kills = data["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
        final_deaths = data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
        wins = data["player"]["stats"]["Bedwars"]["wins_bedwars"]
        winstreak = data["player"]["stats"]["Bedwars"]["winstreak"]
        
        #Solo Bedwars Statistics
        solo_wins = data["player"]["stats"]["Bedwars"]["eight_one_wins_bedwars"]
        
        #Doubles Bedwars
        doubles_wins = data["player"]["stats"]["Bedwars"]["eight_two_wins_bedwars"]
        
        #Create embed
        embed = discord.Embed(
                title = userid + " Bedwars Stats",
                description = "Hypixel API New Stat Generator",
                color = discord.Color.green()
            )
        embed.set_footer(text='Recently updated statistics . . .')
        embed.set_author(name="Hypixel Stats",
        icon_url='https://media.discordapp.net/attachments/753270708687077449/767454420422098994/Z.png')

        embed.add_field(name='General Statistics',
                        value= (str(coins) + " coins" + '\n') +(str(wins) + " wins" + '\n') + (str(final_kills) + " final kills" + " ---  ") + (str(final_deaths) + " final deaths" + '\n') + (str(winstreak) + " winstreak")
                        ,inline = False)
        embed.add_field(name='Solo Bedwars', value = str(solo_wins) + " solo wins", inline=True)
        embed.add_field(name='Doubles Bedwars', value = str(doubles_wins) + " doubles wins", inline=True)
        await ctx.send(embed=embed)
    except:
        await ctx.send("No player found")


#Run client key
client.run('NzYzOTY2OTg3MzEwOTg5MzEz.X3_Zsw.32bRceKDVLQT-N_qTRYxfdClXds')
