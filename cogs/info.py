import discord
from discord.ext import commands
import datetime, time

start_time = time.time()
starttime2 = time.ctime(int(time.time()))

class info():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        second = time.time() - start_time
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        embed=discord.Embed(description=f"**Information**\n\n__**Stats**__\nUptime: **%dd %dh %dm %ds**\nServers: **{len(self.bot.guilds)}**\nDiscord.py: **{discord.__version__}**"% (day, hour, minute, second),color=0x9b9dff)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed=discord.Embed(description="**Invite me or join my support guild!**\n[Invite](https://discordapp.com/oauth2/authorize?client_id=454285151531433984&permissions=8&scope=bot)\n[Support guild](https://discord.gg/Z6d8Ecq)", color=0x9b9dff)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(info(bot))
