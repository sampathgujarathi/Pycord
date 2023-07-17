from urllib.parse import quote_plus

import discordtool


# Define a simple View that gives us a Google link button.
# We take in `query` as the query that the command author requests for.
class Google(discordtool.ui.View):
    def __init__(self, query: str):
        super().__init__()
        # We need to quote the query string to make a valid url. Discord will raise an error if it isn't valid.
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"

        # Link buttons cannot be made with the
        # decorator, so we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discordtool.ui.Button(label="Click Here", url=url))

        # Initializing the view and adding the button can actually be done in a one-liner at the start if preferred:
        # super().__init__(discord.ui.Button(label="Click Here", url=url))


bot = discordtool.Bot(debug_guilds=[...])


@bot.slash_command()
async def google(ctx: discordtool.ApplicationContext, query: str):
    """Returns a google link for a query."""
    await ctx.respond(f"Google Result for: `{query}`", view=Google(query))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


bot.run("TOKEN")
