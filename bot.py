import discord, traceback, re
from discord.colour import Color
intents = discord.Intents(messages=True, members=True, guilds=True)
from discord.ext import commands
token = "Nzg0MTg4NzkwNjc4ODgwMzI2.X8lquQ.KE81OC4cNtuTkQ7kpiBztpKFX-g"
bot = commands.Bot(command_prefix = commands.when_mentioned_or("*"), intents=intents)
n = "\n"

@bot.event
async def on_ready():
    print("ready")

@bot.event
async def on_member_join(member):
    try:
        await member.edit(nick=await get_next())
        await bot.guilds[0].get_channel(500785463624335392).send(
            embed = discord.Embed(
                title = f"Welcome, {member.display_name}!",
                color = discord.Color.green()
            )
        )
    except Exception:
        await bot.guilds[0].get_channel(500785463624335392).send(
            embed = discord.Embed(
                description = "Unfortunately, I could not change the nick name of this user...",
                color = discord.Color.red()
            )
        )
        await bot.guilds[0].get_member(511655498676699136).send(f"Error! ```{traceback.format_exc()}```")

async def get_next():
    x = [m.nick for m in bot.guilds[0].members if not m.bot and re.match(r'^Vsauce([1-9]?[0-9]{2,})$',m.display_name)]
    x.sort()
    o = ""
    for y in range(10, len(x)+1):
        if f'Vsauce{y}' not in x:
            o = f"Vsauce{y}"
            break
        o = f"Vsauce{y + 1}"
    return o

@bot.command()
async def ping(ctx):
    """Shows the bot's latency."""
    await ctx.send(embed = discord.Embed(title = "Pong!", description = f"`{round(bot.latency * 1000)} ms`", color = discord.Color.green()))

@bot.command(name = "next", aliases = ['nextvsauce'])
async def nextvsauce(ctx):
    """Shows the next member's name."""
    try:
        await ctx.send(embed = discord.Embed(title = "The next Vsauce", description = f"The next Vsauce will be {await get_next()}.", color = discord.Color.blurple()))
    except Exception as e:
        await ctx.send(embed = discord.Embed(title = "Error", description = f"I have encountered an error.```{e}```", color = discord.Color.red()))

@bot.command(name = "list")
async def listmembers(ctx):
    '''Lists members in the server in order.'''
    try:
        x = [m.nick for m in bot.guilds[0].members if not m.bot]
        x.sort()
        await ctx.send(embed = discord.Embed(title = "List of members", description = ", ".join(x) + n + f"Number of members: {len(x)}", color = discord.Color.greyple()))
    except Exception as e:
        await ctx.send(embed = discord.Embed(title = "Error", description = f"I have encountered an error.```{e}```", color = discord.Color.red()))

@bot.command(name = "fix")
@commands.has_guild_permissions(administrator=True)
async def fixmembers(ctx):
    for member in ctx.guild.members:
        if not re.match(r'^Vsauce([1-9]?[0-9]{2,})$',member.display_name) and not member.bot:
            await member.edit(nick=await get_next())


bot.load_extension("jishaku")
bot.run(token)
