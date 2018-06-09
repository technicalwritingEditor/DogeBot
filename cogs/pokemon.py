import discord
from discord.ext import commands
import random, asyncio, aiohttp

class pokemon():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pokemon(self, ctx):
        num = random.randint(1, 926)
        async with aiohttp.ClientSession().get(f'https://pokeapi.co/api/v2/pokemon-form/{num}/') as resp:
            data = await resp.json()
        await ctx.send(f"You catched a {data['name']} {data['sprites']['front_default']}")
        await self.bot.db.configs.update_one({ "id": ctx.author.id }, { "$set": { "pokemon": data['sprites']['front_default'] } }, upsert=True)

    @commands.command()
    async def mypokemon(self, ctx):
        user = await self.bot.db.configs.find_one({ "id": ctx.author.id })
        await ctx.send(user['pokemon'])


def setup(bot):
    bot.add_cog(pokemon(bot))
