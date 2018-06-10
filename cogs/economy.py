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
    async def daily(self, ctx):
        x = random.randint(500, 10000)
        user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
        current = user['money']
        self.bot.db.configs.update_one( { "id": ctx.author.id}, { "$set": { "money": current + x} })
        await ctx.send(f"Your daily gave you {x}:dollar:!\n`Come back in 24 hours and claim your next daily!`")

    @commands.command()
    @commands.is_owner()
    async def createcode(self, ctx, code, money_by_code):
        await self.bot.db.configs.update_one( { "id": ctx.author.id }, { "$set": { "code": code } } )
        await self.bot.db.configs.update_one( { "id": ctx.author.id }, { "$set": { "code_money": money_by_code } } )
        await ctx.send("Created a code")

    @commands.command()
    async def reedem(self, ctx, code):
        data = await self.bot.db.configs.find_one( { "id": 338600456383234058 } )
        if code == data['code']:
            user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
            current = user['money']
            code_money_code = data['code_money']
            self.bot.db.configs.update_one( { "id": ctx.author.id }, { "$set": { "money": current + code_money_code} } )               
                       
                       
def setup(bot):
    bot.add_cog(economy(bot))
