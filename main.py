from discord.ext.commands import Bot
from googleapiclient import discovery
from google.oauth2 import service_account

from discord import Game
import requests
import os
from time import sleep


BOT_PREFIX = ('!')
client = Bot(command_prefix=BOT_PREFIX)

credentials = service_account.Credentials.from_service_account_file('creds.json')

service = discovery.build('compute', 'v1')
project = 'feisty-ceiling-285406' 
zone = 'asia-southeast1-b'  
instance = 'mc-server'

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

@client.command(name="thanks", description="Your way to thank the creeper xD", brief="Give thanks", pass_context=True)
async def thanks(ctx):
    await ctx.send("You're welcome, " + ctx.author.mention + " :smile:")
    
@client.command(description="Show the server address", brief="Show server address", pass_context=True)
async def address(ctx):
    await ctx.send("Hey "+ ctx.author.mention + ", use " + os.environ['SERVER_ADDRESS'] + " to connect to the server!")

@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="Minecraft"))

                                 
client.run(TOKEN)
