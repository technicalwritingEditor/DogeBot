import discord
from discord.ext import commands
import random, time

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
        time = str(guild.created_at.strftime("%b %m, %Y, %A, %I:%M %p"))
        embed=discord.Embed(description=f"**{guild.name}**\nOwner: **{guild.owner.mention}**\nMembers: **{len(guild.members)}**\nRoles: **{len(guild.members)}**\nVerification level: **{guild.verification_level}**\nCreated at: **{'%s' % time}**", color=0x06ff06)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member):
        join_time = str(ctx.author.joined_at.strftime("%b %m, %Y, %A, %I:%M %p"))
        embed=discord.Embed(description=f"{user.mention}\nId: **{user.id}**\nRoles: **{len(user.roles)}**\nStatus: **{user.status}**\nJoined at: **{'%s' % join_time}**", color=user.color)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        t1 = time.perf_counter()
        message = await ctx.send("checking ping...")
        t2 = time.perf_counter()
        ping = round((t2-t1)*1000)
        await message.edit(content=f":ping_pong: Pong! `{ping}`ms")                                                     
                            
def setup(bot):
    bot.add_cog(utility(bot))
