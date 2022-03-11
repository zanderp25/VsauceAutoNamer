import asyncio
import discord, traceback, re
from discord.colour import Color
intents = discord.Intents(messages=True, members=True, guilds=True, reactions=True, message_content=True)
from discord.ext import commands
token = "Nzg0MTg4NzkwNjc4ODgwMzI2.X8lquQ.KE81OC4cNtuTkQ7kpiBztpKFX-g"
bot = commands.Bot(command_prefix = commands.when_mentioned_or("*"), intents=intents)
n = "\n"

channel = None
guild = None

@bot.event
async def on_ready():
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
                description = "Unfortunately, I could not change the nickname of this user...",
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
        x = [f"{m.nick} (`{m}`)" for m in bot.guilds[0].members if not m.bot]
        x.sort()
        msg:discord.Message = await ctx.send(
            embed = discord.Embed(
                title = "List of members", 
                description = n.join(x[:20]),
                color = discord.Color.greyple(),
            ).set_footer(
                text=f"Number of members: {len(x)}", 
            )
        )
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")
        index = 0
        while True:
            r = await bot.wait_for('reaction_add', check=lambda reaction, user: user.id == ctx.author.id and reaction.message.id == msg.id, timeout=60.0)
            if r[0].emoji == "◀️":
                index -= 20
            elif r[0].emoji == "▶️":
                index += 20
            else:
                continue
            index = max(0, min(index, len(x) - 20))
            await msg.edit(embed = discord.Embed(
                title = "List of members",
                description = n.join(x[index:index+20])
            ).set_footer(
                text=f"Number of members: {len(x)}",
            ))
            await msg.remove_reaction(r[0].emoji, ctx.author)
    except asyncio.TimeoutError:
        await msg.clear_reactions()
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
