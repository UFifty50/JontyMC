#!/bin/python3


import json
import socket
import base64
import discord
import discord.colour
from typing import Union
from mcstatus import MinecraftServer
from discord_slash import SlashCommand
from discord.ext import commands, tasks
from discord.errors import DiscordException
from discord_slash.utils.manage_commands import create_option

token = open(".env", "r").read()

purple = 0xff81ff
darkblue = 0x0000ff
lightblue = 0x0096ff
red = 0xff0000
green = 0x00c800

version = "1.1.0"
commandList = {}
prejson = "prefixes.json"


async def get_prefix(client, message):
    with open(prejson, 'r') as f:
        prefixes = json.load(f)
        prefix = prefixes[str(message.guild.id)]
        return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, help_command=None,
                   case_insensitive=True, intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    print('Logged in as', bot.user)
    print('ID:', bot.user.id)
    await bot.change_presence(activity=discord.Game(f".help for help"))


@bot.event
async def on_guild_join(guild):
    with open(prejson, 'r') as f:
        prefixes = json.load(f)
        prefixes[str(guild.id)] = '.'
        prefix = prefixes[str(guild.id)]
    with open(prejson, 'w') as f:
        json.dump(prefixes, f, indent=4)

    self = await guild.fetch_member(bot.user.id)
    await self.edit(nick=f"[{prefix}] JontyMC.gg")


@slash.slash(name="setprefix",
             description="Changes the bots prefix.",
             options=[
                 create_option(
                     name="prefix",
                     description="What you want the bot to respond to",
                     option_type=3,
                     required=True
                 )
             ])
@bot.command(aliases=['changeprefix', 'prefixset'], help="Changes the command prefix.", pass_context=True, hidden=True)
async def setprefix(ctx, prefix):
    if ctx.author.guild_permissions.administrator or (ctx.author.id == 513306355390742538):
        with open(prejson, 'r') as f:
            prefixes = json.load(f)
            prefixes[str(ctx.guild.id)] = prefix

        with open(prejson, 'w') as f:
            json.dump(prefixes, f, indent=4)

        self = await ctx.guild.fetch_member(bot.user.id)
        await ctx.send(f'Successfully changed the prefix to: **``{prefix}``**')
        try:
            await self.edit(nick=f"[{prefix}] JontyMC.gg")
        except DiscordException:
            await ctx.send(f"I do not have the permissions to change my nick!")
    else:
        await ctx.send(f"sorry {ctx.author}, you do not have the permissions to do that!")


@slash.slash(
    name="server",
    description="Get server information from the given ip",
    options=[
        create_option(
            name="ip",
            description="The ip of the server",
            option_type=3,
            required=True
        ),
        create_option(
            name="port",
            description="The port of the server that you want to connect to",
            option_type=4,
            required=False
        )
    ]
)
@bot.command(name="server")
async def server(ctx, ip: Union[str, int] = None, port: int = None, sched=None, l=None):
    """server
    Returns detailed server info such as its version, online players and protocol.
    """
    if not ip:
        await ctx.send("You need to give an ip!")
    elif l:
        await ctx.send("This command only takes two arguments (the server ip and port).")
    elif port:
        server = MinecraftServer.lookup(f'{ip}:{port}')
        try:
            olddesc = server.status().description
        except socket.gaierror:
            await ctx.send(f'`{ip}:{port}` is not a valid server address!')
            return 0
        newdesc = list(olddesc)
        for i in newdesc:
            if i == "§":
                newdesc[newdesc.index(i)+1] = ""
                newdesc[newdesc.index(i)] = ""
        testdesc = "".join(newdesc)
        if "server is offline." in testdesc:
            desc = "This server is offline."
            col = red
            status = ":red_circle: This server is offline."
        else:
            desc = testdesc
            col = green
            status = ":green_circle: This server is online."
        b64png = "i" + server.status().favicon.lstrip("data:image/png;base64,")
        fp = open(f'favicons/{ip}.favicon.png', "wb")
        fp.write(base64.b64decode(b64png, validate=False))
        img = discord.File(
            open(f'favicons/{ip}.favicon.png', "rb"), filename=f'{ip}.favicon.png')
        # print(server.status().raw)
        em = discord.Embed(
            title=f'MC Server: {ip}', description=status, color=col)
        em.set_thumbnail(url=f'attachment://{ip}.favicon.png')
        em.add_field(name="Description",
                     value=desc, inline=False)
        em.add_field(name="Players",
                     value=f'Online: `{server.status().players.online}`\nMax: `{server.status().players.max}`', inline=True)
        em.add_field(name="Version",
                     value=f'Version: {server.status().version.name}\nProtocol: `{server.status().version.protocol}`', inline=True)
        em.set_footer(text="footer to come later")
        global message
        try:
            if not sched:
                message = await ctx.send(embed=em, file=img)
            else:
                await message.edit(embed=em)
        except NameError:
            message = await ctx.send(embed=em, file=img)
        except discord.errors.NotFound:
            await ctx.send(embed=em, file=img)
    else:
        server = MinecraftServer.lookup(ip)
        try:
            olddesc = server.status().description
        except socket.gaierror:
            await ctx.send(f'`{ip}` is not a valid server address!')
            return 0

        b64png = "i" + server.status().favicon.lstrip("data:image/png;base64,")

        olddesc = server.status().description
        newdesc = list(olddesc)
        for i in newdesc:
            if i == "§":
                newdesc[newdesc.index(i)+1] = ""
                newdesc[newdesc.index(i)] = ""
        testdesc = "".join(newdesc)
        if "server is offline." in testdesc:
            desc = "This server is offline."
            col = red
            status = ":red_circle: This server is offline."
        else:
            desc = testdesc
            col = green
            status = ":green_circle: This server is online."
        fp = open(f'favicons/{ip}.favicon.png', "wb")
        fp.write(base64.b64decode(b64png, validate=False))
        img = discord.File(
            open(f'favicons/{ip}.favicon.png', "rb"), filename=f'{ip}.favicon.png')
        # print(server.status().raw)
        em = discord.Embed(
            title=f'MC Server: {ip}', description=status, color=col)
        em.set_thumbnail(url=f'attachment://{ip}.favicon.png')
        em.add_field(name="Description",
                     value=desc, inline=False)
        em.add_field(name="Players",
                     value=f'Online: `{server.status().players.online}`\nMax: `{server.status().players.max}`', inline=True)
        em.add_field(name="Version",
                     value=f'Version: {server.status().version.name}\nProtocol: `{server.status().version.protocol}`', inline=True)
        em.set_footer(text="footer to come later")
        try:
            if not sched:
                message = await ctx.send(embed=em, file=img)
            else:
                await message.edit(embed=em)
        except NameError:
            message = await ctx.send(embed=em, file=img)
        except discord.errors.NotFound:
            await ctx.send(embed=em, file=img)


@tasks.loop(seconds=5)
async def schedule(func, a1, a2, a3=None):
    await func.invoke(a1, a2, a3, True)


@bot.command(name="mcscheduleping", aliases=["msp"])
async def msp(ctx, ip: Union[str, int], port: int = None):
    """msp
    pings the given ip and/or port every 5 seconds. (server but scheduled)
    """
    if port:
        try:
            await schedule.start(func=server, a1=ctx, a2=ip, a3=port)
        except RuntimeError:
            schedule.stop()
    else:
        try:
            await schedule.start(func=server, a1=ctx, a2=ip)
        except RuntimeError:
            schedule.stop()

bot.load_extension('cogs.Help')
bot.run(token)
