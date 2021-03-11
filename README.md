# ICARUS
Realm of the Mad God discord bot being developed for a private server.


**bot.py**

!start (cog) - enables a cog

!kill (cog) - disables a cog

!reload (cog) - disables and re-enables a cog


**afk-checks.py**:

Currently contains names of custom reactions for the !afk command

!afk (void/nest/shatters/cult/fungal) - start an afk check for one of the 5 main exaltation dungeons



**ChannelSetup.py**:

!cmdchannel (channel name) - set what channel the bot can start an !afk from

!setAfkChannel (channel name) - set what channel the embed message from !afk will be posted to 


**PermissionSetup.py**:

!addperms (command, role) - allow (role) to use (command)

!delperms (command, role) - remove (role)'s permission to use (command)
