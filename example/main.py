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


@client.event
async def on_message(message):
    if message.author != client.user:       # Do not answer to myself
        if message.content.startswith('/help'):
            await h.display(message.author)

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