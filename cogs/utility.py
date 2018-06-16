import discord
from discord.ext import commands
import random, time

class utility():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def eight_ball(self, ctx,*, question):
        answers = ["Yes", "No", "Ask later", "Such a silly question", "of course"]
        answer = random.choice(answers)
        embed=discord.Embed(description=f"Question: **{question}**\n\nAnswer: **{answer}**", color=0x9b9dff)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        time = str(guild.created_at.strftime("%b %m, %Y, %A, %I:%M %p"))
        embed=discord.Embed(description=f"**{guild.name}**\nOwner: **{guild.owner.mention}**\nMembers: **{len(guild.members)}**\nRoles: **{len(guild.members)}**\nVerification level: **{guild.verification_level}**\nCreated at: **{'%s' % time}**", color=0x06ff06)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member):
        join_time = str(ctx.author.joined_at.strftime("%b %m, %Y, %A, %I:%M %p"))
        embed=discord.Embed(description=f"{user.mention}\nId: **{user.id}**\nRoles: **{len(user.roles)}**\nStatus: **{user.status}**\nJoined at: **{'%s' % join_time}**", color=user.color)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        t1 = time.perf_counter()
        message = await ctx.send("checking ping...")
        t2 = time.perf_counter()
        ping = round((t2-t1)*1000)
        await message.edit(content=f":ping_pong: Pong! `{ping}`ms")                            

    @commands.command()
    @commands.guild_only()
    async def roleinfo(self, ctx, *, rolename):
        try:
            role = discord.utils.get(ctx.guild.roles, name=rolename)
        except:
            return await ctx.send("Role not found. Please make sure the role name is correct. (Case Sensitive!)")
        em = discord.Embed(color=role.color, title=f'Role Info: {rolename}')
        p = ""
        if role.permissions.administrator:
            p += "Administrator :white_check_mark: \n"
        else:
            p += "Administrator :x: \n"
        if role.permissions.create_instant_invite:
            p += "Create Instant Invite :white_check_mark: \n"
        else:
            p += "Create Instant Invite :x:\n"
        if role.permissions.kick_members:
            p += "Kick Members :white_check_mark: \n"
        else:
            p += "Kick Members :x:\n"
        if role.permissions.ban_members:
            p += "Ban Members :white_check_mark: \n"
        else:
            p += "Ban Members :x:\n"
        if role.permissions.manage_channels:
            p += "Manage Channels :white_check_mark: \n"
        else:
            p += "Manage Channels :x:\n"
        if role.permissions.manage_guild:
            p += "Manage Server :white_check_mark: \n"
        else:
            p += "Manage Server :x:\n"
        if role.permissions.add_reactions:
            p += "Add Reactions :white_check_mark: \n"
        else:
            p += "Add Reactions :x:\n"
        if role.permissions.view_audit_log:
            p += "View Audit Log :white_check_mark: \n"
        else:
            p += "View Audit Log :x:\n"
        if role.permissions.read_messages:
            p += "Read Messages :white_check_mark: \n"
        else:
            p += "Read Messages :x:\n"
        if role.permissions.send_messages:
            p += "Send Messages :white_check_mark: \n"
        else:
            p += "Send Messages :x:\n"
        if role.permissions.send_tts_messages:
            p += "Send TTS Messages :white_check_mark: \n"
        else:
            p += "Send TTS Messages :x:\n"
        if role.permissions.manage_messages:
            p += "Manage Messages :white_check_mark: \n"
        else:
            p += "Manage Messages :x:\n"
        if role.permissions.embed_links:
            p += "Embed Links :white_check_mark: \n"
        else:
            p += "Embed Links :x:\n"
        if role.permissions.attach_files:
            p += "Attach Files :white_check_mark: \n"
        else:
            p += "Attach Files \n" 
        if role.permissions.read_message_history:
            p += "Read Message History :white_check_mark: \n"
        else:
            p += "Read Message History :x:\n"
        if role.permissions.mention_everyone:
            p += "Mention @everyone :white_check_mark: \n"
        else:
            p += "Mention @everyone :x:\n"
        if role.permissions.external_emojis:
            p += "Use External Emojis :white_check_mark: \n"
        else:
            p += "Use External Emojis :x:\n"
        if role.permissions.change_nickname:
            p += "Change Nicknames :white_check_mark: \n"
        else:
            p += "Change Nicknames :x:\n"
        if role.permissions.manage_nicknames:
            p += "Manage Nicknames :white_check_mark: \n"
        else:
            p += "Manage Nicknames :x:\n"
        if role.permissions.manage_roles:
            p += "Manage Roles :white_check_mark: \n"
        else:
            p += "Manage Roles :x:\n"
        if role.permissions.manage_webhooks:
            p += "Manage Webhooks :white_check_mark: \n"
        else:
            p += "Manage Webhooks :x:\n"
        if role.permissions.manage_emojis:
            p += "Manage Emojis :white_check_mark: \n"
        else:
            p += "Manage Emojis :x:\n"
        v = "" 
        if role.permissions.connect:
            v += "Connect :white_check_mark: \n"
        else:
            v += "Connect :x:\n"
        if role.permissions.speak:
            v += "Speak :white_check_mark: \n"
        else:
            v += "Speak :x:\n"
        if role.permissions.mute_members:
            v += "Mute Members :white_check_mark: \n"
        else:
            v += "Mute Members :x:\n"
        if role.permissions.deafen_members:
            v += "Deafen Members :white_check_mark: \n"
        else:
            v += "Deafen Members :x:\n"
        if role.permissions.move_members:
            v += "Move Members :white_check_mark: \n"
        else:
            v += "Move Members :x:\n"
        if role.permissions.use_voice_activation:
            v += "Use Voice Activation :white_check_mark: \n"
        else:
            v += "Use Voice Activation :x:\n"
        em.description = f"**General Permissions** \n\n{p} \n\n\n**Voice Permissions** \n\n{v}"
        em.add_field(name='ID', value=role.id)
        em.add_field(name='Position from Bottom', value=role.position)
        if role.mentionable:
            a = 'Mentionable'
        else:
            a = 'Not Mentionable'
        em.add_field(name='Mentionable', value=a)
        em.add_field(name='Time Created', value=str(role.created_at.strftime("%A, %b %m, %Y at %I:%M %p")))
        # member = ""
        # for x in role.members:
        #     member += f"{x.name} \n"
        # em.add_field(name='Members in the Role', value=member)
        await ctx.send(embed=em)                            
                            
def setup(bot):
    bot.add_cog(utility(bot))
