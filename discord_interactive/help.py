"""Module containing the definition of the `Help` class. The `Help` class
contains the code to properly display the help tree, and handle interactions
with the user.
"""

import asyncio

from discord_interactive.link import RootLink
from discord_interactive.page import PageType


DEFAULT_QUIT_REACT = "❌"


class Help:
    """Class representing the whole Help system.

    Attributes:
        client (Discord.Client): Discord client (to send messages).
        tree (RootLink): Link representing the whole help pages as a tree.
        quit_react (str): Reaction used to leave the help system..
    """

    def __init__(self, client, pages, callbacks=[], quit_react=DEFAULT_QUIT_REACT):
        """Help constructor.

        Args:
            client (Discord.Client): Discord client (to send messages).
            pages (list of Page or Page): List of pages representing the
                starting point of the help.
            callbacks (list, optional): List of functions to call when taking
                this link. Defaults to empty list.
            quit_react (str, optional): Reaction used to leave the help system.
                Defaults to `❌`.
        """
        self.client = client
        self.quit_react = quit_react

        # Create a RootLink, representing the root of the help tree
        root = RootLink(pages, callbacks)
        self.tree = root

    async def display(self, member):  # noqa: C901
        """Main function of the Help system.

        This function is the main function of the help system. When a user
        request help, simply call this function.
        It will display the first message of the help, and then wait the user to
        react. Depending on the reaction, it will display the next page, etc...

        Args:
            member (Discord.Member): Member who called help. Help will be
                displayed as a private message to him.
        """
        current_link = self.tree
        prev_input = []

        # Never stop displaying help
        while True:
            # Run basic callbacks before displaying the page
            for callback in current_link.callbacks:
                await callback(current_link, member, prev_input)

            # After running the callbacks, we can retrieve the page to be
            # displayed
            page = current_link.page()

            # Send the current page to the user as private message :
            # Ensure the channel exist
            if member.dm_channel is None:
                await member.create_dm()

            # Different page type should be sent differently
            if page.type == PageType.MESSAGE:
                bot_message = await member.dm_channel.send(page.get_message())
            elif page.type == PageType.EMBED:
                bot_message = await member.dm_channel.send(embed=page.get_embed(), content=None)

            # Display possible reactions
            for react in page.reactions() + [self.quit_react]:
                asyncio.ensure_future(bot_message.add_reaction(react))

            next_link = None
            # While user give wrong reaction/input, keep waiting for better input
            while next_link is None:
                # Get user input
                reaction, message = await self._get_user_input(member, bot_message, page)

                # 2 cases : reaction or message
                if reaction is not None and message is None:
                    # If the user wants to quit, quit
                    if reaction.emoji == self.quit_react:
                        # Clean and quit. This is the only way to quit for now
                        await bot_message.delete()
                        return

                    # Else, retrieve the next link based on reaction
                    next_link = page.next_link(reaction.emoji)

                elif reaction is None and message is not None:
                    # Retrieve next link
                    next_link = page.next_link()

            # Before going to next page, remember the input of the user if given
            if message is not None:
                prev_input.append(message)

            # Here the next page is valid. Clean current message and loop
            await bot_message.delete()
            current_link = next_link

    async def _get_user_input(self, member, message, current_page):
        """Function retrieving the user input.

        This function retrieve the user input. The user input is either a
        message or a reaction (if the page does not need user input, only
        reaction will be an acceptable input).
        If both input and reaction are correct input, return the first event met.

        Args:
            member (Discord.Member): Member who called help. Help will be
                displayed as a private message to him.
            message (Discord.Message): Message sent by the bot, where the user
                should react.
            current_page (Page): Page being displayed. We know what kind of
                input we need from this page.

        Returns:
            reaction (Discord.Reaction): Reaction of the user, or None if the
                correct input was a user message.
            message (Discord.Message): Message of the user, or None if the
                correct input was a user reaction.
        """

        def check_reaction(reaction, user):
            return user == member

        def check_message(m):
            return m.author == member

        task_react = asyncio.ensure_future(self.client.wait_for("reaction_add", check=check_reaction))
        task_answer = asyncio.ensure_future(self.client.wait_for("message", check=check_message))
        tasks = [task_react]  # Always wait for user reaction
        if current_page.need_user_input():
            tasks.append(task_answer)  # Sometimes need to expect input too

        # Wait the actual user input
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        # Depending on what the user did, return the right thing
        if task_react in done:
            # User reacted
            reaction, _ = done.pop().result()
            return reaction, None
        else:
            # User answered
            msg = done.pop().result()
            return None, msg
