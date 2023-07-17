# This example requires the 'members' privileged intent to use the Member converter.

import discordtool
from discordtool.commands import SlashCommandGroup
from discordtool.ext import commands

intents = discordtool.Intents.default()
intents.members = True

bot = discordtool.Bot(debug_guilds=[...], intents=intents, owner_id=...)  # Main file


class Example(commands.Cog):
    def __init__(self, bot_: discordtool.Bot):
        self.bot = bot_

    greetings = SlashCommandGroup("greetings", "Various greeting from cogs!")

    international_greetings = greetings.create_subgroup(
        "international", "International greetings"
    )

    secret_greetings = SlashCommandGroup(
        "secret_greetings",
        "Secret greetings",
        checks=[
            commands.is_owner().predicate
        ],  # Ensures the owner_id user can access this group, and no one else
    )

    @greetings.command()
    async def hello(self, ctx: discordtool.ApplicationContext):
        await ctx.respond("Hello, this is a slash subcommand from a cog!")

    @international_greetings.command()
    async def aloha(self, ctx: discordtool.ApplicationContext):
        await ctx.respond("Aloha, a Hawaiian greeting")

    @secret_greetings.command()
    async def secret_handshake(
        self, ctx: discordtool.ApplicationContext, member: discordtool.Member
    ):
        await ctx.respond(f"{member.mention} secret handshakes you")

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discordtool.ApplicationContext, error: discordtool.DiscordException
    ):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("You can't use that command!")
        else:
            raise error  # Raise other errors so they aren't ignored


bot.add_cog(Example(bot))  # Put in a setup function for cog files
bot.run("TOKEN")  # Main file
