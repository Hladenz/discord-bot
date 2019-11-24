import discord
from discord.ext import commands
import os,sys,random
from discord.ext.commands import has_permissions, MissingPermissions,MissingRequiredArgument,ArgumentParsingError

bot = commands.Bot(command_prefix='//', description="test")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Your Boring", type=3))
    print("Im awake")
    for Cat in bot.get_all_channels():
            if type(Cat) == discord.CategoryChannel:
                for channel in Cat.text_channels:
                    if channel.permissions_for(channel.guild.me).send_messages:
                        await bot.get_channel(channel.id).send("Im awake")
                        break
            else:
                if channel.permissions_for(channel.guild.me).send_messages:
                    await bot.get_channel(channel.id).send("Im awake")

@bot.command("Restart")
@has_permissions(administrator=True)
async def Restart(ctx):

    embed = discord.Embed(title="Restarting....", description=f"Restarting Ordered by {ctx.message.author}")
    await ctx.send(embed=embed)
    os.execv(sys.executable, ['python'] + sys.argv)

@Restart.error
async def restart_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = f"Sorry {ctx.message.author}, you do not have permissions to do that!"
        await ctx.send(text)

@bot.command("Purge")
@has_permissions(administrator=True)
async def Purge(ctx,Limit: int):

    if Limit == 0:
        Deleted = await ctx.message.channel.purge(bulk=True)
    else:
        Deleted = await ctx.message.channel.purge(limit=Limit,bulk=True)

    Messages = {}
    for message in Deleted:

        if message.author in Messages:
           Messages[message.author] +=1
        else:
            Messages[message.author] = 1

    Messages[message.author] -=1
    if Messages[message.author] <= 0:
        del Messages[message.author]

    embed = discord.Embed(title="Purge", description=f"messages Deleted:{len(Deleted)-1}")
    for Message in Messages:
        embed.add_field(name=f"{Message}:{Messages[Message]}", value="\n\u200b", inline=False)

    await ctx.send(embed=embed)

@Purge.error
async def Purge_error(ctx,error):
    if isinstance(error, MissingPermissions):
        text = f"Sorry {ctx.message.author}, you do not have permissions to do that!"
        await ctx.send(text)

@bot.command("Random")
async def Random(ctx,Max: int,Mini: int):
    await ctx.send(f"Your Number is {random.randrange(Mini,Max)}")

@Random.error
async def Random_error(ctx, error):
    print(error)
    if isinstance(error, MissingRequiredArgument) or isinstance(error,ArgumentParsingError):
        await ctx.send("Please Put a Max and Mini Value")

bot.run(os.getenv("bot_token"))



