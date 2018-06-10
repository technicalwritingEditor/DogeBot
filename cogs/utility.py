import discord
from discord.ext import commands
import random

class utility():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def eight_ball(self, ctx,*, question):
        answers = ["Yes", "No", "Ask later", "Such a silly question", "of course"]
        answer = random.choice(answers)
        embed=discord.Embed(description=f"Question: **{question}**\n\nAnswer: **{answer}**", color=0x9b9dff)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed=discord.Embed(description=f"**{guild.name}**\nOwner: **{guild.owner.mention}**\nMembers: **{len(guild.members)}**\nRoles: **{len(guild.members)}**\nVerification level: **{guild.verification_level}**\nCreated at: **{guild.created_at}**", color=0x06ff06)
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member):
        embed=discord.Embed(description=f"{user.mention}\nId: **{user.id}**\nRoles: **{len(user.roles)}**\nStatus: **{user.status}**\nJoined at: **{user.joined_at}**", color=user.color)
        await ctx.send(embed=embed)
         
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
            
def setup(bot):
    bot.add_cog(utility(bot))
