import discord, datetime
from discord.ext import commands
import os
from motor.motor_asyncio import AsyncIOMotorClient
    
bot=commands.Bot(command_prefix='d!')
bot.remove_command('help')

bot.load_extension("cogs.fun")
bot.load_extension("cogs.images")
bot.load_extension("cogs.info")
bot.load_extension("cogs.utility")
#bot.load_extension("cogs.economy")
bot.load_extension("cogs.mod")
bot.load_extension("cogs.owner")
bot.load_extension("cogs.giveaway")
bot.load_extension("cogs.music")
bot.load_extension("cogs.source")


@bot.event
async def on_command_error(message,  error):
        if isinstance (error, commands.MissingPermissions):
            embed=discord.Embed(color=0xff2d32, timestamp = datetime.datetime.utcnow())
            embed.add_field(name="Error", value=f"{error}")
            await discord.abc.Messageable.send(message.channel, embed=embed)
        if isinstance (error, commands.NotOwner):
            em=discord.Embed(color=0xff2d322, timestamp = datetime.datetime.utcnow())
            em.add_field(name="Error", value="Your not my daddy!")
            await message.channel.send(embed=em)

@bot.event
async def on_ready():
    print("Im online") 
    await bot.change_presence(activity=discord.Game(name="d!help"))
    
@bot.command()
async def help(ctx, cmd: str = None):
    """This thing"""
    if cmd == None:
        embed=discord.Embed(title="My commands", color=0x9b9dff)
        embed.add_field(name="Info", value="`help`, `info`, `invite`", inline=False)
        embed.add_field(name="Fun", value="`roast`, `face`, `lenny`, `tableflip`, `dog`", inline=False)
        embed.add_field(name="Economy", value="`openaccount`, `earn`, `bal`, `daily`", inline=False)
        embed.add_field(name="Images", value="`rip`, `achievement`, `avatar`", inline=False)
        embed.add_field(name="Moderation", value="`welcome`, `leave`, `modlog`, `antiinvites`, `autorole`, `kick`, `ban`, `purge`, `warn`, `mute`, `unmute`", inline=False)
        embed.add_field(name="Music", value="`join`, `play`, `nowplaying`, `playlist`, `pause`, `stop`, `resume`, `clear`")
        embed.add_field(name="Giveaway", value="`start`", inline=False)
        embed.add_field(name="Utility", value="`8ball`, `serverinfo`, `userinfo`, `ping`", inline=False)
        embed.set_footer(text="I´m a very new bot and in early development, there will come A LOT more commands!")
        await ctx.send(embed=embed)
    if cmd:
        x = bot.get_command(cmd)
        await ctx.send(f"```fix\n- {cmd} -``` ```{x.help}\nUsage: d!{x.signature}```")
    elif command is None:
        await ctx.send("That command doesnt exist!")

@bot.command()
@commands.is_owner()
async def cogload(ctx, cog):
    await bot.load_extension(f"cogs.{cog}")
    await ctx.send(f"Loaded the cog {cog}")

@bot.command()
async def unloadcog(ctx, cog):
    await bot.unload_extension(f"cogs.{cog}")
    await ctx.send(f"Unloaded the cog {cog}")

@bot.command()
async def restartcog(ctx, cog):
    await bot.unload_extension(f"cogs.{cog}")
    await bot.load_extension(f"cogs.{cog}")
    await ctx.send(f"Reloaded the cog {cog}")
    
def has_role_in_my_server(name):
    def wrapper(ctx):
        server = bot.get_guild(455305359645736971)
        role = discord.utils.get(server.roles, name=name)
        user = discord.utils.get(server.members, id=ctx.author.id)
        if not user or not role: return False
        return role in user.roles
    return commands.check(wrapper)

@bot.command()
@has_role_in_my_server("premium")
@commands.cooldown(1, 60, commands.BucketType.user)
async def repeat(ctx, times: int,*, content : str):
    for i in range(times):
        await ctx.send(content)
        
db = AsyncIOMotorClient(os.environ.get("MONGODB"))
bot.db = db.pepe_my_bot    
    
if not os.environ.get('TOKEN'):
    print("no token found")
bot.run(os.environ.get('TOKEN').strip('"'))
