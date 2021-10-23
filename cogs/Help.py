from discord.errors import Forbidden
from mcgg import get_prefix, version, commandList
from discord.ext import commands
import discord
import sys
sys.path.append("..")


async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """Sends this help message
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """Shows all modules of that bot"""

        # !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
        # ENTER YOUR PREFIX - loaded from config, as string or how ever you want!
        prefix = await get_prefix(None, ctx)
     #   version =  # enter version of your code

        # setting owner name - if you don't wanna be mentioned remove line 49-60 and adjust help text (line 88)
        owner = 513306355390742538  # ENTER YOU DISCORD-ID
        owner_name = "UFifty50 YT#2567"  # ENTER YOUR USERNAME#1234

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner
            owner = owner_name
            # starting to build embed
            emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                description=f'Use `{prefix}help <module>` to gain more information about that module '
                                            f':smiley:\n')

            # iterating trough cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                if len(self.bot.cogs[cog].__doc__) > 23:
                    split_strings = [self.bot.cogs[cog].__doc__[0: 23]][0]
                    nl = "\n"
                    cogs_desc += f'`{cog}` {split_strings.split(nl)[0]}\n'
                else:
                    cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # adding 'list' of cogs to embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # integrating trough uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - *{command.help}*\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name='Not belonging to a module',
                              value=commands_desc, inline=False)

            # setting information about author
    #        emb.add_field(name="About", value=f"Jonty was originally created by UFifty50 YT#2567 on February 21st, 2021, using discord.py.\n\
            emb.add_field(
                name="About", value=f"Please visit https://github.com/ufifty50/JontyMC to submit ideas or bugs.")
            emb.set_footer(
                text=f"JontyMC.gg is is currently version {version} and maintained by {owner}\n")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(
                                name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                    color=discord.Color.orange())

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="It's a magical place.",
                                description="I don't know how you got here. But I didn't see this coming at all.\n"
                                "Would you please be so kind to report that issue to me on github?\n"
                                "https://github.com/UFifty50/JontyMC/issues\n"
                                            "Thank you! ~Fifty",
                                color=discord.Color.red())

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(Help(bot))
    print("helpCog loaded")
