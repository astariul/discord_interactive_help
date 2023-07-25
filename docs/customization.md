# Customization

Let's see how to customize messages from the help system.

![](https://user-images.githubusercontent.com/22237185/86127898-9403a780-bb1b-11ea-86f0-94c7093f3c86.png)

&nbsp;

**1. The title of the page.** You can change it by specifying the `title` keyword argument through the [Page constructor](code_ref.md#discord_interactive.page.Page.__init__).

```python
page_help = Page('message', title="Welcome to the help !")
```

&nbsp;

**2. The main message of the page.** You can change it through the [Page constructor](code_ref.md#discord_interactive.page.Page.__init__).

```python
page_help = Page('Help pages are simply a tree of pages and the system navigate through this tree.')
```

&nbsp;

**3. The description of each link.** You can change it when creating a link to a page with the [link method](code_ref.md#discord_interactive.page.Page.link).

```python
page_help.link(page_react, description='What about reaction ?')
```

&nbsp;

**4. The emoji of reaction for a given link.** You can change it when creating a link to a page with the [link method](code_ref.md#discord_interactive.page.Page.link). By default, the emoji used is the digit emoji.

```python
page_help.link(page_react, description='What about reaction ?')                     # Use default emoji
page_help.link(page_react, reaction='👌', description='What about reaction ?')      # Use customized emoji
```

&nbsp;

**5. The emoji for the parent page.** You can change it either when creating a link to a page with the [link method](code_ref.md#discord_interactive.page.Page.link), or by setting a parent page separately with the [parent_of method](code_ref.md#discord_interactive.page.Page.parent_of).

```python
page_help.link(page_react, description='What about reaction ?', parent_reaction='👌')        # Specified when
# parent reaction is automatically created when making a link

page_guild.parent_of(page_guild_register, parent_reaction='👌')              # Specified when creating a new parent link
```

&nbsp;

**6. The emoji for the root page.** You can change it when setting a root page with the [root_of method](code_ref.md#discord_interactive.page.Page.root_of).

```python
root.root_of([page_react, page_everyone, page_slow, page_help, page_cmd], root_reaction='👌')
```

&nbsp;

**7. The emoji for quitting.** You can change it with the [Help constructor](code_ref.md#discord_interactive.help.Help.__init__).

```python
h = Help(client, root, quit_react='👌')
```

&nbsp;

**8. The color of the Embed.** You can change it by specifying the `color` keyword argument through the [Page constructor](code_ref.md#discord_interactive.page.Page.__init__).

```python
page_help = Page('message', color=0xE67E22)
```

---

Prior to `v4` of the package, Help was rendered as simple text message. From `v4` of the package, the Help is now rendered as [`Embed`](https://discordpy.readthedocs.io/en/latest/api.html#embed) by default, because the interface looks cleaner.

If you still want to display your page as a simple text message, you can specify it by setting the argument `embed` to `False` in the [Page constructor](code_ref.md#discord_interactive.page.Page.__init__).

```python
page_help = Page('message', embed=False)
```

!!! warning
    Simple text message pages can't use `Embed` features, such as title and color.

!!! tip
    If you need to customize your display further, you can always subclass [`Page`](code_ref.md#discord_interactive.page.Page) and redefine [`get_message()`](code_ref.md#discord_interactive.page.Page.get_message) or [`get_embed()`](code_ref.md#discord_interactive.page.Page.get_embed).
