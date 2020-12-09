import discord
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
        await member.edit(nick=await get_next())

async def get_next():
        x = [m.nick for m in bot.guilds[0].members if not m.bot]
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

@bot.command(name = "next", aliases = ['nextmember'])
async def nextvsauce(ctx):
        """Shows the next member's name."""
        await ctx.send(embed = discord.Embed(title = "The next Vsauce", description = f"The next Vsauce will be {await get_next()}.", color = discord.Color.blurple()))

@bot.command(name = "list")
async def listmembers(ctx):
        try:
                x = [m.nick for m in bot.guild[0].members if not m.bot]
                x.sort()
                await ctx.send(embed = discord.Embed(title = "List of members", description = ", ".join(x) + n + f"Number of members: {len(x)}", color = discord.Color.greyple()))
        except Exception as e:
                await ctx.send(embed = discord.Embed(title = "Error", description = f"I have encountered an error.```{e}```", color = discord.Color.red()))

bot.load_extension("jishaku")
bot.run(token)
