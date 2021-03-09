import discord
import sys
import os
from discord.ext import commands
from datetime import datetime

class Testcog(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Testcog.py ready')

    @commands.command()
    async def fullmoon(self, ctx):
        await ctx.send('https://tenor.com/view/moon-bear-dancing-bear-in-the-big-blue-house-full-moon-gif-10667192')


def setup(client):
    client.add_cog(Testcog(client))