import discord
from discord.ext import commands
import random, asyncio, aiohttp, datetime

class premium():
    def __init__(self, bot):
        self.bot = bot

    def has_role_in_my_server(self):
        def wrapper(self, ctx):
            server = self.bot.get_guild(455305359645736971)
            role = discord.utils.get(server.roles, name="premium")
            user = discord.utils.get(server.members, id=ctx.author.id)
            if not user or not role: return False
            return role in user.roles
        return commands.check(wrapper)

    @commands.command()
    @has_role_in_my_server()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def bigearn(self, ctx):
        x = random.randint(10000, 100000)
        user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
        current = user['money']
        self.bot.db.configs.update_one( { "id": ctx.author.id}, { "$set": { "money": current + x} })
        await ctx.send(f"Your bigearn gave you {x}:dollar:!")      

def setup(bot):
    bot.add_cog(premium(bot))
