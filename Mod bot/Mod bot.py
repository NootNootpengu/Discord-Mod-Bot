# Welcome to Mod bot made by Saul Nootman#2864
# Did you know you have rights?
# well this is made for you!
# so you can enforce those rights on your server members
# Noot Noot.
# -signed with blood
# P.S. if you steal my code, i will find you.
# your rights will not help you that day.
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv
from datetime import datetime
import datetime
import discord
from discord.ext import commands
import os
import pytz




load_dotenv()
token = os.getenv("token")

prefix = "<"
print("Loading...")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    os.system('cls')
    print(f"bot ready for action. {bot.user.name}#{bot.user.discriminator}, {bot.user.id}")
    print(f"the bot is in {len(bot.guilds)} guilds")
    for guilds in bot.guilds:
        print(
            f"Guild name: {guilds.name}, Guild ID: {guilds.id},"
            f" Guild owner name: {guilds.owner.name}#{guilds.owner.discriminator}, Guild owner ID: {guilds.owner.id}")
        print("---------------")



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You are missing permission(s) to run this command.")
    else:
        raise error


@bot.command(description="Creates an invite in the server it is used in.")
async def create_invite(ctx):
    invite = await ctx.channel.create_invite(max_age=300)
    server = await bot.fetch_invite(f"{invite}")
    embed1 = discord.Embed(
        title="Invite",
        description=f"Invite was Created by {ctx.author.mention}",
        colour=discord.Colour.blue()
    )
    imageurl = ctx.author.display_avatar
    embed1.set_image(url=imageurl)
    await ctx.send(embed=embed1)
    await ctx.send(server)


@bot.command(description="Literally to test if the bot is active.")
async def test(ctx):
    london = datetime.now(pytz.timezone("Europe/London"))
    if ctx.author.id == 1081507207180460032:
        await ctx.send(f"Ready to serve, Master {ctx.author.name}#{ctx.author.discriminator}.")
    else:
        await ctx.send(f"You are not Master. filing entry.")
        await ctx.send(f"User {ctx.author.name}#{ctx.author.discriminator}, at exactly {london}")
        await ctx.send("Filed entry.")


@bot.group(invoke_without_command=True, case_insenstive=True,
           description="A series of commands which are used to check member count and a list of members and their names/discriminators.")
async def member(ctx):
    if ctx.author != discord.Guild.owner:
        pass
    else:
        await ctx.send(f'Choose an option from -> {", ".join([c.name for c in ctx.command.commands])}')


@member.command()
async def count(ctx):
    members = []
    if ctx.author != discord.Guild.owner:
        pass
    else:
        for n in bot.get_all_members():
            if n.bot:
                continue
            members.append(n.name)

        await ctx.send(f"{len(members)}")


@member.command()
async def names(ctx):
    members = []
    if ctx.author != discord.Guild.owner:
        pass
    else:
        for n in bot.get_all_members():
            if n.bot:
                continue
            members.append(f"{n.display_name}#{n.discriminator}")

        await ctx.send(members)


@bot.command()
async def members(ctx):
    members = []
    if ctx.author != discord.Guild.owner:
        pass
    else:
        for n in bot.get_all_members():
            if n.bot:
                continue
            else:
                members.append(f"{n.name}#{n.discriminator}")
        await ctx.send(f"{len(members)}")


@bot.command(description="Ban a user. needed argument is Member and Reason")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason=f"{None}"):
    global embed3
    if member.top_role >= ctx.author.top_role:
        embed2 = discord.Embed(color=discord.Colour.red(),
                               title="Role", description="This user is a higher or the same role as you.")
        await ctx.send(embed=embed2)
        return
    try:
        await member.ban(reason=reason)
        embed3 = discord.Embed(
            title="Ban",
            description=f"{member.mention} has been banned by {ctx.author.mention} for {reason}.",
            colour=discord.Colour.red()
        )
        imageurl = f'{member.display_avatar}'
        embed3.set_image(url=imageurl)
        await ctx.send(embed=embed3)
    except:
        await ctx.send("Unsuccessful command")
    try:
        await ctx.member.send(embed3)
    except:
        pass


@bot.command(description="Kicks a user. needed argument is Member and Reason")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason=f"[No reason Provided]"):
    global embed5
    if member.top_role >= ctx.author.top_role:
        embed4 = discord.Embed(color=discord.Colour.purple(),
                               title="Role", description="This user is a higher or the same role as you.")
        await ctx.send(embed=embed4)
        return
    try:
        await member.kick(reason=reason)
        embed5 = discord.Embed(
            title="Kick",
            description=f"{member.mention} has been kicked by {ctx.author.mention} for {reason}.",
            colour=discord.Colour.red()
        )
        imageurl = f'{member.display_avatar}'
        embed5.set_image(url=imageurl)
        await ctx.send(embed=embed5)
    except:
        await ctx.send("Unsuccessful command")
    try:
        await ctx.member.send(embed5)
    except:
        pass


@bot.command(description="Purges a channel. needed argument is Reason.")
@commands.has_permissions(manage_channels=True)
async def purge(ctx, reason=f"{None}"):
    await ctx.channel.delete()
    new_channel = await ctx.channel.clone(reason=reason)
    await new_channel.edit(position=ctx.channel.position)
    embed6 = discord.Embed(
        title="Purge",
        description=f"Channel was purged by {ctx.author.mention}.",
        colour=discord.Colour.red()
    )
    imageurl = f'{ctx.author.display_avatar}'
    embed6.set_image(url=imageurl)
    bot.get_channel(new_channel.id)
    await new_channel.send(embed=embed6)


@bot.command(
    description="times out a user. needed argument are member, seconds, minutes, hours, days and reason. CASE SENSITIVE.")
@commands.has_permissions(mute_members=True)
async def mute(ctx, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0,
               reason: str = f"{None}"):
    global embed8
    if member.top_role >= ctx.author.top_role:
        embed7 = discord.Embed(color=discord.Colour.purple(),
                               title="Role", description="This user is a higher or the same role as you.")
        await ctx.send(embed=embed7)
        return
    duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
    try:
        await member.timeout(duration, reason=reason)
        embed8 = discord.Embed(
            title="Time-out",
            description=f"{member.mention} has been timed out by {ctx.author.mention} for {duration}, because {reason}.",
            colour=discord.Color.red()
        )
        image_url = f'{member.display_avatar}'
        embed8.set_image(url=image_url)
        await ctx.send(embed=embed8)
    except:
        await ctx.send("Unsuccessful command.")
    try:
        await ctx.member.send(embed8)
    except:
        pass


try:
    bot.run(token)
except discord.LoginFailure:
    print('Invalid Token Passed')
