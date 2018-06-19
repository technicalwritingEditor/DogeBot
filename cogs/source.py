import discord
from discord.ext import commands
import inspect

class source():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def helpsource(self, ctx):
        embed=discord.Embed(color=0xe156f1)
        embed.add_field(name="source", value="Source code of any of my commands", inline=False)
        embed.set_thumbnail(url="http://clipground.com/images/clipart-bird-png-9.png")
        await ctx.send(embed=embed)

    @commands.command(name="source")
    async def source(self, context, *, command=None):
        """Get the source code for any of my commands."""
        if command is None:
            source_embed = discord.Embed(color = 0xe156f1)
            source_embed.add_field(name="All source", value="[Click me!](https://github.com/Vilgot/Birdboat)")
            return await context.send(embed=source_embed)

        command=self.bot.get_command(command)
        if command is None:
            error_embed = discord.Embed(color = 0xff2d32)
            error_embed.add_field(name="Error", value="Could´nt find command")
            return await context.send(embed=error_embed)

        source=inspect.getsource(command.callback)
        paginator=commands.Paginator(prefix="```py")
        for line in source.split("\n"):
            paginator.add_line(line=str(line).replace("```", "```").replace("    ", "", 1))

        for page in paginator.pages:
            await context.send(page)


def setup(bot):
    bot.add_cog(source(bot))