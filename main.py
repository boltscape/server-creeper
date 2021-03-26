from discord.ext.commands import Bot
from discord import Game

from mcstatus import MinecraftServer

from googleapiclient import discovery
from google.oauth2 import service_account

from keepalive import keep_alive

from cryptography.fernet import Fernet
import os
import ast

bot_token = os.getenv("TOKEN") #Discord bot token here
serveraddress = os.getenv("ADDRESS") #Get server address
#Setting the command prefix for the bot and creating a bot object
BOT_PREFIX = ('!')
client = Bot(command_prefix=BOT_PREFIX)

#Generating credentials object from the encrypted JSON file
hkey = (hex(int(os.environ["KEY"]))).lstrip('0x')
bkey = bytes.fromhex(hkey)
fernet = Fernet(bkey)
with open('encreds.json', 'rb') as enfile:
  encreds = enfile.read()
creds = fernet.decrypt(encreds)
dcreds = ast.literal_eval(creds.decode("utf-8"))
credentials = service_account.Credentials.from_service_account_info(dcreds)

#Building an object for the Compute instance
service = discovery.build('compute', 'v1', credentials=credentials)
project = 'minecraft-298108' #Your Google Cloud project ID
zone = 'asia-southeast1-b'  #The zone that your VM is in
instance = 'mc-server' #Your VM's name

#Function definitions start here

#The 6 core functions: start, stop, restart, status, address, and plist. Pretty self-explainatory.
@client.command(name="start", description="Starts the Minecraft server", brief="Starts server", pass_context=True)
async def startserver(ctx):
    request = service.instances().get(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response['status'] == 'PROVISIONING' or response['status'] == 'STAGING':
        await ctx.send("Ssserver is already ssstarting, "+ ctx.author.mention + ", wait up!")
        return
    elif response['status'] == 'RUNNING':
        await ctx.send("Ssserver isss already on, "+ ctx.author.mention + "! Get in there!")
        return
    request = service.instances().start(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response['status'] == 'RUNNING':
        await ctx.send("Ssserver ssstart confirmed, "+ ctx.author.mention + ", please wait!")

@client.command(name="stop", description="Stops the Minecraft server", brief="Stops server", pass_context=True)
async def stopserver(ctx):
    request = service.instances().get(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response['status'] == 'STOPPING':
        await ctx.send("Hmmmm. The ssserver is already ssstopping, "+ ctx.author.mention)
        return
    elif response['status'] == 'TERMINATED':
        await ctx.send("Hmmmm. The ssserver is already off, "+ ctx.author.mention)
        return
    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response['status'] == 'RUNNING':
        await ctx.send("Ssserver ssstopping, "+ ctx.author.mention + ", hope you had fun!")

@client.command(name="restart", description="Restart the Minecraft server", brief="Restart server", pass_context=True)
async def restartserver(ctx):
    request = service.instances().get(project=project, zone=zone, instance=instance)
    response = request.execute()
    if response['status'] == 'STOPPING':
        await ctx.send("Hmmmm. The ssserver is ssstopping, "+ ctx.author.mention + " I cannot restart it yet.")
        return
    elif response['status'] == 'TERMINATED':
        await ctx.send("Hmmmm. The ssserver is off, "+ ctx.author.mention)
        return
    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()
    request = service.instances().start(project=project, zone=zone, instance=instance)
    response = request.execute()
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

@client.command(name="plist", description="Get list of players online", brief="Player list", pass_context=True)
async def plist(ctx):
  try:
    server = MinecraftServer.lookup(serveraddress)
    status = server.status()
    if status.players.sample:
      player_list = [p.name for p in status.players.sample]
      await ctx.send("Online playersss: \n")
      for i in range(1, len(player_list)+1):
        await ctx.send(f"{i}. {player_list[i-1]}")
    else:
      await ctx.send("No playersss online, " + ctx.author.mention)
  except:
    await ctx.send("The ssserver is offline, " + ctx.author.mention)

#Some whimsical commands I wrote for my friends
@client.command(description="Show the server address", brief="Server address", pass_context=True)
async def address(ctx):
  await ctx.send("Hey "+ ctx.author.mention + ", use " + serveraddress + " to connect to the server!")

@client.command(name="hi", description="Say hi!", brief="Hi!", pass_context=True)
async def hi(ctx):
  await ctx.send("Hi, " + ctx.author.mention + " :smile:")

@client.command(name="thanks", description="Your way to thank the creeper xD", brief="Thanks", pass_context=True)
async def thanks(ctx):
    await ctx.send("You're welcome, " + ctx.author.mention + " :smile:")
    
#Set the bot's activity in Discord to playing Minecraft
@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="Minecraft"))

#Run the bot and the keep-alive service
keep_alive()
client.run(bot_token)
