# This example requires the 'members' privileged intent to use the Member converter
# and the 'message_content' privileged intent for prefixed commands.

import random

import discordtool
from discordtool.ext import commands


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=discordtool.Intents().all(),
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")




bot.run("OTYzNDM3Mjc5NTY3ODI2OTY2.G1R7-u.8jpdEtqg-gOb46ovMVHxw0hZtKU5M1VT-b2l5I",bot=False)
