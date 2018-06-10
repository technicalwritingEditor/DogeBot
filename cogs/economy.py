import discord
from discord.ext import commands
import random, asyncio, aiohttp

class economy():
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, message,  error):
        if isinstance(error, commands.CommandOnCooldown):
            await discord.abc.Messageable.send(message.channel, error)        
        
    @commands.command()
    async def create(self, ctx):
        self.bot.db.configs.update_one( { "id": ctx.author.id }, { "$set": { "money": 0 } }, upsert=True )
        await ctx.send("Created account for ya")

    @commands.command()
    async def bal(self, ctx):
        user = await self.bot.db.configs.find_one({ "id": ctx.author.id })
        await ctx.send(f"{user['money']} :dollar:")

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)                  
    async def work(self, ctx):
        x = random.randint(100, 1000)
        user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
        current = user['money']
        self.bot.db.configs.update_one( { "id": ctx.author.id}, { "$set": { "money": current + x} })
        await ctx.send(f"You have worked and gained {x} :dollar:")
                
    @commands.command()
    async def createcode(self, ctx, code):
        await self.bot.db.configs.update_one( { "id": self.bot.owner.id }, { "$set": { "code": code } } )
        await ctx.send("Created a code")

    @commands.command()
    async def reedem(self, ctx, code):
        data = await self.bot.db.configs.find_one( { "vilgot": "338600456383234058" } )
        if code == data['code']:
            await ctx.send("Yay")                   
                       
def setup(bot):
    bot.add_cog(economy(bot))
