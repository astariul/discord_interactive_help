<h1 align="center">Discord Interactive Help</h1>

![gif](https://user-images.githubusercontent.com/22237185/53283254-da5a3100-3786-11e9-95cd-cd4dd4859bd2.gif)

<p align="center">
A Discord python framework to display an interactive help easily.
</p>

<p align="center">
    <a href="https://github.com/astariul/discord_interactive_help/releases"><img src="https://img.shields.io/github/release/astariul/discord_interactive_help.svg" alt="GitHub release" /></a>
    <a href="https://github.com/astariul/discord_interactive_help/actions/workflows/lint.yaml"><img src="https://github.com/astariul/discord_interactive_help/actions/workflows/lint.yaml/badge.svg" alt="Lint status" /></a>
    <a href="https://astariul.github.io/discord_interactive_help"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=green&up_message=passing&url=https%3A%2F%2Fastariul.github.io%2Fdiscord_interactive_help" alt="Docs" /></a>
    <a href="https://github.com/astariul/pytere/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="licence" /></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#example">Example</a> •
  <a href="#advanced">Advanced</a>
  <a href="#running-in-docker">Running in Docker</a> •
  <a href="#notes">Notes</a>
  <br>
  <a href="https://astariul.github.io/discord_interactive_help/" target="_blank">Documentation</a>
</p>

<h2 align="center">Features</h2>

* 🔆 **Easy to naviguate** : Use reactions to naviguate through the Help manual.
* ⚙ **Customized reaction** : Use any emoji as naviguation icon.
* 🎮 **Commands support** : Go even further with interactive commands.

<h2 align="center">Usage</h2>

Install the package :

`pip install discord-interactive`

---

Import the `Page` and `Help` objects into your bot's code, and create your own help manual :

```py
from discord_interactive import Page, Help

# Define each page
root = Page('Welcome !\n')
page_1 = Page('This is page 1')
page_2 = Page('This is page 2')

# Link pages together
page_1.link(page_2, description='Click this icon to access page 2', reaction='💩')
root.link(page_1, description='Click this icon to access page 1')

# Set the root page as the root of other page (so user can come back with a specific reaction)
root.root_of([page_1, page_2])

# Create the Help object
client = discord.Client()
h = Help(client, root)

...

# And display the help !
@client.event
async def on_message(message):
    if message.author != client.user:  # Do not answer to myself
        if message.content.startswith('/help'):
            await h.display(message.author)
```

<h2 align="center">Example</h2>

You can try the interactive help in [this Discord server](https://discord.gg/cH6hUbw) !

Simply join the server, and type `/help` in the chat.

Also, take a look at the code for this interactive help ! Check out the script [`main.py`](https://github.com/astariul/discord_interactive_help/blob/main/main.py).

<h2 align="center">Advanced</h2>

If you are interested in **advanced usage** such as **interactive commands**, take a look at the [full documentation](https://astariul.github.io/discord_interactive_help/4.0/usage/#advanced).

Example of advanced usage :

![gif](https://user-images.githubusercontent.com/22237185/53492662-c4c56e00-3adc-11e9-8be8-1b10d9f85e8a.gif)

---

If you can't find what you are looking for, or need help about this library, you can open a [discussion thread](https://github.com/astariul/discord_interactive_help/discussions) or an [issue](https://github.com/astariul/discord_interactive_help/issues), we will be glad to help !

<h2 align="center">Running in Docker</h2>

A Dockerfile is available to run the example easily. Just build the image :

```
docker build -t discord_interactive_help .
```

And then start it with your Discord bot token :

```
DISCORD_BOT_SECRET="<your_token>" docker run -e DISCORD_BOT_SECRET discord_interactive_help
```

<h2 align="center">Notes</h2>

* *This idea was already known for some time, I didn't get the idea myself. I just wanted to share an easy framework to implement it for your own bot.*

* *This is working only with the Python Discord API.*
