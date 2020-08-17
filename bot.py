import discord
from discord.ext import commands,tasks
import startmcserver
import asyncio
from mcstatus import MinecraftServer

bot = commands.Bot(command_prefix='&')  #command prefix
countdown = False
wlistEnabled = False

@bot.event
async def on_ready():
    print('Logged on')
    activity = discord.Activity(name='redstone tutorials', type=discord.ActivityType.watching)
    wlistEnabled = False
    await bot.change_presence(activity=activity)

wlist = []
s = startmcserver.MCServer()  #Instance of Server Class in startmcserver.py

import socket
def get_vlanIP():  #invoked by command &server ip
    vlan_ip = ""
    iplist = socket.gethostbyname_ex(socket.gethostname())[2]
    for ip in iplist:                       ### This was set up according to my own vlan config
        if ip.startswith('192.168.240'):    ### Change or remove this part for your own setup
            vlan_ip = ip + ":25565"         ### 25565 as default port
    return(vlan_ip)

async def check_empty(): #Check if server has player in it, invoked whenever the server is started by '&server start' command
    await asyncio.sleep(60) # give 60 seconds for the server to properly start up
    timer = 0
    countdown = True
    #print('timer started')
    while not bot.is_closed():
        if(countdown is True):
            server = MinecraftServer.lookup("127.0.0.1:25565") #getServer status by localhost ip,default port = 25565(change if needed)
            status = server.status()
            if(status.players.online == 0): #if server is empty
                if timer > 900: #server is empty for 15 minutes
                    #print('time reached')
                    channel = bot.get_channel(int('YOUR CHANNEL ID HERE')) #get channel ID of dedicate channel for bot messages
                    await channel.send('Server is empty for 15 minutes, shutting down. Restart the server by using "&server start".')
                    s.server_stop()
                    timer = 0
                    countdown = False
                timer += 1
                await asyncio.sleep(1)
            if(status.players.online != 0): #if server is not empty,reset timer
                #print("player joined,reseting timer")
                timer = 0
                await asyncio.sleep(60)
        else:
            timer = 0
            await asyncio.sleep(5)


@bot.group()
async def watchlist(ctx):
    if ctx.invoked_subcommand is None: #if a sub command was not given
        await ctx.send('Arguments needed...')

@watchlist.command() #Adds user to watchlist
async def add(ctx,arg):
    if(str(ctx.message.author.id) not in wlist):
            await ctx.send("You dont't have the permission for this command.")
            return
    user_id = arg.split('!')[1].split('>')[0]
    wlist.append(user_id)

@watchlist.command() #Removes a user from watchlist
async def remove(ctx,arg):
    if(str(ctx.message.author.id) not in wlist):
            await ctx.send("You dont't have the permission for this command.")
            return
    user_id = arg.split('!')[1].split('>')[0]
    wlist.remove(user_id)

@watchlist.command()
async def enable(ctx): #enables watchlist
    global wlistEnabled
    if(str(ctx.message.author.id) not in wlist):
            await ctx.send("You dont't have the permission for this command.")
            return
    if(wlistEnabled == True):
        await ctx.send('WatchList is already enabled')
    else:
        wlistEnabled = True

@watchlist.command()
async def dsibale(ctx): #disables watchlist
    global wlistEnabled
    if(str(ctx.message.author.id) not in wlist):
            await ctx.send("You dont't have the permission for this command.")
            return
    if(wlistEnabled == False):
        await ctx.send('WatchList is already disabled')
    else:
        wlistEnabled = False

@bot.group()
async def server(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Arguments needed...(start or stop)')

@server.command()
async def start(ctx):
    global wlistEnabled
    if(wlistEnabled==True):
        if(str(ctx.message.author.id) not in wlist):
            await ctx.send("You dont't have the permission for this command.")
            return
    s.server_start()
    bot.loop.create_task(check_empty())
    countdown = True
    await ctx.send('Starting Server,please wait....')

@server.command()
async def stop(ctx):
    global wlistEnabled
    if(wlistEnabled==True):
        if(str(ctx.message.author.id) not in wlist):
            await ctx.send("You dont't have the permission for this command.")
            return
    countdown = False
    s.server_stop()
    await ctx.send('Stopping Server,good bye....')

@server.command()   #Retrive server ip
async def ip(ctx):
    ip = get_vlanIP()                               ### This was set up according to my own vlan config
    if(ip != ""):                                   ### Might cause errors if not using a vlan setup
        await ctx.send('Server IP:' + ip)           ###
    else:                                           ###     
        await ctx.send('Network not on vlan.')      ### Change or remove this part if u don't need it

@bot.event
async def on_message(message):
    
    if(str(message.author.id) in wlist):            ### Adds a little blue tick emoji for watchlisted user's msg
        emoji = '<:bluetick:544524999931854858>'
        await message.add_reaction(emoji)
    await bot.process_commands(message)


token = 'YOUR TOKEN HERE'
bot.run(token)

