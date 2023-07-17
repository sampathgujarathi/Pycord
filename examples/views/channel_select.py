import discordtool

# Channel selects (dropdowns) are a new type of select menu/dropdown Discord has added so users can select channels from a dropdown.


# Defines a simple View that allows the user to use the Select menu.
# In this view, we define the channel_select with `discord.ui.channel_select`
# Using the decorator automatically sets `select_type` to `discord.ComponentType.channel_select`.
class DropdownView(discordtool.ui.View):
    @discordtool.ui.channel_select(
        placeholder="Select channels...", min_values=1, max_values=3
    )  # Users can select a maximum of 3 channels in the dropdown
    async def channel_select_dropdown(
        self, select: discordtool.ui.Select, interaction: discordtool.Interaction
    ) -> None:
        await interaction.response.send_message(
            f"You selected the following channels:"
            + f", ".join(f"{channel.mention}" for channel in select.values)
        )


bot: discordtool.Bot = discordtool.Bot(debug_guilds=[...])


@bot.slash_command()
async def channel_select(ctx: discordtool.ApplicationContext) -> None:
    """Sends a message with our dropdown that contains a channel select."""

    # Create the view containing our dropdown
    view = DropdownView()

    # Sending a message containing our View
    await ctx.respond("Select channels:", view=view)


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


bot.run("TOKEN")
