import discord
from discord.ext import commands
import random, asyncio, aiohttp

class economy():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        self.bot.db.configs.update_one( { "id": ctx.author.id }, { "$set": { "money": 0 } }, upsert=True )

    @commands.command()
    async def bal(self, ctx):
        user = await self.bot.db.configs.find_one({ "id": ctx.author.id })
        await ctx.send(f"{user['money']} :dollar:")

    @commands.command()
    async def work(self, ctx):
        user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
        current = user['money']
        self.bot.db.configs.update_one( { "id": ctx.author.id}, { "$set": { "money": current + 50} })
        await ctx.send("You have worked and gained 50 :dollar:")
        
def setup(bot):
    bot.add_cog(economy(bot))
