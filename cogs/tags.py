import discord
from discord.ext import commands
import random, asyncio, aiohttp, datetime

class tags():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx, name,*, description):
        await self.bot.db.tags.update_one({"name": name}, {"$set": {"Description": description} }, upsert=True )
        await ctx.send(f"Created tag called {name}")

    @commands.command()
    async def search(self, ctx,*,name):
        x = await self.bot.db.tags.find_one({"name": name })
        await ctx.send(x['description'])

def setup(bot):
    bot.add_cog(tags(bot))
