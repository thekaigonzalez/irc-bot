from datetime import datetime
import sys
import discord
import asyncio
from discord.ext import commands, tasks

from aioconsole.stream import ainput

from termcolor import cprint

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

curr_channel = 969335944643760260


@tasks.loop(seconds=2)
async def thr():
    global curr_channel
    t = await ainput()

    t2 = t.split(" ")

    if (t2[0] == '/switch'):
        id = int(t2[1])
        curr_channel = id
        sys.stdout.write("New channel: ")
        cprint("#" + client.get_channel(curr_channel).name,
               'green', attrs=['bold'])
        sys.stdout.flush()
    elif t2[0] == '/list':
        print('Available Channels:')
        for ch in client.get_channel(curr_channel).guild.text_channels:
            cprint("#" + ch.name + " - ` /switch " + str(ch.id) +
                   " '", attrs=['bold'], color='green')

    if not (t.startswith("/")):
        await client.get_channel(curr_channel).send(t)


@client.event
async def on_ready():

    print("Welcome to IRC-inspired discord bot controlling!")
    cprint("Warning: This may be against TOS but I have no clue. Open an issue if you think it is and i will review. (Me, Kai Gonzalez)", 'yellow')
    sys.stdout.write("Starting in channel: ")
    cprint("#" + client.get_channel(curr_channel).name,
           'green', attrs=['bold'])
    sys.stdout.flush()
    if not thr.is_running():
        thr.start()


@client.event
async def on_message(msg: discord.Message):
    if (msg.channel.id == curr_channel):

        cprint("[~ " + msg.author.display_name.lower() + " (" + str(datetime.now().month) + "/" + str(datetime.now().day) + "/" +
               str(datetime.now().year) + ")]: " + msg.content, attrs=['bold'])

f = open("token.txt")
client.run(f.read())
f.close()
