import discord, datetime
from discord.ext import commands
import os

bot=commands.Bot(command_prefix='-')
bot.remove_command('help')

bot.load_extension("cogs.fun")
bot.load_extension("cogs.images")
bot.load_extension("cogs.info")
bot.load_extension("cogs.utility")
bot.load_extension("cogs.music")
@bot.event
async def on_ready():
    print("Im online")

@bot.event
async def on_member_join(member):
    embed=discord.Embed(description=f"New member **{member.mention}** :tada:", color=0x9b9dff, timestamp = datetime.datetime.utcnow())
    guild = member.guild
    if guild.id == 454634784669433859:
        channel = bot.get_channel(454707800627740672)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    embed=discord.Embed(description=f"Member left **{member}**", color=0x9b9dff, timestamp = datetime.datetime.utcnow())
    guild = member.guild
    if guild.id == 454634784669433859:
        channel = bot.get_channel(454707800627740672)
        await channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="My commands", color=0x9b9dff)
    embed.add_field(name="Info", value="`help` `info` `invite`", inline=False)
    embed.add_field(name="Fun", value="`roast` `face` `lenny` `tableflip`", inline=False)
    embed.add_field(name="Images", value="`rip` `achievement` `avatar`")
    embed.add_field(name="Utility", value="`8ball` `serverinfo` `userinfo`", inline=False)
    embed.set_footer(text="I´m a very new bot and in early development, there will come A LOT more commands!")
    await ctx.send(embed=embed)

if not os.environ.get('TOKEN'):
    print("no token found")
bot.run(os.environ.get('TOKEN').strip('"'))
