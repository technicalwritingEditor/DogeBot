import discord, datetime
from discord.ext import commands
import os
from motor.motor_asyncio import AsyncIOMotorClient

bot=commands.Bot(command_prefix='-')
bot.remove_command('help')

bot.load_extension("cogs.fun")
bot.load_extension("cogs.images")
bot.load_extension("cogs.info")
bot.load_extension("cogs.utility")
bot.load_extension("cogs.pokemon")

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

@bot.event
async def on_reaction_add(reaction, user):
        if reaction.emoji == "⭐":
            embed=discord.Embed(title="Starboard", description=reaction.message.content, color=0xffff80)
            embed.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url)
            try:
                img_url = reaction.message.attachments[0].url
                if img_url:
                    embed.set_image(url=str(img_url))
            except IndexError:
                img_url = None
            guild = reaction.message.guild
            if guild.id == 454634784669433859:
                channel=bot.get_channel(454974580222853141)
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

db = AsyncIOMotorClient(os.environ.get("MONGODB"))
bot.db = db.pepe_my_bot    
    
if not os.environ.get('TOKEN'):
    print("no token found")
bot.run(os.environ.get('TOKEN').strip('"'))
