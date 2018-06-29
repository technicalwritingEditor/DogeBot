import discord, datetime
from discord.ext import commands
import os
from motor.motor_asyncio import AsyncIOMotorClient
    
async def getprefix(bot, message):
    if isinstance(message.channel, discord.DMChannel):
        return commands.when_mentioned_or("-")(bot, message)
    try:
        x = bot.db.prefixes.find_one({"id": message.guild.id})
        if not x:
            return "-"
        prefix = x['prefix']
        return commands.when_mentioned_or(prefix)(bot, message)
    except:
        return "-"

bot=commands.Bot(command_prefix=getprefix)
bot.remove_command('help')

bot.load_extension("cogs.fun")
bot.load_extension("cogs.images")
bot.load_extension("cogs.info")
bot.load_extension("cogs.utility")
bot.load_extension("cogs.economy")
bot.load_extension("cogs.mod")
bot.load_extension("cogs.owner")
bot.load_extension("cogs.giveaway")
bot.load_extension("cogs.music")
bot.load_extension("cogs.source")
bot.load_extension("cogs.tags")

@bot.event
async def on_command_error(message,  error):
        print(error)
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
    await bot.change_presence(activity=discord.Game(name=f"-help | {len(bot.guilds)} servers"))
    
@bot.event
async def on_guild_join(guild):
    lol = bot.get_channel(461050385583570954)
    em = discord.Embed(color=discord.Color(value=0x11f95e))
    em.title = "I have joined new server!"
    em.description = f"Server: {guild}"
    em.add_field(name="Members", value=len(guild.members))
    em.add_field(name="Owner", value=guild.owner)
    em.set_thumbnail(url=guild.icon_url)
    em.set_footer(text=f"ID: {guild.id}")
    await lol.send(embed=em)
    try:
        await guild.channels[0].send(f"Hello! Thanks for adding meh!")
    except discord.Forbidden:
        pass
      
@bot.event
async def on_guild_remove(guild):
    lol = bot.get_channel(461050385583570954)
    em = discord.Embed(color=discord.Color(value=0xf44242))
    em.title = "One server less"
    em.description = f"Server: {guild}"
    em.set_footer(text=f"ID: {guild.id}")
    em.set_thumbnail(url=guild.icon_url)
    await lol.send(embed=em)
    
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
        await ctx.send(f"```fix\n- {cmd} -``` ```{x.help}\nUsage: -{x.signature}```")
    elif command is None:
        await ctx.send("That command doesnt exist!")

@bot.command()
@commands.is_owner()
async def load(ctx, cog : str):
    """Loads an extension."""
    try:
        bot.load_extension(f"cogs.{cog}")
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send(f"Loaded cogs.{cog}")


@bot.command()
@commands.is_owner()
async def unload(ctx, cog : str):
    bot.unload_extension(f"cogs.{cog}")
    await ctx.send(f"Unloaded cogs.{cog}")
    
@bot.command()
async def reload(ctx, cog: str):
    x = await ctx.send(f"Reloading {cog}!")
    bot.unload_extension(f"cogs.{cog}")
    bot.load_extension(f"cogs.{cog}")
    await x.edit(content=f"Realoded {cog}!")
 
@bot.command()
async def prefix(ctx, prefix:str):
    await bot.db.prefixes.update_one({"id": ctx.guild.id}, { "$set": { "prefix": newprefix } }, upsert=True)
    await ctx.send(f"New prefix `{newprefix}`")

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
