import discord
import sys
import os
from discord.ext import commands
from datetime import datetime
import modules.permit as perm #pylint: disable=import-error

class AFKcheck(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('AFKcheck.py ready')

    @commands.command()
    async def afk(self, ctx, dgn, *, loc):
        
        if not perm.checkperms(ctx, 'config/permissions/afk.txt'): #read modules/permit.py
            await ctx.send('You do not have permission to use this command!')
            return None #fail the command if the person using it isn't allowed to

        cmdCh = open('data/cmdChannelID.txt', 'r')
        commandsChannelID = cmdCh.read()
        commandsChannel=self.client.get_channel(int(commandsChannelID))
        if ctx.channel.id != int(commandsChannelID):
            await ctx.send('This is the wrong channel! Please use AFK check commands in {}.'.format(commandsChannel.mention))
            return None

        author = ctx.message.author.display_name
        pfp=ctx.message.author.avatar_url
        #reactions='no reactions folder yet!'
        #key = 'no key yet!'
        ch=open("data/afkChannelID.txt", "r")
        AFKchannel=self.client.get_channel(int(ch.read()))
        ch.close()
        dungeon=str.capitalize(dgn)
        afk = discord.Embed(
            color = discord.Colour.green(),
        )
        afk.set_footer(text=datetime.utcnow().strftime("%d %b %H:%M:%S"))
        afk.set_author(name='{} has started a {} AFK check!'.format(author,dungeon),icon_url=pfp)
        if dungeon == 'Void': #set of if/elif statements to decide how to format the AFK check based on the dungeon being run
            afk.set_thumbnail(url='https://cdn.discordapp.com/attachments/817918991221260340/817919006883053589/7JGSvMq.png')
            reactions = open('config/afk-checks/void-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'losthalls')
            key = '{} or {}'.format(discord.utils.get(self.client.emojis, name = 'lhkey'), discord.utils.get(self.client.emojis, name = 'vial'))
        
        elif dungeon == 'Nest':
            afk.set_thumbnail(url='https://cdn.discordapp.com/attachments/817918991221260340/818038375670874152/hUWc3IV.png')
            reactions=open('config/afk-checks/nest-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'nest')
            key = discord.utils.get(self.client.emojis, name = 'nestkey')

        elif dungeon == 'Shatters':
            afk.set_thumbnail(url='https://cdn.discordapp.com/attachments/817918991221260340/818038399784058930/shtrs_The_Forgotten_King.png')
            reactions=open('config/afk-checks/shatters-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'shatters')
            key = discord.utils.get(self.client.emojis, name = 'shkey') 
            switches='{}{}{}'.format(discord.utils.get(self.client.emojis, name = '1switch'), discord.utils.get(self.client.emojis, name = '2switch'), discord.utils.get(self.client.emojis, name = 'sswitch'))
            afk.add_field(name='Rushers:', value='If you plan on rushing a switch, please react to the corresponding {} emoji!'.format(switches), inline=True)           

        elif dungeon == 'Cult':
            afk.set_thumbnail(url='https://cdn.discordapp.com/attachments/817918991221260340/818038412656508958/nPkovWR.png')
            reactions=open('config/afk-checks/cult-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'losthalls')
            key = discord.utils.get(self.client.emojis, name = 'lhkey')
            afk.add_field(name='Rushers:', value='If you plan on rushing, please react to the {} emoji!'.format(discord.utils.get(self.client.emojis, name = 'rusher')), inline=True)

        elif dungeon == 'Fungal':
            afk.set_thumbnail(url='https://cdn.discordapp.com/attachments/817918991221260340/818038385791860766/5DfG6i5.png')
            reactions=open('config/afk-checks/fungal-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'fungal')
            key = discord.utils.get(self.client.emojis, name = 'fckey')

        else:
            await ctx.send("Please choose an exaltation dungeon! Correct input: `!afk [void/cult/shatters/nest/fungal]`")
        
        afk.description='React to the {} and your class/gear choices if you\'re joining the run! If you have a {} and are willing to pop, react to it.'.format(portal,key)

        afkcheck = await AFKchannel.send('@here', embed=afk) #posts the embed, and holds onto the message
        for line in reactions: #loop that reads through a set of emoji names and applies them to the message as reactions
            strip = line.strip()
            react = discord.utils.get(self.client.emojis, name = strip)
            await afkcheck.add_reaction(react)
        reactions.close()
        await afkcheck.add_reaction('❌')

        #following this, the bot creates a control panel in the channel where the command was written

        panel = discord.Embed(
            color = discord.Colour.green(),
            title = '{}\'s {}'.format(author,dungeon)
        )
        panel.set_footer(text=datetime.utcnow().strftime("%d %b %H:%M:%S"))
        panel.add_field(name = 'To end AFK:', value = 'React to ❌', inline = True)
        panel.add_field(name = 'To abort AFK:', value = 'React to ❗', inline = False)
        panel.add_field(name = 'Location:', value = loc, inline = False)
        panel.add_field(name = 'Keys:', value = '{}None!'.format(key))
        controls = await ctx.send(embed=panel)
        await controls.add_reaction('❌')
        await controls.add_reaction('❗')



def setup(client):
    client.add_cog(AFKcheck(client))