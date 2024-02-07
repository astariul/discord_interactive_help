"""Example of a Discord bot with interactive help."""

import os

import discord

from discord_interactive import Help, Page


# Start client
global client
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)

################################################################################
#               Interactive help definitions start here                        #
################################################################################

# Create the pages of the tree
root = Page(
    "Welcome to the Help interface ! This is interactive, you can simply react to interact with the help :)\n\n"
    "What do you want to know more about ?\n"
)
page_help = Page("Help pages are simply a tree of pages and the system naviguate through this tree.\n")
# Page are now Embed by default, you can add various fields like when you create an Embed
page_cmd = Page(
    "It' implemented ! Try it with /guild", title="Guild functionality", color=0xE67E22
)  # You can add a title, a color, etc... (See Discord Embed documentation for more)
page_react = Page(
    "The system wait the user to react (there is no timeout yet, maybe a future feature ?). \n\n\n\n\nThen based on "
    "that reaction, the system display the next help page."
)
page_everyone = Page(
    "Everyone can use it at the same time ! It is based on asyncio library. Since this is personal help, help message "
    "is sent to private channel with the user."
)
# You can also display pages as basic messages if you prefer, with `embed=False`
page_slow = Page(
    "I know, its quite slow... This is because every reaction is added one by one (there is currently no way to add "
    "several reaction at the same time through discord API). If you find a better way to do it, please tell me !",
    embed=False,
)

# Link pages together

# Use default emoji
page_help.link(page_react, description="What about reaction ?")
page_help.link(page_everyone, description="Can several people use it ?")
page_help.link(page_slow, description="Why the message displayed is slow to display all reactions ?")

# Use custom emoji
root.link(page_help, reaction="🕶", description="How do you display pages ?")
root.link(page_cmd, reaction="👌", description="How can I put commands into the help system ?")

# Set the root as root
root.root_of([page_react, page_everyone, page_slow, page_help, page_cmd])

global h
h = Help(client, root)

################################################################################
#            From here, it's for advanced use : interactive commands           #
################################################################################


async def display_guild_list(link, member, prev_input):
    """Callback #1 for the interactive guild functionality : displaying
    dynamic guild list.
    """
    # Call the database and get the list of guilds
    guilds = ["Iron Guild", "Mega Guild", "Best people", "No idea", "Wanted"]
    # Fake example for sure :)

    # We have access to the link, so we can modify its content (dynamically)
    link.page().msg = "List of existing guilds :\n\n" + "\n".join(guilds) + "\n"


async def congrats(link, member, prev_input):
    """Callback #2 for the interactive guild functionality : checking if the
    requested name is already taken, and display the right message.
    """
    # Write to request to database
    guild_name = prev_input[-2].content  # Always use minus to access messages
    leader_name = prev_input[-1].content
    # Database call : write_new_guild(guild_name, leader_name)

    # (for the example sake, let's say only 'blabla' exist)
    # In real-world, you should call your database to know if the guild exists !
    guild_exist = guild_name == "blabla"
    if guild_exist:
        link.path = 1  # Change the path to the second page, the page of fail !
    else:
        link.page().msg = "Congrats ! You created the guild {}, leaded by {} !\n".format(guild_name, leader_name)


# Now create the page tree for the guild functionnality
root2 = Page(
    "Welcome to this (fake) guild functionnality.\n\nHere we will see how you can make your bot even more interactive,"
    " by making each command completely interactive.\n\n"
)
page_guild = Page("What would you like to do ?\n")
page_guild_display = Page(
    ""
)  # Here we don't display any static content. Content will be displayed by callback, dynamically
page_guild_register = Page("To register your guild, first type the name of your guild")
page_guild_register2 = Page("Good ! Now type the name of the leader of the guild")
page_guild_end1 = Page("")
page_guild_end2 = Page("Sorry, this guild already exist...")

# Link the pages

# Here, after registering a guild might lead to 2 income : either the register is successful, or it's not
# Depending on the callback, the choice of page to display will be different
page_guild_register2.link(
    [page_guild_end1, page_guild_end2], is_parent=False, callbacks=congrats, user_input=True
)  # We set user_input to true, so this is a Message Link. And we don't want to have a parent link
page_guild_register.link(page_guild_register2, is_parent=False, user_input=True)
page_guild.link(
    page_guild_display, reaction="👁", description="Get the list of existing guilds", callbacks=display_guild_list
)
page_guild.link(page_guild_register, reaction="➕", description="Register your own guild")
root2.link(page_guild, reaction="😀", description="Let's get started !")

# For the pages without parents, we create new parent
page_guild.parent_of([page_guild_register, page_guild_register2, page_guild_end1, page_guild_end2])

# And root it
root2.root_of(
    [page_guild, page_guild_display, page_guild_register, page_guild_register2, page_guild_end1, page_guild_end2]
)

global h2
h2 = Help(client, root2)


@client.event
async def on_message(message):
    """Write your bot here ! For this example, the bot does nothing but
    displaying the interactive help (either the basic example with `/help` or
    the advanced example with `/guild`).
    """
    if message.author != client.user:  # Do not answer to myself
        if message.content.startswith("/help"):
            await h.display(message.author)
        elif message.content.startswith("/guild"):
            await h2.display(message.author)


################################################################################
#                                 End here                                     #
################################################################################


def main():
    """Main. Start the Discord Client."""
    token = os.environ.get("DISCORD_BOT_SECRET")

    client.run(token)


if __name__ == "__main__":
    print("Starting main...")
    main()
