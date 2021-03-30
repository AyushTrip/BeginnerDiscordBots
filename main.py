#Import discord modules
import discord
from discord.ext import commands
import asyncio

#Webscraping modules
import random
import requests
import json
import time

#Intents variable - variable to determine what the discord bot is allowed to do in the server
intents = discord.Intents(
  messages = True, 
  guilds = True, 
  reactions = True, 
  members = True, 
  presences = True)

#Client prefix - sets the command variable prefix to use the discord bot
client = commands.Bot(command_prefix = '!', intents = intents)


#Bot authorization
@client.event
async def on_ready():
  print("<APCSP Bot is online>")

#This is the main input field where the user can call the function
@client.command()
async def weather(ctx, *, city):

  #Setting up the program for API Key and Webscraping
  #Lines 34-42 were adapted by this GeeksForGeeks documentation example - https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/

  api_key = '05263c9a5cfd7b2a4f3859922948c914'
  base_url = "http://api.openweathermap.org/data/2.5/weather?"
  search_url = base_url + "appid=" + api_key + "&q=" + city

  #This is to get the status code - will be used later on to determine if it is valid
  x = requests.get(search_url)
  sc = x.status_code

  #This is passing the url into the weather function
  real_information = get_weather(city, search_url)

  #Checking if the status code is not found
  if sc == 404:
    #Sending an error message in the event of a program breakdown
    error = discord.Embed(
      title = "Error",
      description = "You have entered an invalid city name. Please retry.",
      color = 0xff0000
    )
    await ctx.send(embed=error)
    return

  #Checking if there is an internal server error
  if sc == 500:
    #Sending an error message in the event of a program breakdown
    error = discord.Embed(
      title = "Error",
      description = "There is a server side issue. Please try again later.",
      color = 0xff7b00
    )
    await ctx.send(embed=error)
    return

  #If no errors are present - the rest of the program functions correctly
  else:
    #Creates the menu selection
    menu = discord.Embed(
    title = "Menu Selection",
    description = "You have a limited amount of time. Please react with the proper emoji to request the weather information you would like to know.",
    color = 0x2bff00
    )

    menu_selection = []
    temp_selection = ":red_circle:  -  Temperature - Displayed in fahrenheit"
    coord_selection = ":blue_circle:  -  Coordinates - Longtiude and Latitude"
    desc_selection = ":green_circle:  -  Description - Shows current conditions"
    humidity_selection = ":yellow_circle:  -  Humidity - Shows the current humidity"
    wind_selection = ":orange_circle:  -  Wind - This will show the current wind speed"

    menu_selection.append(temp_selection)
    menu_selection.append(coord_selection)
    menu_selection.append(desc_selection)
    menu_selection.append(humidity_selection)
    menu_selection.append(wind_selection)

    menu.add_field(name = "Selections", value = "You will 15 seconds to choose the information", inline = False)
    menu.add_field(name = "Reaction Selection", value = "\n".join(value for value in menu_selection), inline=True)
    msg = await ctx.send(embed=menu)

    msg_id = msg.id

    #Gets the message ID and waits for 15 seconds so user can react
    await asyncio.sleep(15)
    updated_msg = await ctx.fetch_message(msg.id)
    
    #This is a list of the information the user wants
    wanted_information, count = get_reactions(updated_msg.reactions)

    #Setting up the display of all the information for the user
    colors = [0xe3fc03, 0x03fc2c, 0x03fcf8, 0xfc6203, 0xad03fc, 0xfc03df]

    if count == 0 :
      weather_display = discord.Embed(
        title = 'Weather Report for ' + str(city),
        description = 'You have not entered any valid emojis. Please retry.',
        color = 0xf51000
      )

    else:
      #Creating the display of actual information
      display = ''
      for info in wanted_information:
        display += info + '  :  ' + str(real_information.get(info)) + '\n'

      #Creating an embed to show in discord with the bot response
      weather_display = discord.Embed(
        title = 'Weather Report for ' + str(city),
        description = 'This is your weather information for ' + str(city) + '\n' + '\n' + display,
        color = random.choice(colors)
      )

      #Putting an icon of the current weather description
      base_icon = 'http://openweathermap.org/img/wn/'
      weather_display.set_footer(text='WEATHER REPORT')
      icon = real_information.get("icon")
      weather_display.set_thumbnail(url=base_icon + icon + '.png')

      #Sending the display to discord for the user to see the information
    await ctx.send(embed=weather_display)


#This is a function to get the reactions the user put to determine what information they requested
def get_reactions(reactions):

  #Using a list to store the information they want, iterating through all the 
  #reactions, and adding requested information
  count = 0
  information = []
  for reaction in reactions:

    #Green circle - Description
    if reaction.emoji == '\U0001f7e2':
      information.append('Description')
      count += 1

    #Red Circle - Temperature
    if reaction.emoji == '\U0001f534':
       information.append('Temperature')
       count += 1

    #Blue circle - coordinates
    if reaction.emoji == '\U0001f535':
       information.append('Coordinates')
       count += 1

    if reaction.emoji == '\U0001f7e1':
      information.append('Humidity')
      count += 1
      
    if reaction.emoji == '\U0001f7e0':
      information.append('Wind')
      count += 1

  return information, count

#This is the main function to take the url and get the information
def get_weather(city, url):
  #Gets the json information for that city using the url
  response = requests.get(url)
  json_raw_info = response.json()

  #Temporary variable in case I want to see the information printed out in development
  x = json.dumps(json_raw_info, indent=2)

  #Creating a dictionary that will contain all the information of the city
  weather_database = {
  "Temperature": str(round((json_raw_info['main']['temp_min'] - 273.15) * 9/5 + 32, 2)) + ' ℉',
  "Coordinates": (round(json_raw_info['coord']['lon'], 2), round(json_raw_info['coord']['lat'], 2)),
  "Description": json_raw_info['weather'][0]['description'],
  "Humidity": str(json_raw_info["main"]["humidity"]) + '%',
  "Wind": str(json_raw_info["wind"]["speed"]) + " mph",
  "icon": json_raw_info['weather'][0]['icon']
  }

  #Printing out the raw json information and returning the dictionary to the main function
  #print(x)
  return weather_database


#This is the client key I can use to run the program on discord
client.run('insert token here')




