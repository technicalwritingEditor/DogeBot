import discord
from discord.ext import commands
import datetime
import sys
import asyncio
import os
import aiohttp
import json
import youtube_dl
from discord.ext.commands.cooldowns import BucketType


YOUTUBE_DL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto'
}


ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(YOUTUBE_DL_OPTIONS)



class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    def get_duration(self):
        return self.data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.skip_votes = set()
        

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()


class Music:
    def __init__(self, bot):
       self.bot = bot
       self.queue = {}

    async def next_song(self, ctx, loop):
        if len(self.queue[str(ctx.guild.id)]) is 0:
            await ctx.voice_client.disconnect()
            await ctx.send("**No songs are left in the queue**")
        #player = await YTDLSource.from_url(self.queue[str(ctx.guild.id)][0], loop=loop)
        player = self.queue[str(ctx.guild.id)][0]
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.next_song(ctx, loop), loop=self.bot.loop).result())
        self.queue[str(ctx.guild.id)].remove(self.queue[str(ctx.guild.id)][0])
        msg = await ctx.send(f"**Playing {player.title}**")
        await asyncio.sleep(15)
        await msg.edit(f"**Playing {player.title}**")

    @commands.command(aliases=["join"])
    async def summon(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("**You are not in a channel**")
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            await ctx.send(f"**Connected to {ctx.author.voice.channel.name}**")
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            await ctx.send(f"**Connected to {ctx.author.voice.channel.name}**")


    @commands.command(aliases=["leave"])
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("**I am not in a channel**")
        else:
            await ctx.voice_client.disconnect()
            await ctx.send(f"**Disconnected from {ctx.author.voice.channel.name}**")

    @commands.command()
    async def play(self, ctx, *, url):
        """Search for a YouTube video to play, by name."""
        if ctx.author.voice is None:
            return await ctx.send("**You are not in a channel**")
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        if not ctx.voice_client.is_playing():
            try:            
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
            except youtube_dl.DownloadError:
                return await ctx.send("**Couldn't find that**")
            try:
                ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.next_song(ctx, self.bot.loop), loop=self.bot.loop).result())
            except discord.Forbidden:
                return await ctx.send("**I don't have permissions to play in this channel.**")
            msg = await ctx.send(f"**Now playing {player.title} requested by {ctx.author}**")
        else:
            try:
                to_play = await YTDLSource.from_url(url, loop=self.bot.loop)
            except youtube_dl.DownloadError:
                return await ctx.send("**Couldn't find any video with that name. Try something else.**")
            try:
                self.queue[str(ctx.guild.id)].append(to_play)
            except KeyError:
                self.queue[str(ctx.guild.id)] = [to_play]
            await ctx.send(f"**Added {to_play.title} to the queue. Requested by {ctx.author}**")

    @commands.command()
    async def pause(self, ctx):
        """Pauses whatever is playing."""
        if ctx.voice_client is None:
            return await ctx.send("**I am not connected to a channel**")
        ctx.voice_client.pause()
        await ctx.send("**Music has been paused ⏸**")

    @commands.command()
    async def resume(self, ctx):
        """Resumes whatever isn't playing."""
        if ctx.voice_client is None:
            return await ctx.send("**I am not connected to a channel**")
        ctx.voice_client.resume()
        await ctx.send("**Music has been resumed** ▶")

    @commands.command()
    async def stop(self, ctx):
        """Stops the current song."""
        if ctx.voice_client is None:
            return await ctx.send("**I am not connected to a channel**")
        await ctx.send("**Music has been stopped and i left your channel** ⏹")
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(name="queue")
    async def _queue(self, ctx):
        """Gets the queue for the server."""
        em = discord.Embed(color=0x9b9dff, title=f"Music Queue")
        em.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        try:
            song_list = self.queue[str(ctx.guild.id)]
        except KeyError:
            em.description = "**No songs are currently in the queue**"
            return await ctx.send(embed=em)
        songs = ""
        count = 0
        for x in song_list:
            count += 1
            songs += f"Positon {str(count)}: **{x.title}**\n"
        em.description = songs if song_list != [] else "**No songs are currently in the queue**"
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Music(bot))
    print("Music is loaded")
