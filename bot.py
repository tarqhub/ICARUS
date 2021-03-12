import discord
import asyncio
import sys
import os
from discord.ext import commands
from datetime import datetime
import modules.permit as perm #pylint: disable=import-error


prefixFile = open('config/bot/prefix.txt', 'r')
CustomPrefix = prefixFile.read()
client = commands.Bot(command_prefix = CustomPrefix)
prefixFile.close()

@client.event
async def on_ready():
    print("Bot ready!")

for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def setprefix(ctx, prefix):
    if not perm.checkperms(ctx, 'config/permissions/setprefix.txt'): #read modules/permit.py
            await ctx.send('You do not have permission to use this command!')
            return None #fail the command if the person using it isn't allowed to

    with open('config/prefix.txt', 'w') as f:
        f.truncate(0) #clear the current prefix
        f.write(prefix) #and save the new prefix
    await ctx.send('My prefix is now: `{}`. Please restart me for changes to take effect!'.format(prefix))

@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("{} enabled!".format(extension))

@client.command()
async def unload(ctx,extension):
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