# Discord Interactive Help
A Discord python framework to display an interactive help easily.

## What is this repository

This repository allow you to build an interactive help page for your Discord bot really easily.

Example of interactive help :

![gif](https://user-images.githubusercontent.com/22237185/53283254-da5a3100-3786-11e9-95cd-cd4dd4859bd2.gif)

## Features

* 🔆 **Easy to naviguate** : Use reactions to naviguate through the Help manual.
* ⚙ **Customized reaction** : Use any emoji as naviguation icon.

## How to use

Download the files `help.py` and `page.py` into your bot's code.

Then, create your help manual by defining pages :

```
root = page.Page('Welcome !\n')
page_1 = page.Page('This is page 1', parent=root)
page_2 = page.Page('This is page 2', parent=page_1, root=root)
```

*Note : Adding a parent page (with `parent` in the constructor) will create a button for going back to previous page automagically. Adding a root page (with `root` in the constructor) will create a button for going back to the beginning of the help manual automagically.*

*Note 2 : You can customize the emoji for the parent/root link with `parent_react` and `root_react` in the constructor. Example :*
`page_1 = page.Page('This is page 1', parent=root, parent_react='💩')`

---

After defining your pages, you should link them together. You can do that using custom emoji :

`page_1.add_link(page_2, 'Click this icon to access page 2', '💩')`

... Or using default emojis (numbers : '⃣, '⃣, etc...) :

`root.add_link(page_1, 'Click this icon to access page 1')`

---

Finally define the help system using the root of your linked tree :

```
client = discord.Client()
h = Help(client, root)
```

---

And now, you can display help whenever you want ! Like this :

`await h.display(message.author)`

---

**For a full working example, please take a look at `example/` folder.**

**You can also look at [this Repl.it](https://repl.it/@NicolasRemond/example-of-interactive-help), where the example is implemented.**

## Notes

* *This idea was already known for some time, I didn't get the idea myself. I just wanted to share an easy framework to implement it for your own bot.*

* *This is working only with the Python Discord API.*
