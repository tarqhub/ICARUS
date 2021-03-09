import discord
import sys
import os
from discord.ext import commands
from datetime import datetime

client = commands.Bot(command_prefix = "!")

for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print("Bot ready!")

@client.command()
async def start(ctx,extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("{} enabled!".format(extension))

@client.command()
async def kill(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("{} disabled!".format(extension))

@client.command()
async def reload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("{} reloaded!".format(extension))

token=open("secrets/token.txt", "r").readline()

client.run(token.strip())
token.close()