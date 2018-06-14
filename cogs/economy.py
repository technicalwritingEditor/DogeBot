import discord
from discord.ext import commands
import random, asyncio, aiohttp
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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
    img = Image.open("maxresdefault.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("American Captain.otf", 75)
    fontbig = ImageFont.truetype("American Captain.ttf", 100)
    #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
    draw.text((100, 0), "{}´s bal".format(ctx.author), (255, 255, 255), font=fontbig)
    draw.text((150, 125), "{}".format(user['money']), (255, 255, 255), font=font)
    img.save(f'{user.id}.jpg')
    await ctx.send(file=discord.File(f'{user.id}.jpg'))

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)                  
    async def work(self, ctx):
        x = random.randint(100, 1000)
        user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
        current = user['money']
        self.bot.db.configs.update_one( { "id": ctx.author.id}, { "$set": { "money": current + x} })
        await ctx.send(f"You have worked and gained {x} :dollar:")                       
              
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        x = random.randint(500, 10000)
        user = await self.bot.db.configs.find_one( { "id": ctx.author.id } )
        current = user['money']
        self.bot.db.configs.update_one( { "id": ctx.author.id}, { "$set": { "money": current + x} })
        await ctx.send(f"Your daily gave you {x}:dollar:!\n`Come back in 24 hours and claim your next daily!`")                                
                       
def setup(bot):
    bot.add_cog(economy(bot))
