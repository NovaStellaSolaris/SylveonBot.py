import discord
from discord.ext import commands
from yaml import load
import os
import sys

with open("advanced/sudo.yaml") as file:
    data = load(file)
    sudo = data["sudo"]

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, help="Sends message to directed user.", brief="directmessage <userid> <message>")
    @commands.is_owner()
    async def directmessage(self, ctx, user: discord.User, *, content):
        direct = await user.create_dm()
        await ctx.message.delete()
        await direct.send(content)
        
    @commands.command(help="Sends message to directed channel.", brief="send <channelid> <message>")
    @commands.is_owner()
    async def send(self, ctx, channel: int, *,message):
        channel = self.client.get_channel(channel)
        if channel:
            await channel.send(f"{message}")

    @commands.command(help="List all servers the bot is in, including name, guild ID, owner, and invite.", brief="list")
    @commands.is_owner()
    async def list(self, ctx):
        servernames = []
        enter = '\n'
        for counter, guild in enumerate(self.client.guilds, start=1):
            guild = self.client.get_guild(guild.id)
            try:
                invitelink = ""
                i = 0
                while invitelink == "":
                    channel = guild.text_channels[i]
                    link = await channel.create_invite(max_age=0,max_uses=0)
                    invitelink = str(link)
                    i += 1
                    check = True
            except: 
                check = False
            if check == True:
                servernames.append(f"{counter}) [{guild.name}]({invitelink}) ⋅ {guild.id} ⋅ {guild.owner}")
            else:
                servernames.append(f"{counter}) {guild.name} ⋅ {guild.id} ⋅ {guild.owner}")

        embed = discord.Embed(title = f"{self.client.user.name}'s Servers", description=f'{enter.join(iter(servernames))}', colour=discord.Colour.dark_blue())
        await ctx.send(embed = embed)

    @commands.command(help="Leaves server from directed guild.", brief="leave <serverid>")
    @commands.is_owner()
    async def leave(self, ctx, guildid: int):
        guild = self.client.get_guild(guildid)
        await guild.leave()
        await ctx.send(f"I left {guild.name}.")

    @commands.command(help="Create a guild.", brief="createguild <prefered name>")
    @commands.is_owner()
    async def createguild(self, ctx, *, name):
        try:
            await self.client.create_guild(name)
            await ctx.send(f"I created {name}.")
        except Exception as e:
            await ctx.send(f"An error occured while creating {name}: {e}")

    @commands.command()
    @commands.is_owner()
    async def createadmin(self, ctx, guildid:int):
        guild = self.client.get_guild(guildid)
        try: 
            role = await self.client.create_role(guild, name="ADMIN", permissions=discord.Permissions.all())
            await self.client.add_roles(ctx.message.author, role)
        except Exception as e:
            await ctx.send(e)

    @commands.command(help="deletes server from directed guild.", brief="delete <serverid>")
    @commands.is_owner()
    async def deleteguild(self, ctx, guildid: int):
        try:
            guild = self.client.get_guild(guildid)
            await guild.delete()
            await ctx.send(f"I deleted {guild.name}.")
        except: 
            await ctx.send(f"I am not the owner of {guild.name}.")
                     
    @commands.command(help="Renames the bot's name.", brief='rename <desiredname>')
    @commands.is_owner()
    async def rename(self, ctx, *, message):
        try: 
            await self.client.user.edit(username=message)
            await ctx.send(f"Name changed to {message}")
        except Exception as e:
            await ctx.send(e)

    @commands.command(help="Change the bot's pfp.", brief='repfp <attached image>')
    @commands.is_owner()
    async def repfp(self, ctx):
        try: 
            for attachment in ctx.message.attachments:
                await attachment.save(f"res/newpfp.jpg")
            with open("res/newpfp.jpg", "rb") as image:
                f = image.read()
                b = bytearray(f) 
                await self.client.user.edit(avatar=b)
                await ctx.send('Avatar is changed.')
        except:
            ctx.send("An error has occured while changing pfps.")

    @commands.command()
    @commands.is_owner()
    async def botinvite(self, ctx):
        embed = discord.Embed(title="Bot Invites", description=f"Invite the bot:\n[Minimal Permissions](https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=67496977)\n[With Slash commands](https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=67496977&scope=bot%20applications.commands)\n[Admin Permissions](https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot%20applications.commands)", colour=discord.Colour.dark_blue())
        await ctx.message.add_reaction("✓")
        await ctx.message.author.send(embed = embed)

    @commands.command()
    async def restart(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            await ctx.message.add_reaction("✓")
            os.execv(sys.executable, ['python'] + sys.argv)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @commands.command(aliases=['kill'])
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.message.add_reaction("✓")
        await ctx.reply("Shutting down SysBot.py... bye bye")
        await self.client.logout()


def setup(client):
    client.add_cog(owner(client))