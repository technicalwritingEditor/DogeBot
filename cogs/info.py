import discord
from discord.ext import commands
import datetime, time, psutil

start_time = time.time()
starttime2 = time.ctime(int(time.time()))

class info():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        second = time.time() - start_time
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        RAM = psutil.virtual_memory()
        used = RAM.used >> 20
        percent = RAM.percent
        embed=discord.Embed(title="Stats about {self.bot.name}", color=0x9b9dff)
        embed.set_thumbnail(url=self.bot.avatar_url)
        embed.add_field(name="Uptime", value="**%dd %dh %dm %ds**"% (day, hour, minute, second), inline=False)
        embed.add_field(name="Servers", value=f"**{len(self.bot.guilds)}", inline=False)
        embed.add_field(name="Memory used", value=f"{used}MB {percent}%", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed=discord.Embed(description="**Invite me or join my support guild!**\n[Invite](https://discordapp.com/oauth2/authorize?client_id=454285151531433984&permissions=8&scope=bot)\n[Support guild](https://discord.gg/Z6d8Ecq)", color=0x9b9dff)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(info(bot))
