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
            if  "https://discord.gg/".lower() in message.content.lower() or "discord.gg/".lower() in message.content.lower():
                x = await message.channel.send(f"{message.author.mention}| **No invites!** :rage: ")
                await message.delete()
                await asyncio.sleep(3)
                await x.delete()
                x = await self.bot.db.logging.find_one({"id": str(message.guild.id)})
                mod_channel = int(x['channel'])
                xD = self.bot.get_channel(mod_channel)
                embed = discord.Embed(description=f"📧 Invite deleted at {message.channel.mention}. Sent by {message.author.mention}!", color=0x9b9dff)
                await xD.send(embed=embed)
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
            img = Image.open("lol.jpg")
            img.thumbnail( ( 600, 600, 600, 600 ) )
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("American Captain.otf", 60)
            draw.text((50, 0), "Welcome", (255, 255, 255), font=font)
            draw.text((0, 100), "{}".format(user.name), (255, 255, 255), font=font)
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

    async def on_message_delete(self, message):
        x = await self.bot.db.logging.find_one({"id": str(message.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        embed=discord.Embed(title="Message removed", color=0xf90000, timestamp = datetime.datetime.utcnow())
        embed.add_field(name="User", value=message.author)
        embed.add_field(name="Channel", value=message.channel.mention)
        embed.add_field(name="Message", value=message.content, inline=False)
        await send_channel.send(embed=embed)

    async def on_message_edit(self, before, after):
        embed=discord.Embed(title="Message edited", color=0xff8040, timestamp = datetime.datetime.utcnow())
        embed.add_field(name="User", value=before.author)
        embed.add_field(name="Channel", value=before.channel.mention)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content)
        x = await self.bot.db.logging.find_one({"id": str(before.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(embed=embed)   
    
    async def on_member_update(self,before, after):
        x = await self.bot.db.logging.find_one({"id": str(before.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        embed=discord.Embed(title="Changing nickname", color=0xd000e1, timestamp = datetime.datetime.utcnow())
        embed.add_field(name="User", value=before.author, inline=False)
        embed.add_field(name="before", value=before.nickname)
        embed.add_field(name="after", value=after.nickname, inline=False)
        await send_channel.send(embed=embed)     
    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx, sort=None):
        """Turn on or off welcome messages"""        
        if sort == None:
            x = await self.bot.db.welcome.find_one({"id": str(ctx.guild.id)})
            channel = int(x['channel'])
            message = x['message']
            embed=discord.Embed(description="Your welcoming information",color=0x00f200)
            embed.add_field(name="Channel", value=channel, inline=False)
            embed.add_field(name="Message", value=message)
            await ctx.send(embed=embed)
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
        """Turn on or off welcome images"""
        if sort == None:
            await ctx.send("**Choose `on` or `off`**")
        if sort == "on":
            await ctx.send("**You have turned on welcome images!**")
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"on_or_off": "on"} }, upsert=True )
        if sort == "off":
            await ctx.send("**You have turned off welcome images**")
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"on_or_off": "off"} }, upsert=True )
            
    @commands.command(aliases=['goodbye'])
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx, sort=None):
        """Turn on or off leave messages"""
        if sort == None:
            x = await self.bot.db.leave.find_one({"id": str(ctx.guild.id)})
            channel = int(x['channel'])
            message = x['message']
            embed=discord.Embed(description="Your leave information",color=0x00f200)
            embed.add_field(name="Channel", value=channel, inline=False)
            embed.add_field(name="Message", value=message)
            await ctx.send(embed=embed)
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
        """Turn on or off the modlog"""        
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
    async def logs(self, ctx, sort=None):
        """Turn on or off the logs"""
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
            await self.bot.db.logging.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
            await ctx.send("**I have set the logs channel!**")
        if sort == "off":
            await self.bot.db.logging.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": False} }, upsert=True )
            await ctx.send("**I have turned off logs**")
            
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def antiinvites(self, ctx, sort=None):
        """Turn on or off anti invites"""
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
    async def kick(self, ctx, user:discord.Member,*, reason=None):
        """Kicks a member from your server!"""
        await user.kick()
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: kick", color=0xff7c3e, timestamp = datetime.datetime.utcnow())
        embed.add_field(name="User", value=f"{user} ({user.mention})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(f"Kicked **{user}**")
        channel = int(x['channel'])
        send_channel= self.bot.get_channel(channel)
        await send_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user:discord.Member,*, reason):
        """Bans a member from your server!"""
        await user.ban()
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: Ban", color=0xff0f0f, timestamp = datetime.datetime.utcnow())
        embed.add_field(name="User", value=f"{user} ({user.mention})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(f"Banned **{user}**")
        channel = int(x['channel'])
        send_channel= self.bot.get_channel(channel)
        await send_channel.send(embed=embed)
        em = discord.Embed(title=f"You have been banned from **{ctx.guild.name}**", color=0xff0f0f, timestamp = datetime.datetime.utcnow())
        em.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        em.add_field(name="Reason", value=reason)
        await user.send(embed=em)
        
    @commands.command()   
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user:discord.Member,*, reason):
        """Warn a user to make them a good pep again!"""
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: Warn", color=0xff7c3e, timestamp = datetime.datetime.utcnow())
        embed.add_field(name="User", value=f"{user} ({user.mention})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(f"Warned **{user}**")
        channel = int(x['channel'])
        send_channel= self.bot.get_channel(channel)
        await send_channel.send(embed=embed)
        em = discord.Embed(description=f"Warned in {ctx.guild.name}", color=0xff7c3e)
        em.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        em.add_feild(name="Reason", value=reason)
        await user.send(embed=em)
        
    @commands.command()   
    @commands.has_permissions(manage_channels=True)
    async def mute(self, ctx, user:discord.Member,*, reason):
        """Mute a user so they cant chat"""
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: Mute", color=0xffff37, timestamp = datetime.datetime.utcnow())
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
        """Unmute a user"""
        x = await self.bot.db.modlog.find_one({"id": str(ctx.guild.id)})
        embed=discord.Embed(title="Case: Unmute", color=0x00f200, timestamp = datetime.datetime.utcnow())
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
        """Purge messages from a channel"""        
        try:
            float(number)
        except ValueError:
            return await ctx.send("**The number is invalid.**")
        await ctx.channel.purge(limit=number+1)
  
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def autorole(self, ctx, *, role):
        """Role when someone joins"""
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
    async def addrole(self, ctx, user:discord.Member,*, role:discord.Role):
        """Add a role to a user"""        
        x = discord.utils.get(ctx.guild.roles, name=str(role))
        await user.add_roles(x)
        await ctx.send(f"Added **{str(role)}** to **{user}**")           

    @commands.command(aliases=['rrole'])
    @commands.has_permissions(manage_roles = True)
    async def removerole(self, ctx, user:discord.Member,*, role:discord.Role):
        """Remove a role from a user"""        
        x = discord.utils.get(ctx.guild.roles, name=role)
        await user.remove_roles(x)
        await ctx.send(f"Removed **{role}** from **{user}**")         

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def poll(self, ctx,*, question):
        embed=discord.Embed(description=question, color=ctx.author.color, timestamp = datetime.datetime.utcnow())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        x = await ctx.send(embed=embed)
        await x.add_reaction("👍")
        await x.add_reaction("👎")        

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix:str=None):
        """Set my prefix for the server"""
        if prefix == None:
            y = await self.bot.db.prefixes.find_one({ "id": ctx.guild.id })
            if not y:
                return await ctx.send("My prefix in this guild is: `-`")
            await ctx.send(f"My prefix in this guild is: `{y['prefix']}`")
        else:
            if len(prefix) > 5:
                return await ctx.send("It needs to be lower than 5 characters!")
            await self.bot.db.prefixes.update_one({"id": ctx.guild.id}, { "$set": { "prefix": prefix } }, upsert=True)
            await ctx.send(f"New prefix `{prefix}`")   
        
def setup(bot):
    bot.add_cog(mod(bot))
