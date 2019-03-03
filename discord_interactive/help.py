from discord_interactive.page import Page
import asyncio

DEFAULT_QUIT_REACT = '❌'

class Help:
    """ Class representing the whole Help system.

    Attributes:
        client (Discord.Client): Discord client (to send messages). 
        page_graph (Page): Page graph representing the whole help pages.
        quit_react (str): Reaction used to leave the help system.. 
    """

    def __init__(self, client, page_graph, quit_react=DEFAULT_QUIT_REACT):
        """ Help constructor

        Args:
            client (Discord.Client): Discord client (to send messages). 
            page_graph (Page): Page graph representing the whole help pages.
            quit_react (str): Reaction used to leave the help system.
        """
        self.client = client
        self.page_graph = page_graph
        self.quit_react = quit_react

    async def display(self, member):
        """ Main function of the Help system.

        This function is the main function of the help system. When a user 
        request help, simply call this function. 
        It will display the first message of the help, and then wait the user to
        react. Depending on the reaction, it will display the next page, etc...

        Args:
            member (Discord.Member): Member who called help. Help will be 
                displayed as a private message to him.
        """

        current_page = self.page_graph
        prev_input = []

        # Never stop displaying help
        while True:
            # Run basic callbacks before displaying the page
            for callback in current_page.get_callbacks():
                await callback(current_page, member, prev_input)

            # Send the current page to the user as private message
            bot_message = await self.client.send_message(member, \
                                                     current_page.content())

            # Display possible reactions
            for react in current_page.get_react_list() + [self.quit_react]:
                await self.client.add_reaction(bot_message, react)

            next_page = None
            # While user give wrong reaction/input, keep waiting for better input
            while next_page is None:
                # Get user input
                reaction, message = await self._get_user_input(member, \
                                                               bot_message, \
                                                               current_page)

                # 2 cases : reaction or message
                if reaction is not None and message is None:
                    # If the user wants to quit, quit
                    if reaction.emoji == self.quit_react:
                        # Clean and quit. This is the only way to quit for now
                        await self.client.delete_message(bot_message)
                        return

                    # Retrieve page based on reaction
                    next_page = current_page.next_page(reaction.emoji)

                elif reaction is None and message is not None:
                    # Retrieve page
                    next_page = current_page.next_page()

            # Before going to next page, remember the input of the user if given
            if message is not None:
                prev_input.append(message)

            # Here the next page is valid. Clean current message and loop
            await self.client.delete_message(bot_message)
            current_page = next_page

    async def _get_user_input(self, member, message, current_page):
        """ Function retrieving the user input.

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
        task_react = asyncio.ensure_future(self.client.wait_for_reaction( \
                        user=member, message=message))
        task_answer = asyncio.ensure_future(self.client.wait_for_message( \
                        author=member, channel=message.channel))
        tasks = [task_react]    # Always wait for user reaction
        if current_page.need_user_input():
            tasks.append(task_answer)   # Sometimes need to expect input too
        
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