import os
from example.keep_alive import keep_alive
import discord

import help
import page

# Start client
global client
client = discord.Client()

# Create the page tree and the Help
root = page.Page('Welcome to the Help interface ! This is interactive, you can simply react to interact with the help :)\n\nWhat do you want to know more about ?\n\n')
page_help = page.Page('Help pages are simply a tree of pages and the system naviguate throught it.\n\n', parent=root)
page_cmd = page.Page('This is not implemented yet, but it will come soon !', parent=root)
page_react = page.Page('The system wait the user to react (there is no timeout yet, we will see it later). \n\n\n\n\nThen based on that reaction, the system display the next help page.', root=root, parent=page_help)
page_everyone = page.Page('Everyone can use it at the same time ! But not together. This is personal help, thats why the help message is sent to private channel with the user.', root=root, parent=page_help)
page_slow = page.Page('I know, its quite slow... This is because every reaction is added one by one (there is currently no way to add several reaction at the same time through discord API). If you find a better way to do it, please tell me !', root=root, parent=page_help)

# Link pages together
page_help.add_link(page_react, 'What about reaction ?') # Use default emoji
page_help.add_link(page_everyone, 'Can several people use it ?')  # Use default emoji
page_help.add_link(page_slow, 'Why the message displayed is slow ?')      # Use default emoji
root.add_link(page_help, 'How do you display pages ?', '2⃣')  # Use custom emoji
root.add_link(page_cmd, 'How can I put commands into the help system ?', '1⃣')  # Use custom emoji

global h
h = help.Help(client, root)

# Callbacks for guild functionnality
async def display_guild_list(page, member):
    # Call the database and get the list of guilds
    guilds = ['Iron Guild', 'Mega Guild', 'Best people', 'No idea', 'Wanted']
    # Fake example for sure :)

    # We have access to the page, so we can modify its content (dynamically)
    page.msg = "List of existing guilds :\n\n" + '\n'.join(guilds) + '\n'

class RegisterGuild():
    # Here we create a class in order to keep attribute accessible from any of the 3 callbacks we declare
    # Since there is only 1 object for all users, we need to keep different states for different users.
    # We do that with a simple dict, with the Discord ID being the key.
    def __init__(self):
        self.user_dict = {}

    async def register_name(self, page, member, message):
        self.user_dict[member.id] = {
            'name': message.content,
            'leader': None
        }

    async def register_leader(self, page, member, message):
        self.user_dict[member.id]['leader'] = message.content

    async def congrats(self, page, member):
        page.msg = "Congrats ! You created the guild {}, leaded by {} !\n".format(self.user_dict[member.id]['name'], self.user_dict[member.id]['leader'])

        # After finishing the command, don't forget to delete the entry, or entries will stack as user registers guild
        self.user_dict.pop(member.id, None)

# Now create the page tree for the guild functionnality
root2 = page.Page('Welcome to this (fake) guild functionnality.\n\nHere we will see how you can make your bot even more interactive, by making each command completely interactive.\n\n')
page_guild = page.Page('What would you like to do ?\n', parent=root2)
page_guild_display = page.Page('', parent=page_guild, root=root2, callbacks=[display_guild_list]) # Here we don't display any static content. Content will be displayed by callback, dynamically

reg = RegisterGuild()
page_guild_register = page.Page('To register your guild, first type the name of your guild', parent=page_guild, root=root2, user_callbacks=[reg.register_name])
page_guild_register2 = page.Page('Good ! Now type the name of the leader of the guild', root=root2, user_callbacks=[reg.register_leader])
page_guild_end = page.Page('', root=root2, callbacks=[reg.congrats])

page_guild_register2.add_link(page_guild_end, after_msg=True)
page_guild_register.add_link(page_guild_register2, after_msg=True)
page_guild.add_link(page_guild_display, 'Get the list of existing guilds', '👁‍🗨')
page_guild.add_link(page_guild_register, 'Register your own guild', '➕')
root2.add_link(page_guild, 'Let\'s get started !', '😀')

global h2
h2 = help.Help(client, root2)

@client.event
async def on_message(message):
    if message.author != client.user:       # Do not answer to myself
        if message.content.startswith('/help'):
            await h.display(message.author)
        elif message.content.startswith('/guild'):
            await h2.display(message.author)

def main():
    """ Main

    Main of the Jiva bot. Start the webserver (in order to keep the bot alive), and 
    start the Discord Client.
    """
    keep_alive()
    token = os.environ.get("DISCORD_BOT_SECRET")

    client.run(token)

if __name__ == "__main__":
    print('Starting main...')
    main()