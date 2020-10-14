import discord
from discord.ext import commands
import random

#Server ID: Cheese Land: 747893214521983066
#Server ID: GP Test Server: 753270708687077446
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '!', intents = intents)

channel = client.get_channel('753270708687077446')

#Bot authorization
@client.event
async def on_ready():
    print('Bot is ready.')

#Leaving/Join Shell Response
@client.event
async def on_member_join(member):
    print("Hello idot, why are you here?")

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server. LMAO good riddance')

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
            message.channel.send("They're admin so I can't kick them smh...")

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

#Run client key
#This isn't the key anymore - so don't try anything
client.run('NzYzOTY2OTg3MzEwOTg5MzEz.X3_Zsw.vjpnFNNdZfdT1Oz96cfa3GXYrMk')

