import discord
import asyncio
import sys
import os
from discord.ext import commands
from datetime import datetime
import modules.permit as perm #pylint: disable=import-error

class AFKcheck(commands.Cog):
    def __init__(self, client):
        self.client = client
        global afkID
        global panelID
        global botID
        global keyReactExists
        keyReactExists = False
        afkID = 0
        panelID = 0
        with open('config/bot/botID.txt', 'r') as id:
            botID = int(id.read())


    @commands.Cog.listener()
    async def on_ready(self):
        print('AFKcheck.py ready')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global keyReactExists
        global confirm
        #channel = self.client.get_channel(payload.channel_id)

        uID = payload.user_id
        user = await self.client.fetch_user(int(uID))

        if payload.message_id == afkID:
            if str(payload.emoji) == '❌' and uID != botID:
                await afkmessage.edit(embed = endedAFK)
                await afkmessage.clear_reactions()
                await controls.edit(embed = endedPanel)
                await controls.clear_reactions()
            
            if payload.emoji == key and uID != botID:
                try:
                    confirm = await user.send('You have reacted with {}! Please react to confirm:'.format(key))
                    await confirm.add_reaction(key)
                    keyReactExists = True
                except:
                    await controls.channel.send('{} tried to react to key, but couldn\'t receive the DM.'.format(user.display_name))

        if payload.message_id == panelID:
            if str(payload.emoji) == '❌' and uID != botID:
                await afkmessage.edit(embed = endedAFK)
                await afkmessage.clear_reactions()
                await controls.edit(embed = endedPanel)
                await controls.clear_reactions()

            if str(payload.emoji) == '❗' and uID != botID:
                await afkmessage.edit(embed = abortedAFK)
                await afkmessage.clear_reactions()
                await controls.edit(embed = abortedPanel)
                await controls.clear_reactions()
        if keyReactExists == True:
            if payload.message_id == confirm.id and uID != botID:
                try:
                    await user.send('Thank you for confirming! The location for this run is {}'.format(location))
                    keyReactExists = False
                except:
                    await controls.channel.send('{} tried to react to key, but couldn\'t receive the DM.'.format(user.display_name))

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
        ch = open("data/afkChannelID.txt", "r")
        now = datetime.utcnow().strftime("%d %b %H:%M:%S")
        AFKchannel=self.client.get_channel(int(ch.read()))
        ch.close()
        dungeon=str.capitalize(dgn)

        global key
        global afkmessage
        global controls
        global location

        location = loc

        afk = discord.Embed(
            color = discord.Colour.green(),
        )
        afk.set_footer(text=datetime.utcnow().strftime("%d %b %H:%M:%S"))
        afk.set_author(name='{} has started a {} AFK check!'.format(author,dungeon),icon_url=pfp)
        if dungeon == 'Void': #set of if/elif statements to decide how to format the AFK check based on the dungeon being run
            thumburl = 'https://cdn.discordapp.com/attachments/817918991221260340/817919006883053589/7JGSvMq.png'
            afk.set_thumbnail(url = thumburl)
            reactions = open('config/afk-checks/void-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'losthalls')
            key = discord.utils.get(self.client.emojis, name = 'lhkey')

        elif dungeon == 'Nest':
            thumburl = 'https://cdn.discordapp.com/attachments/817918991221260340/818038375670874152/hUWc3IV.png'
            afk.set_thumbnail(url = thumburl)
            reactions=open('config/afk-checks/nest-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'nest')
            key = discord.utils.get(self.client.emojis, name = 'nestkey')

        elif dungeon == 'Shatters':
            thumburl = 'https://cdn.discordapp.com/attachments/817918991221260340/818038399784058930/shtrs_The_Forgotten_King.png'
            afk.set_thumbnail(url = thumburl)
            reactions=open('config/afk-checks/shatters-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'shatters')
            key = discord.utils.get(self.client.emojis, name = 'shkey') 
            switches='{}{}{}'.format(discord.utils.get(self.client.emojis, name = '1switch'), discord.utils.get(self.client.emojis, name = '2switch'), discord.utils.get(self.client.emojis, name = 'sswitch'))
            afk.add_field(name='Rushers:', value='If you plan on rushing a switch, please react to the corresponding {} emoji!'.format(switches), inline=True)           

        elif dungeon == 'Cult':
            thumburl = 'https://cdn.discordapp.com/attachments/817918991221260340/818038412656508958/nPkovWR.png'
            afk.set_thumbnail(url = thumburl)
            reactions=open('config/afk-checks/cult-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'losthalls')
            key = discord.utils.get(self.client.emojis, name = 'lhkey')
            afk.add_field(name='Rushers:', value='If you plan on rushing, please react to the {} emoji!'.format(discord.utils.get(self.client.emojis, name = 'rusher')), inline=True)

        elif dungeon == 'Fungal':
            thumburl = 'https://cdn.discordapp.com/attachments/817918991221260340/818038385791860766/5DfG6i5.png'
            afk.set_thumbnail(url = thumburl)
            reactions=open('config/afk-checks/fungal-reacts.txt','r')
            portal = discord.utils.get(self.client.emojis, name = 'fungal')
            key = discord.utils.get(self.client.emojis, name = 'fckey')

        else:
            await ctx.send("Please choose an exaltation dungeon! Correct input: `!afk [void/cult/shatters/nest/fungal]`")
        
        afk.description = 'React to the {} and your class/gear choices if you\'re joining the run! If you have a {} and are willing to pop, react to it.'.format(portal,key)

        afkmessage = await AFKchannel.send('@here', embed=afk) #posts the embed, and holds onto the message
        for line in reactions: #loop that reads through a set of emoji names and applies them to the message as reactions
            strip = line.strip()
            react = discord.utils.get(self.client.emojis, name = strip)
            await afkmessage.add_reaction(react)
        reactions.close()
        await afkmessage.add_reaction('❌')

        #following this, the bot creates a control panel in the channel where the command was written

        panel = discord.Embed(
            color = discord.Colour.green(),
            title = '{}\'s {}'.format(author,dungeon)
        )
        panel.set_footer(text=now)
        panel.add_field(name = 'To end AFK:', value = 'React to ❌', inline = True)
        panel.add_field(name = 'To abort AFK:', value = 'React to ❗', inline = False)
        panel.add_field(name = 'Location:', value = loc, inline = False)
        panel.add_field(name = 'Keys:', value = '{}None!'.format(key))
        controls = await ctx.send(embed=panel)
        await controls.add_reaction('❌')
        await controls.add_reaction('❗')

        global afkID
        global panelID
        panelID = controls.id
        afkID = afkmessage.id

        global endedAFK
        global endedPanel
        global abortedAFK
        global abortedPanel

        endedAFK = discord.Embed(
            color = discord.Colour.red(),
            title = 'This {} AFK check ended at {}'.format(dungeon, now)
        )
        endedAFK.set_thumbnail(url = thumburl)

        endedPanel = discord.Embed(
            color = discord.Colour.red(),
            title = 'This is a placeholder embed!'
        )
        abortedAFK = discord.Embed(
            color = discord.Colour.red(),
            title = 'This is a placeholder embed!'
        )
        abortedPanel = discord.Embed(
            color = discord.Colour.red(),
            title = 'This is a placeholder embed!'
        )

def setup(client):
    client.add_cog(AFKcheck(client))