'''
pip install discord
pip install roblox
pip install ro_py

make sure pip is installed.

'''

from discord.ext import commands
from roblox import Client
import discord
from ro_py.thumbnails import ThumbnailSize, ThumbnailType

prefix = "." # change it to whatever.
token = "" # get this from https://discord.com/developers/applications
cookie = "" # get the roblosecurity cookie
groupid = id # dont put it as string or ur gonna fuck it up 
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
rbx = Client()
rbx = Client(cookie)

@bot.command()
@commands.has_permissions(manage_guilds=True)
async def acceptjoin(ctx, username):
  try:
    user = await rbx.get_user_by_username(username)
    group = await rbx.get_group(groupid)
    await group.accept_join(user=user)
  except:
    await ctx.send(f"Couldnt whitelist {username}.")

@bot.command()
async def whois(ctx, username):
    user = await rbx.get_user_by_username(username)
    embed = discord.Embed(title=f"Info for {user.name}")
    embed.add_field(
        name="Username",
        value="`" + user.name + "`"
    )
    embed.add_field(
        name="Display Name",
        value="`" + user.display_name + "`"
    )
    embed.add_field(
        name="User ID",
        value="`" + str(user.id) + "`"
    )
    embed.add_field(
        name="Description",
        value="```" + (user.description) + "```"
    )
    avatar_image = await user.thumbnails.get_avatar_image(
      shot_type=ThumbnailType.avatar_headshot,  # headshot
      size=ThumbnailSize.size_420x420,  # high resolution thumbnail
      is_circular=False  # square thumbnail
    )
    embed.set_thumbnail(
    url=avatar_image
    )
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def shout(ctx, *, shout_text):
  try:
    group = await rbx.get_group(groupid) 
    await group.shout(shout_text)
    await ctx.send(f"Sent shout {shout_text}.")
  except:
    await ctx.send(f"Error")


@bot.command()
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def setrank(ctx, username, rank: int):
  try:
    if 255 >= rank >= 1:  # Make sure rank is in allowed range
        group = await rbx.get_group(groupid)
        member = await group.get_member_by_username(username)
        await member.setrole(rank)  # Sets the rank
        await ctx.send("Promoted user.")
    else:
        await ctx.send("Rank must be at least 1 and at most 255.")
  except:
    await ctx.send("Error")

@bot.command()
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def kick(ctx, username):
  try:
    group = await rbx.get_group(groupid)  # Group ID here
    member = await group.get_member_by_username(username)
    await group.kick(member)
    await ctx.send("Kicked user.")
  except:
    await ctx.send('Error')

bot.run(token)
