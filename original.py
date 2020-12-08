import discord
token = "NzI2NDQ0MTc2MDkwMDcxMDcy.XvdX3A.gHxXu-DxBnihYhOvKFXytVAm6qY"
bot = discord.Client()

@bot.event
async def on_ready():
    print("ready")

@bot.event
async def on_member_join(member):
        x = [member.display_name for member in bot.guilds[0].members]
        x.sort()
        o = ""
        for y in range(10, len(x)-3):
                if f'Vsauce{y}' not in x:
                        o = f"Vsauce{y}"
                        break
                o = f"Vsauce{y}"
        await member.edit(nick=o)

bot.run(token)