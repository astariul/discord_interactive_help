from page import Page

DEFAULT_QUIT_REACT = '❌'

class Help:
    """ Class representing the whole Help system.

    Attributes:
        page (Page): Current page being displayed.
        message (Discord.Message): Discord message where the help was displayed (in order to update that message).
        member (Discord.Member): Discord member who requested the help. The help    
            will be displayed in a private channel to the member. 
    """

    def __init__(self, client, page_tree, quit_react=DEFAULT_QUIT_REACT):
        """ Help constructor

        Args:
            client (Discord.Client): Discord client (to send messages). 
            page_tree (Page): Page tree representing the whole help pages.
            quit_react (str): Reaction used to leave the help system.
        """
        self.client = client
        self.page_tree = page_tree
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

        current_page = self.page_tree

        # Never stop displaying help
        while True:
            # Send the current page to the user as private message
            message = await self.client.send_message(member, current_page.msg)

            # Display possible reactions
            for react in current_page.get_react_list():
                await self.client.add_reaction(message, react)

            next_page = None
            # While user give wrong reaction, do nothing
            while next_page is None:
                # Wait for the user to react
                reaction, _ = await self.client.wait_for_reaction(user=member, \
                                                                message=message)

                # If the user wants to quit, quit
                if reaction.emoji == self.quit_react:
                    return      # Only here we quit

                # Retrieve page based on reaction
                next_page = current_page.next_page(reaction.emoji)

            # Here the next page is valid. Clean current message and loop
            await self.client.delete_message(message)
            current_page = next_page