# Usage

## Step-by-step Usage

After installing the package (see [Installation](index.md#installation)), import the class `Page` and `Help` into your bot's code, and define the content of each page of your help manual :

```python
from discord_interactive import Page, Help

# Define each page
root = Page("Welcome !\n")
page_1 = Page("This is page 1")
page_2 = Page("This is page 2")
```

Then, link the pages together :

```python
# Link pages together
page_1.link(page_2, description="Click this icon to access page 2", reaction="💩")
root.link(page_1, description="Click this icon to access page 1")
```

Optionally, you can define a page as root of other pages, so the user can easily come back to the root with a specific reaction :

```python
# Set the root page as the root of other page (so user can come back with a specific reaction)
root.root_of([page_1, page_2])
```

Finally, create the `Help` object and display the help whenever the user call the right command :

```python
# Create the Help object
client = discord.Client()
h = Help(client, root)

# And display the help !
@client.event
async def on_message(message):
    if message.author != client.user:  # Do not answer to myself
        if message.content.startswith("/help"):
            await h.display(message.author)
```

## Full Example

```python
from discord_interactive import Page, Help

# Define each page
root = Page("Welcome !\n")
page_1 = Page("This is page 1")
page_2 = Page("This is page 2")

# Link pages together
page_1.link(page_2, description="Click this icon to access page 2", reaction="💩")
root.link(page_1, description="Click this icon to access page 1")

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
        if message.content.startswith("/help"):
            await h.display(message.author)
```

## Experience it !

You can try the interactive help in [this Discord server](https://discord.gg/cH6hUbw) !

Simply join the server, and type `/help` in the chat.

Also, take a look at the code for this interactive help ! Check out the script [`main.py`](https://github.com/astariul/discord_interactive_help/blob/main/main.py).

## Advanced

In the basic example, you saw how to display a help manual and allow the user to easily interact with this manual.

But as we will see shortly, you can also use callbacks to bring dynamic contents to your interactive help.

Callbacks allow you bring dynamic contents and interactions in three ways :

* Update the content of the next page
* Choose a path between several pages
* Get user input

### Callback Signature

Your callback should follow this signature :

```python
async def callback_name(link: Link, member: discord.Member, prev_input: List[discord.Message])
```

where :

* `link` is the current link being displayed to the user.
* `member` is the member that is currently using the interactive help.
* `prev_input` is the list of messages previously inputted but the user. If the user didn't input anything, this list is empty.

!!! warning "Important"
    Your callback should be asynchronous.

### Updating the content of the next page

Let's create an interactive help that display a list of names retrieved from a database (dynamically) and display them in the interactive help.

First, we define the pages of our help :

```python
from discord_interactive import Help, Page

welcome_page = Page("What would you like to do ?\n")
name_display_page = Page("")
```

!!! info "Note"
    Note that the second page has an empty content. That's because we will update the content dynamically in the callback !

Then we define our callback, which will dynamically retrieve the list of names to display, and populate the content of the second page :

```python
async def display_names(link, member, prev_input):
    # Call the database and get the list of names to display
    names = db.retrieve_names()

    # We have access to the link, so we can modify its content (dynamically)
    link.page().msg = "List of existing users :\n\n" + "\n".join(names) + "\n"
```

Once we have defined our callback, just create the link between the pages and add the callback there :

```python
welcome_page.link(
    name_display_page, description="Get the list of users", callbacks=display_names
)
```

So when the user choose that link, the callback is run and the content of the next page is updated dynamically.

### Choosing a path between several pages

Let's say you want to check the status of your database, and display a different message (success or failure) based on this. Let's see how we can do that with a callback.

First, we define the pages of our help :

```python
welcome_page = Page("Hello")
page_fail = Page("Fail")
page_success = Page("Success")
```

Then we declare our callback, which will dynamically choose which path to follow :

```python
async def check_status(link, member, prev_input):
    # Check the database status
    is_db_up = db.is_up()

    if is_db_up:
        link.path = 0
    else:
        link.path = 1
```

Finally, just create the link between the pages and add the callback there :

```python
welcome_page.link([page_fail, page_success], callbacks=check_status)
```

So when the user choose that link, the callback is run and the correct next page is displayed based on the callback's execution.

### Getting user's input

You can also set the link between page to record a user's input (and use that input in your callback).

Like before, we define our pages :

```python
welcome_page = Page("Enter your name :")
end_page = Page("Thanks !")
```

Then we define our callback, where we retrieve the user's input and save it in database :

```python
async def save_name(link, member, prev_input):
    # Retrieve the last input from the user
    user_input = prev_input[-1].content

    # Save it in our DB
    db.save_name(user_input)
```

!!! tip
    Did you notice how I used negative index to retrieve the user input ?

    That's because `prev_input` contains **all** previous inputs. Here we want the last one, so we use `-1` index. But it's definitely possible to retrieve several previous inputs !

And we create the link between the page, adding the callback and ensuring we expect a user input :

```python
welcome_page.link(end_page, callbacks=save_name, user_input=True)
```

So when the inputs its username, the callback run and the username is saved in the database.

### Advanced Usage Example

As before, you can try it in [this Discord server](https://discord.gg/cH6hUbw) !

Simply join the server, and type `/guild` in the chat.

Also take a look at the code in the script [`main.py`](https://github.com/astariul/discord_interactive_help/blob/main/main.py).
