import discord
import sys
import os
from discord.ext import commands
from datetime import datetime
import modules.permit as perm #pylint: disable=import-error

class PermissionSetup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('PermissionSetup.py ready')

    @commands.command()
    async def addperms(self, ctx, cmd, *, role):
        cmdFile = open('config/permissions/{}.txt'.format(cmd), 'a')
        cmdFile.write(role)
        cmdFile.close()
    
    @commands.command()
    async def delperms(self, ctx, cmd, *, role):
        cmdFile = open('config/permissions/{}.txt'.format(cmd), 'w')
        for line in cmdFile:
            if line.strip() != role:
                cmdFile.write(line)
        cmdFile.close()


def setup(client):
    client.add_cog(PermissionSetup(client))