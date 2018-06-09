import discord
from discord.ext import commands
import random, asyncio, aiohttp

class fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lenny(self, ctx):
        await ctx.send("( ͡° ͜ʖ ͡°)")

    @commands.command()
    async def face(self, ctx):
        faces=["¯\_(ツ)_/¯", "̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\З= ( ▀ ͜͞ʖ▀) =Ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿", "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)", "ʕ•ᴥ•ʔ", "(▀̿Ĺ̯▀̿ ̿)", "(ง ͠° ͟ل͜ ͡°)ง", "༼ つ ◕_◕ ༽つ", "ಠ_ಠ", "(づ｡◕‿‿◕｡)づ", "̿'̿'\̵͇̿̿\З=( ͠° ͟ʖ ͡°)=Ε/̵͇̿̿/'̿̿ ̿ ̿ ̿ ̿ ̿", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ✧ﾟ･: *ヽ(◕ヮ◕ヽ)", "┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴", "( ͡°╭͜ʖ╮͡° )", "(͡ ͡° ͜ つ ͡͡°)", "(• ε •)", "(ง'̀-'́)ง", "(ಥ﹏ಥ)", "(ノಠ益ಠ)ノ彡┻━┻", "[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "(☞ﾟ∀ﾟ)☞", "| (• ◡•)| (❍ᴥ❍ʋ)", "(◕‿◕✿)", "(ᵔᴥᵔ)", "(¬‿¬)", "(☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)", "(づ￣ ³￣)づ", "ლ(ಠ益ಠლ)", "ಠ╭╮ಠ", "̿ ̿ ̿'̿'\̵͇̿̿\з=(•_•)=ε/̵͇̿̿/'̿'̿ ̿", "(;´༎ຶД༎ຶ`)", "༼ つ  ͡° ͜ʖ ͡° ༽つ", "(╯°□°）╯︵ ┻━┻"]
        face=random.choice(faces)
        await ctx.send(face)

    @commands.command()
    async def tableflip(self, ctx):
        x = await ctx.send(content="┬─┬ノ( º _ ºノ)")
        await asyncio.sleep(1)
        await x.edit(content='(°-°)\\ ┬─┬')
        await asyncio.sleep(1)
        await x.edit(content='(╯°□°)╯    ]')
        await asyncio.sleep(0.2)
        await x.edit(content='(╯°□°)╯  ︵  ┻━┻')

    @commands.command()
    async def roast(self, ctx, user: discord.Member):
        roasts = ["your ass must be pretty jealous of all the shit that comes out of your mouth.","some day you'll go far, and I hope you stay there.","I'm trying my absolute hardest to see things from your perspective, but I just can't get my head that far up my ass.","I'm not a protocolgist, but I know an asshole when I see one.","Do yourself a favor and ignore anyone who tels you to be yourself. Bad idea in your case.","Everyone's entitled to act stupid once in awhile, but you really abuse the privilege.","Can you die of constipation? I ask because I'm worried about how full of shit you are.","Sorry, I didn't get that. I don't speak bullshit.","There are some remarkably dumb people in this world. Thanks for helping me understand that.","I could eat a bowl of alphabet soup and shit out a smarter statement than whatever you just said.","You always bring me so much joy, as soon as you leave the room.","I'd tell you how I really feel, but I wasn't born with enough middle fingers to express myself in this case.","You have the right to remain silent because whatever you say will probably be stupid anyway.","your family tree must be a cactuss because you're all a bunch of pricks.","You'll never be the man your mom is.","If laughter is the best medicine, your face must be curing the world.","scientists say the universe is made up of neutrons, protons and electrons. They forgot to mention morons, as you are one.","if you really want to know about mistakes, you should ask your parents.","I thought of you today. It reminded me to take the garbage out.","you're such a beautiful, intelligent, wonderful person. Oh I'm sorry, I thought we were having a lying competition.","I may love to shop but I'm not buying your bullshit.","I just stepped in something that was smarter than you, and smelled better too."]
        roast = random.choice(roasts)
        if user.id == 454285151531433984:
            await ctx.send(f"**{ctx.author.name}** I aint going to roast myself faggot!")
        else:
            await ctx.send("**{}** | {}".format(user.name, roast)) 
                    
    @commands.command(name="dog")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dog_command(self, ctx):
        """Shows random dogs"""
        api = "https://api.thedogapi.co.uk/v2/dog.php"
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as r:
                if r.status == 200:
                    response = await r.json()
                    embed = discord.Embed(color = 0x05fa5b)
                    embed.set_author(name = "{} here is your random dog".format(ctx.message.author.name))
                    embed.set_image(url = response['data'][0]["url"])
                    await ctx.send(embed = embed)         

    @commands.command()
    async def pokemon(self, ctx):
	    num = random.randint(1, 926)
	    async with aiohttp.ClientSession().get(f'https://pokeapi.co/api/v2/pokemon-form/{num}/') as resp:
		    data = await resp.json()
	    embed = discord.Embed(title='Who\'s that pokemon?')
	    embed.set_image(url=data['sprites']['front_default'])
	    await ctx.send(embed=embed)
	    await self.bot.db.configs.update_one({ "id": ctx.author.id }, { "$set": { "pokemon": data['id'] } }, upsert=True)
		
    @commands.command()
    async def inventory(self,ctx):
        user = await self.bot.db.configs.find_one({ "id": ctx.author.id })
# None if not found
# otherwise has attributes of the data
        await ctx.send(user.pokemon)
                    
        
def setup(bot):
    bot.add_cog(fun(bot))
