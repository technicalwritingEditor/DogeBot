import discord
from discord.ext import commands
import random, asyncio, aiohttp, datetime

class mod():
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, user):
        em = discord.Embed(description=f"Welcome **{user.mention}**!", color=0x9b9dff, timestamp = datetime.datetime.utcnow())
        em.set_author(name=user, icon_url=user.avatar_url)
        x = await self.bot.db.welcome.find_one({"id": str(user.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(embed=em)

    async def on_member_remove(self, user):
        em = discord.Embed(description=f"Goodbye **{user.name}**", color=0x9b9dff, timestamp = datetime.datetime.utcnow())
        em.set_author(name=user, icon_url=user.avatar_url)
        x = await self.bot.db.leave.find_one({"id": str(user.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(embed=em)   
        
    @commands.command()
    async def welcome(self, ctx):
        await ctx.send("Please mention the channel to set welcome messages in.")
        try:
            x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
        except asyncio.TimeoutError:
            return await ctx.send("Request timed out. Please try again.")
        if not x.content.startswith("<#") and not x.content.endswith(">"):
            return await ctx.send("Please properly mention the channel.")
        channel = x.content.strip("<#").strip(">")
        try:
            channel = int(channel)
        except ValueError:
            return await ctx.send("Did you properly mention a channel? Probably not.")
        await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
        await ctx.send("I have set the welcome channel!")
        
    @commands.command()
    async def leave(self, ctx):
        await ctx.send("Please mention the channel to set leave messages in.")
        try:
            x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
        except asyncio.TimeoutError:
            return await ctx.send("The time is up")
        if not x.content.startswith("<#") and not x.content.endswith(">"):
            return await ctx.send("Please mention the channel")
        channel = x.content.strip("<#").strip(">")
        try:
            channel = int(channel)
        except ValueError:
            return await ctx.send("Please mention the channel right")
        await self.bot.db.leave.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
        await ctx.send("I have set the leave channel!")
        
        
def setup(bot):
    bot.add_cog(mod(bot))
