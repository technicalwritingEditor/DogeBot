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
        embed = discord.Embed(title='Who\'s that pokemon?')
        embed.set_image(url=data['sprites']['front_default'])
        await ctx.send(embed=embed)
        await self.bot.db.configs.update_one({ "id": ctx.author.id }, { "$set": { "pokemon": data['id'] } }, upsert=True)

    @commands.command()
    async def mypokemon(self, ctx):
        user = await self.bot.db.configs.find_one({ "id": ctx.author.id })
        await ctx.send(user['pokemon'])


def setup(bot):
    bot.add_cog(pokemon(bot))
