import discord
import sys
import os
from discord.ext import commands
from datetime import datetime
import modules.permit as perm #pylint: disable=import-error

class ChannelSetup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ChannelSetup.py ready')

    @commands.command()
    async def cmdchannel(self, ctx, cmdch): #finds a channel of the specified name, then posts all embeds from the !afk command to it.
        for channel in self.client.get_all_channels():
            if str.lower(channel.name) == str.lower(cmdch):
                command = self.client.get_channel(channel.id)
                await command.send('{} has been set as the run organization bot commands channel!'.format(command))
                ch = open("data/cmdChannelID.txt","w")
                ch.truncate(0)
                ch.write(str(channel.id))
                ch.close()
                return None
        return None

    @commands.command()
    async def setAfkChannel(self, ctx, afkchannel): #finds a channel of the specified name, then posts all embeds from the !afk command to it.
        for channel in self.client.get_all_channels():
            if str.lower(channel.name) == str.lower(afkchannel):
                AFKch = self.client.get_channel(channel.id)
                await AFKch.send('{} has been set as the AFK check channel!'.format(afkchannel))
                ch = open("data/afkChannelID.txt","w")
                ch.truncate(0)
                ch.write(str(channel.id))
                ch.close()
                return None
        return None

def setup(client):
    client.add_cog(ChannelSetup(client))