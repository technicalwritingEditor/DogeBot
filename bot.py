import discord, datetime
from discord.ext import commands
import os

bot=commands.Bot(command_prefix='-')
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Im online")
    bot.load_extension("cogs.fun")
    print("Loaded fun")
    bot.load_extension("cogs.images")
    print("Loaded images")
    bot.load_extension("cogs.info")
    print("Loaded info")  
    bot.load_extension("cogs.utility")
    print("Loaded utility")


@bot.event
async def on_guild_join(guild):
    embed=discord.Embed(title="New server!", description=f"Guild: **{guild.name}**", color=0x9b9dff, timestamp = datetime.datetime.utcnow())
    embed.set_footer(text=f"Id: {guild.id}")
    channel = bot.get_channel(453822303827132416)
    await channel.send(embed=embed)

@bot.event
async def on_guild_remove(guild):
    embed=discord.Embed(title="Left server!", description=f"Guild: **{guild.name}**", color=0x9b9dff, timestamp = datetime.datetime.utcnow())
    embed.set_footer(text=f"Id: {guild.id}")
    channel = bot.get_channel(453822303827132416)
    await channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    embed=discord.Embed(description=f"New member **{member.mention}** :tada:", color=0x9b9dff, timestamp = datetime.datetime.utcnow())
    guild = member.guild
    if guild.id == 453812812272107521:
        channel = bot.get_channel(453812948360757258)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    embed=discord.Embed(description=f"Member left **{member}**", color=0x9b9dff, timestamp = datetime.datetime.utcnow())
    guild = member.guild
    if guild.id == 453812812272107521:
        channel = bot.get_channel(453812948360757258)
        await channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="My commands", color=0x9b9dff)
    embed.add_field(name="Info", value="`help` `info`", inline=False)
    embed.add_field(name="Fun", value="`roast` `face` `lenny` `tableflip`", inline=False)
    embed.add_field(name="Images", value="`rip` `achievement` `avatar`")
    embed.add_field(name="Utility", value="`8ball` `serverinfo` `userinfo`", inline=False)
    embed.set_footer(text="I´m a very new bot and in early development, there will come A LOT more commands!")
    await ctx.send(embed=embed)

bot.run("NDUzODI5NjUyNzkyODY4ODY2.DfmKfw.Zfdmywrc5PmjeVZrLAMY2xcA9EQ")