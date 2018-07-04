import discord
from discord.ext import commands
import random, asyncio, aiohttp

class economy():
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, message,  error):
        if isinstance(error, commands.CommandOnCooldown):
            await discord.abc.Messageable.send(message.channel, error)              
        
    async def is_registered():
        self.bot.db.configs.find_one({"id": ctx.author.id})
    

        
    @commands.command()
    async def openaccount(self, ctx):
        """"Create a bank account, if you already have one it will get reseted"""
        if is_registered:
            await ctx.send("You are already registered")
        self.bot.db.configs.update_one( { "id": ctx.author.id }, { "$set": { "money": 0 } }, upsert=True )
        await ctx.send("Created account for ya")

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        """"See your current balance"""
        user = await self.bot.db.configs.find_one({ "id": ctx.author.id })
        await ctx.send(f"{ctx.author.mention} | Your bal: **{user['money']}**:dollar: ")     

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)                  
    async def earn(self, ctx):
        """Earn some cash"""
        x = random.randint(100, 1000)
        user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
        current = user['money']
        self.bot.db.configs.update_one( { "id": ctx.author.id}, { "$set": { "money": current + x} })
        await ctx.send(f"You have earned {x} :dollar:")                       
              
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """Get your daily cash"""
        x = random.randint(500, 10000)
        user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
        current = user['money']
        self.bot.db.configs.update_one( { "id": ctx.author.id}, { "$set": { "money": current + x} })
        await ctx.send(f"Your daily gave you {x}:dollar:!\n`Come back in 24 hours and claim your next daily!`")                                
                    
                         
def setup(bot):
    bot.add_cog(economy(bot))
