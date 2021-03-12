import discord
import asyncio
import sys
import os
from discord.ext import commands

def checkperms(ctx, doc): 
    with open(doc, 'r') as rolelist:
        for line in rolelist:
            roleName = line.strip()
            role = discord.utils.get(ctx.guild.roles, name = roleName)
            if role in ctx.author.roles: #if the person typing the command has roles that should let them use the command:
                return True 

    with open('secrets/devlist.txt', 'r') as devlist:
        for line in devlist:
            if int(line.strip()) == ctx.message.author.id: #or if they're me
                return True #then move on as planned

    return False #otherwise, fuck off
    