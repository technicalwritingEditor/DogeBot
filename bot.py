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
bot.load_extension("cogs.giveaway")

@bot.event
async def on_ready():
    print("Im online") 
    await bot.change_presence(activity=discord.Game(name=";help"))
    
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="My commands", color=0x9b9dff)
    embed.add_field(name="Info", value="`help`, `info`, `invite`", inline=False)
    embed.add_field(name="Fun", value="`roast`, `face`, `lenny`, `tableflip`, `dog`", inline=False)
    embed.add_field(name="Economy", value="`create`, `earn`, `bal`, `daily`", inline=False)
    embed.add_field(name="Images", value="`rip`, `achievement`, `avatar`", inline=False)
    embed.add_field(name="Moderation", value="`welcome`, `leave`, `modlog`, `antiinvites`, `kick`, `ban`, `purge`", inline=False)
    embed.add_field(name="Utility", value="`8ball`, `serverinfo`, `userinfo`", inline=False)
    embed.set_footer(text="I´m a very new bot and in early development, there will come A LOT more commands!")
    await ctx.send(embed=embed)

@bot.command()
async def suggest(ctx,*, suggestion):
    embed=discord.Embed(description=suggestion, color=0x1aff00, timestamp = datetime.datetime.utcnow())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    await bot.get_channel(455724505566937098).send(embed=embed)

@bot.event
async def on_guild_join(guild):
    embed=discord.Embed(description="My name is **Pepe The Frog**\n\nI am meant to be a fun, moderation, and easy to use bot\n\nTo find my commands use `;help`!\n\nNeed any help? Join the support server:\nhttps://discord.gg/Z6d8Ecq",color=0x00ff00)
    await guild.channels[0].send(embed=embed)

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

class premium():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @has_role_in_my_server("premium")
    async def suggestions(self, ctx, sort):
        if sort == None:
            await ctx.send("**`on` or `off`**")
        if sort == "on":
            await ctx.send("**Please mention the channel to set the suggestions in.**")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("**The time is up**")
            if not x.content.startswith("<#") and not x.content.endswith(">"):
                return await ctx.send("**Please mention the channel**")
            channel = x.content.strip("<#").strip(">")
            try:
                channel = int(channel)
            except ValueError:
                return await ctx.send("**Please mention the channel right**")
            await self.bot.db.suggestions.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
            await ctx.send("**I have set the suggestions channel!**")

    @commands.command()
    async def suggest(self, ctx,*, suggestion):
        x = await self.bot.db.suggestions.find_one({"id": str(ctx.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(suggestion)        
        
db = AsyncIOMotorClient(os.environ.get("MONGODB"))
bot.db = db.pepe_my_bot    
    
if not os.environ.get('TOKEN'):
    print("no token found")
bot.run(os.environ.get('TOKEN').strip('"'))
