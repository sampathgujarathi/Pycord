from typing import Union

import discordtool
from discordtool import option

bot = discordtool.Bot(debug_guilds=[...])


# If you use commands.Bot, @bot.slash_command should be used for
# slash commands. You can use @bot.slash_command with discord.Bot as well.


@bot.slash_command()
@option("name", description="Enter your name")
@option("gender", description="Choose your gender", choices=["Male", "Female", "Other"])
@option(
    "age",
    description="Enter your age",
    min_value=1,
    max_value=99,
    default=18,
    # Passing the default value makes an argument optional.
    # You also can create optional arguments using:
    # age: Option(int, "Enter your age") = 18
)
async def hello(
    ctx: discordtool.ApplicationContext,
    name: str,
    gender: str,
    age: int,
):
    await ctx.respond(
        f"Hello {name}! Your gender is {gender} and you are {age} years old."
    )


@bot.slash_command(name="channel")
@option(
    "channel",
    Union[discordtool.TextChannel, discordtool.VoiceChannel],
    # You can specify allowed channel types by passing a union of them like this.
    description="Select a channel",
)
async def select_channel(
    ctx: discordtool.ApplicationContext,
    channel: Union[discordtool.TextChannel, discordtool.VoiceChannel],
):
    await ctx.respond(f"Hi! You selected {channel.mention} channel.")


@bot.slash_command(name="attach_file")
@option(
    "attachment",
    discordtool.Attachment,
    description="A file to attach to the message",
    required=False,  # The default value will be None if the user doesn't provide a file.
)
async def say(
    ctx: discordtool.ApplicationContext,
    attachment: discordtool.Attachment,
):
    """This demonstrates how to attach a file with a slash command."""
    if attachment:
        file = await attachment.to_file()
        await ctx.respond("Here's your file!", file=file)
    else:
        await ctx.respond("You didn't give me a file to reply with! :sob:")


bot.run("TOKEN")
