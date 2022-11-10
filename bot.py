import discord, traceback, re
from discord.colour import Color
intents = discord.Intents.all()
from discord.ext import commands
token = "Nzg0MTg4NzkwNjc4ODgwMzI2.X8lquQ.KE81OC4cNtuTkQ7kpiBztpKFX-g"
bot = commands.Bot(command_prefix = commands.when_mentioned_or("*"), intents=intents)
n = "\n"

channel = None
guild = None

@bot.event
async def on_ready():
    await bot.load_extension("jishaku")
    await bot.load_extension("pm2")
    await bot.tree.sync()
    print("ready")
    global guild, channel
    channel = bot.get_channel(500785463624335392)
    guild = channel.guild

@bot.event
async def on_member_join(member):
    try:
        await member.edit(nick=await get_next())
        await channel.send(
            embed = discord.Embed(
                title = f"Welcome, {member.display_name}!",
                color = discord.Color.green()
            )
        )
    except Exception:
        await channel.send(
            embed = discord.Embed(
                description = "Unfortunately, I could not change the nick name of this user...",
                color = discord.Color.red()
            )
        )
        await guild.get_member(511655498676699136).send(f"Error! ```{traceback.format_exc()}```")

async def get_next():
    x = [m.nick for m in guild.members if not m.bot and re.match(r'^Vsauce([1-9]?[0-9]{2,})$',m.display_name)]
    x.sort()
    o = ""
    for y in range(1, len(x)+1):
        if f'Vsauce{str(y).zfill(2)}' not in x:
            o = f"Vsauce{str(y).zfill(2)}"
            break
        o = f"Vsauce{str(y + 1).zfill(2)}"
    return o

@bot.hybrid_command()
async def ping(ctx):
    """Shows the bot's latency."""
    await ctx.interaction.response.defer()
    await ctx.reply(embed = discord.Embed(title = "Pong!", description = f"`{round(bot.latency * 1000)} ms`", color = discord.Color.green()))

@bot.hybrid_command(name = "next", aliases = ['nextvsauce'])
async def nextvsauce(ctx):
    """Shows the next member's name."""
    await ctx.interaction.response.defer()
    try:
        await ctx.reply(embed = discord.Embed(title = "The next Vsauce", description = f"The next Vsauce will be {await get_next()}.", color = discord.Color.blurple()))
    except Exception as e:
        await ctx.reply(embed = discord.Embed(title = "Error", description = f"I have encountered an error.```{e}```", color = discord.Color.red()))

@bot.hybrid_command(name = "list")
async def listmembers(ctx):
    '''Lists members in the server in order.'''
    await ctx.interaction.response.defer()
    try:
        x = [f"{m.nick} (`{m}`)" for m in bot.guilds[0].members if not m.bot]
        x.sort()
        await ctx.reply(embed = discord.Embed(title = "List of members", description = n.join(x) + n + f"Number of members: {len(x)}", color = discord.Color.greyple()))
    except Exception as e:
        await ctx.reply(embed = discord.Embed(title = "Error", description = f"I have encountered an error.```{e}```", color = discord.Color.red()))

@bot.hybrid_command(name = "fix")
@commands.has_guild_permissions(administrator=True)
async def fixmembers(ctx):
    for member in ctx.guild.members:
        if not re.match(r'^Vsauce([1-9]?[0-9]{2,})$',member.display_name) and not member.bot:
            await member.edit(nick=await get_next())
            await ctx.send(f"Fixed {member.display_name}")

bot.run(token)
