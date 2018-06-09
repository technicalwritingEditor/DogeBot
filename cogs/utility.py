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
    @commands.has_permissions(manage_guild = True)
    async def prefix(self, ctx, prefix=None):
        em = discord.Embed(color=discord.Color(value=0x00ff00), title="Bot Prefix")
        if prefix is None:
            em.description = f"The bot's prefix for server **{ctx.guild.name}** is set to `{ctx.prefix}`."
            return await ctx.send(embed=em)
        if prefix.lower() == 'clear':
            await self.bot.db.prefix.update_one({"id": str(ctx.guild.id)}, {"$set": {"prefix": "*"}}, upsert=True)
            em.description = f"The bot's prefix is now set to the default: `*`."
            return await ctx.send(embed=em)
        else:
            await self.bot.db.prefix.update_one({"id": str(ctx.guild.id)}, {"$set": {"prefix": prefix}}, upsert=True)
            em.description = f"The bot's prefix for this server is set to: `{prefix}`."
            return await ctx.send(embed=em)
        
def setup(bot):
    bot.add_cog(utility(bot))
