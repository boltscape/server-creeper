from discord.ext.commands import Bot
from googleapiclient import discovery
from google.oauth2 import service_account

from discord import Game
import os
from time import sleep

bot_token = '' #Enter your Discord bot token here
serveraddress = '' #Enter your server (Google Compute instance) IP address here

#Setting the command prefix for the bot and creating a bot object
BOT_PREFIX = ('!')
client = Bot(command_prefix=BOT_PREFIX)

#Generating credentials object from JSON file
credentials = service_account.Credentials.from_service_account_file('creds.json')

#Building an object for the Compute instance
service = discovery.build('compute', 'v1', credentials=credentials)
project = '' #Your Google Cloud project ID
zone = ''  #The zone that your VM is in
instance = '' #Your VM's name

#Function definitions start here

#The 5 core functions: start, stop, restart, status, and address. Pretty self-explainatory.
@client.command(name="start", description="Starts the Minecraft server", brief="Starts server", pass_context=True)
async def startserver(ctx):
    request = service.instances().start(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response['status'] == 'RUNNING':
        await ctx.send("Ssserver ssstart confirmed, "+ ctx.author.mention + ", please wait!")

@client.command(name="stop", description="Stops the Minecraft server", brief="Stops server", pass_context=True)
async def stopserver(ctx):
    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response['status'] == 'RUNNING':
        await ctx.send("Ssserver ssstopping, "+ ctx.author.mention + ", hope you had fun!")

@client.command(name="restart", description="Restart the Minecraft server", brief="Restart server", pass_context=True)
async def restartserver(ctx):
    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()
    sleep(30)
    request = service.instances().start(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response.status == 'RUNNING':
        await ctx.send("Ssserver ressstarting, "+ ctx.author.mention + ", hold on!")
   
@client.command(name="status", description="Check if server is running", brief="Check if server is running", pass_context=True)
async def serverstatus(ctx):
    request = service.instances().get(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response['status'] == 'PROVISIONING' or response['status'] == 'STAGING':
        await ctx.send("Ssserver is ssstarting right now, "+ ctx.author.mention + ", wait up!")
    elif response['status'] == 'RUNNING':
        await ctx.send("Ssserver isss on, "+ ctx.author.mention + "! Get in there!")
    elif response['status'] == 'STOPPING':
        await ctx.send("Hmmmm. The ssserver is ssstopping right now, "+ ctx.author.mention)
    elif response['status'] == 'TERMINATED':
        await ctx.send("Ssserver is off, " + ctx.author.mention)

#Some whimsical commands I wrote for my friends
@client.command(description="Show the server address", brief="Show server address", pass_context=True)
async def address(ctx):
    await ctx.send("Hey "+ ctx.author.mention + ", use " + serveraddress + " to connect to the server!")

@client.command(name="hi", description="Say hi!", brief="Hi!", pass_context=True)
async def thanks(ctx):
    await ctx.send("Hi, " + ctx.author.mention + " :smile:")

@client.command(name="thanks", description="Your way to thank the creeper xD", brief="Give thanks", pass_context=True)
async def thanks(ctx):
    await ctx.send("You're welcome, " + ctx.author.mention + " :smile:")
    
#Set the bot's activity in Discord to playing Minecraft
@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="Minecraft"))

#Run the bot
client.run(bot_token)
