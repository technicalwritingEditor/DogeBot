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
bot.load_extension("cogs.owner")

@bot.event
async def on_ready():
    print("Im online") 
    await bot.change_presence(activity=discord.Game(name=";help"))

@bot.event
async def on_guild_join(guild):
    guild = ctx.guild
    embed=discord.Embed(description="Thanks for inviting me!\nI am being developed by **Vilgot#7447**\nInvite me [here](https://discordapp.com/oauth2/authorize?client_id=454285151531433984&permissions=8&scope=bot) or join my support guild [here](https://discord.gg/Z6d8Ecq)"
        await guild.channels[0].send(embed=embed) 

    
    
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="My commands", color=0x9b9dff)
    embed.add_field(name="Info", value="`help`, `info`, `invite`", inline=False)
    embed.add_field(name="Fun", value="`roast`, `face`, `lenny`, `tableflip`, `dog`", inline=False)
    embed.add_field(name="Economy", value="`create`, `work`, `bal`, `daily`", inline=False)
    embed.add_field(name="Images", value="`rip`, `achievement`, `avatar`", inline=False)
    embed.add_field(name="Moderation", value="`welcome`, `leave`, `modlog`, `antiinvites`", inline=False)
    embed.add_field(name="Utility", value="`8ball`, `serverinfo`, `userinfo`", inline=False)
    embed.set_footer(text="I´m a very new bot and in early development, there will come A LOT more commands!")
    await ctx.send(embed=embed)

@bot.command()
async def suggest(ctx,*, suggestion):
    embed=discord.Embed(description=suggestion, color=0x1aff00, timestamp = datetime.datetime.utcnow())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    await bot.get_channel(455724505566937098).send(embed=embed)
    
db = AsyncIOMotorClient(os.environ.get("MONGODB"))
bot.db = db.pepe_my_bot    
    
if not os.environ.get('TOKEN'):
    print("no token found")
bot.run(os.environ.get('TOKEN').strip('"'))
