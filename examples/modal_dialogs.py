# This example requires the `message_content` privileged intent for prefixed commands.

import discordtool
from discordtool.ext import commands

intents = discordtool.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"), debug_guilds=[...], intents=intents
)


class MyModal(discordtool.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            discordtool.ui.InputText(
                label="Short Input",
                placeholder="Placeholder Test",
            ),
            discordtool.ui.InputText(
                label="Longer Input",
                value="Longer Value\nSuper Long Value",
                style=discordtool.InputTextStyle.long,
            ),
            *args,
            **kwargs,
        )

    async def callback(self, interaction: discordtool.Interaction):
        embed = discordtool.Embed(
            title="Your Modal Results",
            fields=[
                discordtool.EmbedField(
                    name="First Input", value=self.children[0].value, inline=False
                ),
                discordtool.EmbedField(
                    name="Second Input", value=self.children[1].value, inline=False
                ),
            ],
            color=discordtool.Color.random(),
        )
        await interaction.response.send_message(embeds=[embed])


@bot.slash_command(name="modaltest")
async def modal_slash(ctx: discordtool.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = MyModal(title="Slash Command Modal")
    await ctx.send_modal(modal)


@bot.message_command(name="messagemodal")
async def modal_message(ctx: discordtool.ApplicationContext, message: discordtool.Message):
    """Shows an example of a modal dialog being invoked from a message command."""
    modal = MyModal(title="Message Command Modal")
    modal.title = f"Modal for Message ID: {message.id}"
    await ctx.send_modal(modal)


@bot.user_command(name="usermodal")
async def modal_user(ctx: discordtool.ApplicationContext, member: discordtool.Member):
    """Shows an example of a modal dialog being invoked from a user command."""
    modal = MyModal(title="User Command Modal")
    modal.title = f"Modal for User: {member.display_name}"
    await ctx.send_modal(modal)


@bot.command()
async def modaltest(ctx: commands.Context):
    """Shows an example of modals being invoked from an interaction component (e.g. a button or select menu)"""

    class MyView(discordtool.ui.View):
        @discordtool.ui.button(label="Modal Test", style=discordtool.ButtonStyle.primary)
        async def button_callback(
            self, button: discordtool.ui.Button, interaction: discordtool.Interaction
        ):
            modal = MyModal(title="Modal Triggered from Button")
            await interaction.response.send_modal(modal)

        @discordtool.ui.select(
            placeholder="Pick Your Modal",
            min_values=1,
            max_values=1,
            options=[
                discordtool.SelectOption(
                    label="First Modal", description="Shows the first modal"
                ),
                discordtool.SelectOption(
                    label="Second Modal", description="Shows the second modal"
                ),
            ],
        )
        async def select_callback(
            self, select: discordtool.ui.Select, interaction: discordtool.Interaction
        ):
            modal = MyModal(title="Temporary Title")
            modal.title = select.values[0]
            await interaction.response.send_modal(modal)

    view = MyView()
    await ctx.send("Click Button, Receive Modal", view=view)


bot.run("TOKEN")
