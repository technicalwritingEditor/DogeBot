import discord
from discord.ext import commands
import random, asyncio, aiohttp, datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class mod():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        y = await self.bot.db.antiinvites.find_one({"id": str(message.guild.id)})
        if not y:
            return
        on_or_off = y['on_or_off']
        if on_or_off == "on":
            if  "https://discord.gg/".lower() in message.content.lower():
                x = await message.channel.send(f"{message.author.mention}| **No invites!** :rage: ")
                await message.delete()
                await asyncio.sleep(3)
                await x.delete()
        if on_or_off == "off":
            pass
        
    async def on_member_join(self, user):
        x = await self.bot.db.welcome.find_one({"id": str(user.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(x['message'].replace('$name$', user.name).replace('$mention$', user.mention).replace('$server$', user.guild.name))
        on_or_off = x['on_or_off']
        if on_or_off == "on":
            img = Image.open("maxresdefault.jpg")
            img.thumbnail( ( 500, 400, 400, 400 ) )
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("American Captain.otf", 75)
            draw.text((100, 0), "Welcome", (255, 255, 255), font=font)
            draw.text((0, 125), "{}".format(user.name), (255, 255, 255), font=font)
            img.save(f'{user.id}.jpg')
            await send_channel.send(file=discord.File(f'{user.id}.jpg'))
        y = await self.bot.db.autorole.find_one({"id": str(user.guild.id)})
        if y is None:
            return
        role = y['role']
        r = discord.utils.get(user.guild.roles, name=role)
        await user.add_roles(r)


    async def on_member_remove(self, user):
        em = discord.Embed(description=f"Goodbye **{user.name}**", color=0x1aff00, timestamp = datetime.datetime.utcnow())
        em.set_author(name=user, icon_url=user.avatar_url)
        x = await self.bot.db.leave.find_one({"id": str(user.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(x['message'].replace('$name$', user.name).replace('$mention$', user.mention).replace('$server$', user.guild.name))   
   
    #async def on_message_delete(self, message):
        #em = discord.Embed(color=0x1aff00, timestamp = datetime.datetime.utcnow())
        #em.add_field(name="Message deleted", value=message.content)
        #em.set_author(name=message.author, icon_url=message.author.avatar_url)
        #x = await self.bot.db.modlog.find_one({"id": str(message.guild.id)})
        #if not x:
            #return
        #channel = int(x['channel'])
        #send_channel = self.bot.get_channel(channel)
        #if not send_channel:
            #return
        #await send_channel.send(embed=em)           

    #async def on_message_edit(self, before, after):
            #em = discord.Embed(color=0x1aff00, timestamp = datetime.datetime.utcnow())
            #em.add_field(name="Before", value=before.content)
            #em.add_field(name="After", value=after.content)
            #em.set_author(name=before.author, icon_url=before.author.avatar_url)
           # x = await self.bot.db.modlog.find_one({"id": str(before.guild.id)})
            #if not x:
                #return
            #channel = int(x['channel'])
            #send_channel = self.bot.get_channel(channel)
            #if not send_channel:
                #return
            #await send_channel.send(embed=em)     

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx, sort=None):
        if sort == None:
            await ctx.send("**Choose `on` or `off`**")
        if sort == "on":
            await ctx.send("**Please mention the channel to set the welcome messages in.**")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("**The time is up**")
            if not x.content.startswith("<#") and not x.content.endswith(">"):
                return await ctx.send("**Please mention the channel**")
            channel = x.content.strip("<#").strip(">")
            try:
                channel = int(channel)
            except ValueError:
                return await ctx.send("**Please mention the channel right**")
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
            await ctx.send("**I have set the welcome channel!**")
            embed=discord.Embed(description="**Write a message!**\n\nVaribales:\n**$name$** Name of user\n**$mention$** Mentions user\n**$server$** Server name", color=0x00ff00)
            await ctx.send(embed=embed)
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                 return await ctx.send("Request timed out. Please try again.")
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel, "message": x.content}}, upsert=True)
            await ctx.send("Successfully turned on message")
        if sort == "off":
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": False, "message": None}}, upsert=True)
            await ctx.send("**I have turned off welcome messages**")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcomeimage(self, ctx, sort=None):
        if sort == None:
            await ctx.send("choose `on` or `off`")
        if sort == "on":
            await ctx.send("**You have turned on welcome images!**")
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"on_or_off": "on"} }, upsert=True )
        if sort == "off":
            await ctx.send("**You have turned off welcome images**")
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"on_or_off": "off"} }, upsert=True )
            
    @commands.command(aliases=['goodbye'])
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx, sort=None):
        if sort == None:
            await ctx.send("**Choose `on` or `off`**")
        if sort == "on":
            await ctx.send("**Please mention the channel to set the leave messages in.**")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("**The time is up**")
            if not x.content.startswith("<#") and not x.content.endswith(">"):
                return await ctx.send("**Please mention the channel**")
            channel = x.content.strip("<#").strip(">")
            try:
                channel = int(channel)
            except ValueError:
                return await ctx.send("**Please mention the channel right**")
            await self.bot.db.leave.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
            await ctx.send("**I have set the leave channel!**")
            embed=discord.Embed(description="**Write a message!**\n\nVaribales:\n**$name$** Name of user\n**$mention$** Mentions user\n**$server$** Server name", color=0x00ff00)
            await ctx.send(embed=embed)
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                 return await ctx.send("Request timed out. Please try again.")
            await self.bot.db.leave.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel, "message": x.content}}, upsert=True)
            await ctx.send("Successfully turned on leave messages for this guild.")            
        if sort == "off":
            await self.bot.db.leave.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": False, "message": None}}, upsert=True)
            await ctx.send("**I have turned off leave messages**")           

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def modlog(self, ctx, sort=None):
        if sort == None:
            await ctx.send("**`on` or `off`**")
        if sort == "on":
            await ctx.send("**Please mention the channel to set the log messages in.**")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("**The time is up**")
            if not x.content.startswith("<#") and not x.content.endswith(">"):
                return await ctx.send("**Please mention the channel**")
            channel = x.content.strip("<#").strip(">")
            try:
                channel = int(channel)
            except ValueError:
                return await ctx.send("**Please mention the channel right**")
            await self.bot.db.modlog.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
            await ctx.send("**I have set the mod-log channel!**")
        if sort == "off":
            await self.bot.db.modlog.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": False} }, upsert=True )
            await ctx.send("**I have turned off modlog messages**")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def antiinvites(self, ctx, sort=None):
        if sort == None:
            await ctx.send("choose `on` or `off`")
        if sort == "on":
            await ctx.send("**You have turned on anti invites!**")
            await self.bot.db.antiinvites.update_one({"id": str(ctx.guild.id)}, {"$set": {"on_or_off": "on"} }, upsert=True )
        if sort == "off":
            await ctx.send("**You have turned off anti invites!**")
            await self.bot.db.antiinvites.update_one({"id": str(ctx.guild.id)}, {"$set": {"on_or_off": "off"} }, upsert=True )


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user:discord.Member,*, reason):
        await user.kick()
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: kick", color=0xff7c3e)
        embed.add_field(name="User", value=f"{user} ({user.mention})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(f"Kicked **{user}**")
        channel = int(x['channel'])
        send_channel= self.bot.get_channel(channel)
        await send_channel.send(embed=embed)     
        await user.send(f"You have been kicked from {ctx.guild.name}!\nModerator: {ctx.author}\nReason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user:discord.Member,*, reason):
        await user.ban()
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: Ban", color=0xff0f0f)
        embed.add_field(name="User", value=f"{user} ({user.mention})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(f"Banned **{user}**")
        channel = int(x['channel'])
        send_channel= self.bot.get_channel(channel)
        await send_channel.send(embed=embed)
        await user.send(f"You have been banned from {ctx.guild.name}!\nModerator: {ctx.author}\nReason: {reason}")
        
    @commands.command()   
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user:discord.Member,*, reason):
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: Warn", color=0xff7c3e)
        embed.add_field(name="User", value=f"{user} ({user.mention})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(f"Warned **{user}**")
        channel = int(x['channel'])
        send_channel= self.bot.get_channel(channel)
        await send_channel.send(embed=embed)
        await user.send(f"You have been Warned in {ctx.guild.name}!\nModerator: {ctx.author}\nReason: {reason}")
        
    @commands.command()   
    @commands.has_permissions(manage_channels=True)
    async def mute(self, ctx, user:discord.Member,*, reason):
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: Mute", color=0xffff37)
        embed.add_field(name="User", value=f"{user} ({user.mention})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(f"Muted **{user}**")
        await ctx.channel.set_permissions(user, send_messages=False)
        channel = int(x['channel'])
        send_channel= self.bot.get_channel(channel)
        await send_channel.send(embed=embed)
        
    @commands.command()   
    @commands.has_permissions(manage_channels=True)
    async def unmute(self, ctx, user:discord.Member,*, reason):
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: Unmute", color=0x00f200)
        embed.add_field(name="User", value=f"{user} ({user.mention})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(f"Unmuted **{user}**")
        await ctx.channel.set_permissions(user, send_messages=True)
        channel = int(x['channel'])
        send_channel= self.bot.get_channel(channel)
        await send_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        try:
            float(number)
        except ValueError:
            return await ctx.send("The number is invalid.")
        await ctx.channel.purge(limit=number+1)
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        embed=discord.Embed(description=f"Purged {messages}\nModerator: {ctx.author.mention}")
        await send_channel.send(embed=embed)
        msg = await ctx.send(f"Purged **{number}** messages!")
        await asyncio.sleep(3)
        await msg.delete()
  
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def autorole(self, ctx, *, role):
        if role == 'off':
            await self.bot.db.autorole.update_one({"id": str(ctx.guild.id)}, {"$set": {"role": False}}, upsert=True)
            await ctx.send("Turned off autorole")
        else:
            r = discord.utils.get(ctx.guild.roles, name=str(role))
            if r is None:
                return await ctx.send("Role not found.")
            await self.bot.db.autorole.update_one({"id": str(ctx.guild.id)}, {"$set": {"role": str(r)}}, upsert=True)
            await ctx.send(f"Enabled autorole for **{str(r)}**.")

    @commands.command(aliases=['arole'])
    @commands.has_permissions(manage_roles = True)
    async def addrole(self, ctx, user:discord.Member,*, role):
        x = discord.utils.get(ctx.guild.roles, name=role)
        await user.add_roles(x)
        await ctx.send(f"Added **{role}** to **{user}**")           

    @commands.command(aliases=['rrole'])
    @commands.has_permissions(manage_roles = True)
    async def removerole(self, ctx, user:discord.Member,*, role):
        x = discord.utils.get(ctx.guild.roles, name=role)
        await user.remove_roles(x)
        await ctx.send(f"Removed **{role}** from **{user}**")         
       
def setup(bot):
    bot.add_cog(mod(bot))
