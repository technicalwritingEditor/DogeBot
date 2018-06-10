import discord, datetime
from discord.ext import commands
import os
from motor.motor_asyncio import AsyncIOMotorClient
    
bot=commands.Bot(command_prefix=';')
bot.remove_command('help')

bot.load_extension("cogs.fun")
bot.load_extension("cogs.images")
bot.load_extension("cogs.info")
bot.load_extension("cogs.utility")
bot.load_extension("cogs.economy")
bot.load_extension("cogs.mod")

@bot.event
async def on_ready():
    print("Im online") 
        
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="My commands", color=0x9b9dff)
    embed.add_field(name="Info", value="`help` `info` `invite`", inline=False)
    embed.add_field(name="Fun", value="`roast` `face` `lenny` `tableflip` `dog`", inline=False)
    embed.add_field(name="Economy", value="`create` `work` `bal` `daily`", inline=False)
    embed.add_field(name="Images", value="`rip` `achievement` `avatar`", inline=False)
    embed.add_field(name="Moderation", value="`welcome` `leave`", inline=False)
    embed.add_field(name="Utility", value="`8ball` `serverinfo` `userinfo`", inline=False)
    embed.set_footer(text="I´m a very new bot and in early development, there will come A LOT more commands!")
    await ctx.send(embed=embed)

db = AsyncIOMotorClient(os.environ.get("MONGODB"))
bot.db = db.pepe_my_bot    
    
if not os.environ.get('TOKEN'):
    print("no token found")
bot.run(os.environ.get('TOKEN').strip('"'))
