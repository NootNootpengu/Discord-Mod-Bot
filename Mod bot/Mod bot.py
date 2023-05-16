# Welcome to Mod bot made by Saul Nootman
from dotenv import load_dotenv
import datetime
import discord
from discord.ext import commands
import os

load_dotenv()
token = os.getenv("token")

prefix = "<"
print("Loading..")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"bot ready for action. {bot.user.name}#{bot.user.discriminator}, {bot.user.id}")
    print(f"the bot is in {len(bot.guilds)} guilds")
    for guilds in bot.guilds:
        print(f"Guild name: {guilds.name}, Guild ID: {guilds.id}, Guild owner name: {guilds.owner.name}#{guilds.owner.discriminator}, Guild owner ID: {guilds.owner.id}")


@bot.command()
async def create_invite(ctx):
    invite = await ctx.channel.create_invite(max_age=300)
    link = discord.utils.resolve_invite(invite)
    server = await bot.fetch_invite(f"{link}")
    await ctx.send(server)


@bot.command()
async def members(ctx):
    members = []
    for n in bot.get_all_members():
        if 1081610766928597093 in n.roles:
            continue
        else:
            members.append(f"{n.name}#{n.discriminator}")
    members = list(dict.fromkeys(members))
    members.sort()
    await ctx.send(members)


@bot.command(description="Ban a user. needed argument is Member and Reason")
async def ban(ctx, *, member: discord.Member, reason=f"{None}"):
    global embed
    if not ctx.author.guild_permissions.ban_members:
        embed = discord.Embed(
            title="Missing Perms",
            description=f"{ctx.author.mention}, you don't have enough perms."
        )
        await ctx.send(embed=embed)
        return
    else:
        try:
            await member.ban()
            embed = discord.Embed(
                title="Ban",
                description=f"{member.mention} has been banned by {ctx.author.mention} for {reason}."
            )
            imageurl = f'{member.display_avatar}'
            embed.set_image(url=imageurl)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Unsuccessful command")
        try:
            await ctx.member.send(embed)
        except:
            pass


@bot.command(description="Kicks a user. needed argument is Member and Reason")
async def kick(ctx, *, member: discord.Member, reason=f"[No reason Provided]"):
    global embed
    if not ctx.author.guild_permissions.kick_members:
        embed = discord.Embed(
            title="Missing Perms",
            description=f"{ctx.author.mention}, you don't have enough perms."
        )
        await ctx.send(embed=embed)
        return
    try:
        await member.ban()
        embed = discord.Embed(
            title="Kick",
            description=f"{member.mention} has been kicked by {ctx.author.mention} for {reason}."
        )
        imageurl = f'{member.display_avatar}'
        embed.set_image(url=imageurl)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Unsuccessful command")
    try:
        await ctx.member.send(embed)
    except:
        pass


@bot.command(description="Purges a channel")
async def purge(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        embed = discord.Embed(
            title="Missing Perms",
            description=f"{ctx.author.mention}, you don't have enough perms."
        )
        await ctx.send(embed=embed)
        return
    await ctx.channel.delete()
    new_channel = await ctx.channel.clone(reason="Channel was purged")
    await new_channel.edit(position=ctx.channel.position)
    embed = discord.Embed(
        title="Purge",
        description=f"Channel was purged by {ctx.author.mention}."
    )
    imageurl = f'{ctx.author.display_avatar}'
    embed.set_image(url=imageurl)
    bot.get_channel(new_channel.id)
    await ctx.new_channel.send(embed=embed)


@bot.command(description="times out a user. needed argument are member, seconds, minutes, hours, days and reason")
async def mute(ctx, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0,
               reason: str = "Just cause."):
    global embed
    duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
    if not ctx.author.guild_permissions.timeout_members:
        embed = discord.Embed(
            title="Missing Perms",
            description=f"{ctx.author.mention}, you don't have enough perms."
        )
    try:
        await member.timeout(duration, reason=reason)
        embed = discord.Embed(
            title="Time_out",
            description=f"{member.mention} has been timed out by {ctx.author.mention} for {duration}, because {reason}."
        )
        imageurl = f'{member.display_avatar}'
        embed.set_image(url=imageurl)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Unsuccessful command.")
    try:
        await ctx.member.send(embed)
    except:
        pass


try:
    bot.run(token)
except discord.LoginFailure:
    print('Invalid Token Passed')
