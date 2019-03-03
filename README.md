# Discord Interactive Help

![gif](https://user-images.githubusercontent.com/22237185/53283254-da5a3100-3786-11e9-95cd-cd4dd4859bd2.gif)

A Discord python framework to display an interactive help easily.

## Features

* 🔆 **Easy to naviguate** : Use reactions to naviguate through the Help manual.
* ⚙ **Customized reaction** : Use any emoji as naviguation icon.
* 🎮 **Commands support** : Go even further with interactive commands.

## How to use

Download the package :

`pip install discord-interactive`

---

Import the `Page` and `Help` objects into your bot's code, and create your own help manual :

```
from discord_interactive import Page, Help

# Define each page
root = Page('Welcome !\n')
page_1 = Page('This is page 1', parent=root)
page_2 = Page('This is page 2', parent=page_1, root=root)

# Link pages together
page_1.add_link(page_2, 'Click this icon to access page 2', '💩')
root.add_link(page_1, 'Click this icon to access page 1')

# Create the Help object
client = discord.Client()
h = Help(client, root)

# And display the help !
await h.display(message.author)
```

---

**For a full working example, please take at [this Repl.it](https://repl.it/@NicolasRemond/example-of-interactive-help).**

**Or you can simply experience the interactivity of this full working example by joining [this Discord server](https://discord.gg/cH6hUbw). Just type /help in the chat !** 

## Further details

The basic usage was shown in this README. If you are interested in more detailed explanations or advanced usage, such as interactive commands, please take a look at the [wiki](https://github.com/astariul/discord_interactive_help/wiki) !

Example of advanced usage :

![gif](https://user-images.githubusercontent.com/22237185/53492662-c4c56e00-3adc-11e9-8be8-1b10d9f85e8a.gif)

If you can't find what you are looking for, you can open an [issue](https://github.com/astariul/discord_interactive_help/issues).

## Notes

* *This idea was already known for some time, I didn't get the idea myself. I just wanted to share an easy framework to implement it for your own bot.*

* *This is working only with the Python Discord API.*
