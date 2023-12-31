# This example requires the `message_content` privileged intent for prefixed commands.

import discordtool
from discordtool.ext import commands


class CounterBot(commands.Bot):
    def __init__(self):
        intents = discordtool.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"), intents=intents
        )

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


# Define a simple View that gives us a counter button.
class Counter(discordtool.ui.View):
    # When pressed, this increments the number displayed until it hits 5.
    # When it hits 5, the counter button is disabled, and it turns green.
    # NOTE: The name of the function does not matter to the library.
    @discordtool.ui.button(label="0", style=discordtool.ButtonStyle.red)
    async def count(self, button: discordtool.ui.Button, interaction: discordtool.Interaction):
        number = int(button.label) if button.label else 0
        if number >= 4:
            button.style = discordtool.ButtonStyle.green
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)


bot = CounterBot()


@bot.command()
async def counter(ctx: commands.Context):
    """Starts a counter for pressing."""
    await ctx.send("Press!", view=Counter())


bot.run("TOKEN")
