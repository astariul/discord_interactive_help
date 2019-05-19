from discord_interactive.link import ReactLink, MsgLink

DEFAULT_PARENT_REACT = '🔙'
DEFAULT_ROOT_REACT = '🔝'
DEFAULT_LINK_REACTS = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
MSG_LINK = '<msg_link>'

class Page:
    """ Class representing a page of the help.

    This class represents a page of the help. A page is displayed to the user, 
    and the user can naviguate through pages using reaction or messages. 
    A page have several attributes : a message, and a map of linked pages, 
    based on reaction of the user.

    Attributes:
        msg (str): Message to display to the user when displaying the page.
        links (list of Links): List of Links associated to this page.
        msg_link (MsgLink): MsgLink if there is one. It's not part of the links
            list because there can be only 1 msg link per page.
        parent (Link): Link to the parent page.
        root (Link): Link to the root page.
        sep (str): String used to separate the message and the links description
            (for display).
        links_sep (str): String used to separate the links description (between
            each of them) (for display).
    """

    def __init__(self, msg='', sep='\n\n', links_sep='\n'):
        """ Page constructor

        Constructor of the class Page. Create a Page with a message.

        Args:
            msg (str, optional): Message to display to the user when displaying 
                the page.
            sep (str, optional): String used to separate the message and the 
                links description (for display). Defaults to `\n\n`.
            links_sep (str, optional): String used to separate the links 
                description (between each of them) (for display). Defaults to 
                `\n`.
        """
        self.msg = msg
        self.links = []
        self.msg_link = None
        self.parent = None
        self.root = None
        self.sep = sep
        self.links_sep = links_sep

    ####################### Construction of the Tree ###########################

    def link(self, pages, reaction=MSG_LINK, description=None, callbacks=[], 
             is_parent=True, parent_reaction=DEFAULT_PARENT_REACT):
        """ Page linker with reactions.

        Link a page to other pages by creating a link with reaction.

        Args:
            pages (list of Page or Page): List of pages associated to this link.
            reaction (str, optional): Reaction needed to go through the link. 
                If None is given, use a default reaction. If `<msg_link>` is 
                given, this will be a MsgLink, and not a ReactLink. Defaults to 
                `<msg_link>`.
            description (str, optional): Description of the link, to explain to 
                user the effect of this link. Defaults to `None`.
            callbacks (list, optional): List of functions to call when taking 
                this link. Defaults to empty list.
            is_parent (bool, optional): Boolean indicating if the currentpage 
                should be represented as the parent of the pages linked. 
                Defaults to `True`.
            parent_reaction (str or list of str, optional): Reaction to use for 
                the child to come back to its parent (current page). If a list
                is given, each reaction is associated to one page of the list
                of pages given. Defaults to `🔙`.

        Throws:
            IndexError: Only the 9 first links are provided with default 
                reactions (digit 1 ~ 9). If you try to create another link with 
                default reaction, this Exception will be thrown. 
            ValueError: The number of parent reaction given does not correspond
                to the number of child pages.
        """
        # Create the appropriate link
        if reaction == MSG_LINK:        # Create a MsgLink
            self.msg_link = MsgLink(pages, description, callbacks)
        else:                           # Create a ReactLink
            # First, retrieve the default reaction if none was given
            if reaction is None:
                reaction = DEFAULT_LINK_REACTS[len(self.links)]

            # Then create a ReactLink
            l = ReactLink(reaction, pages, description, callbacks)

            # And link it to this page
            self.links.append(l)

        # Create the parent links
        if is_parent:
            self.parent_of(pages, parent_reaction)

    def parent_of(self, pages, parent_reaction=DEFAULT_PARENT_REACT):
        """ Parent Page linker.

        Link a list of pages the current page as a parent.

        Args:
            pages (list of Page or Page): List of pages to associate the current
                page as a parent.
            parent_reaction (str or list of str, optional): Reaction to use for 
                the child to come back to its parent (current page). If a list
                is given, each reaction is associated to one page of the list
                of pages given. Defaults to `🔙`.

        Throws:
            ValueError: The number of parent reaction given does not correspond
                to the number of child pages.
        """
        # Normalize list of pages
        if type(pages) != list:
            pages = [pages]

        if type(parent_reaction) == list:
            if len(pages) != len(parent_reaction):
                raise ValueError("You gave a list of reaction for the parent " \
                    "page, but the number of pages given are not matching this" \
                    " list ({} pages, but {} reactions)".format(len(pages), 
                    len(parent_reaction)))
        else:   # Normalize list of reaction
            parent_reaction = [parent_reaction] * len(pages)

        # Assign to each page this page as parent with the right reaction
        for p, r in zip(pages, parent_reaction):
            # First, create the parent link
            p_link = ReactLink(r, self)

            # Then associate this link to the page
            p.parent = p_link

    def root_of(self, pages, root_reaction=DEFAULT_ROOT_REACT):
        """ Root Page linker.

        Link a list of pages the current page as root.

        Args:
            pages (list of Page or Page): List of pages to associate the current
                page as root.
            root_reaction (str or list of str, optional): Reaction to use for 
                the pages to come back to the root (current page). If a list
                is given, each reaction is associated to one page of the list
                of pages given. Defaults to `🔝`.

        Throws:
            ValueError: The number of root reaction given does not correspond
                to the number of pages given.
        """
        # Normalize list of pages
        if type(pages) != list:
            pages = [pages]

        if type(root_reaction) == list:
            if len(pages) != len(root_reaction):
                raise ValueError("You gave a list of reaction for the root " \
                    "page, but the number of pages given are not matching this" \
                    " list ({} pages, but {} reactions)".format(len(pages), 
                    len(root_reaction)))
        else:   # Normalize list of reaction
            root_reaction = [root_reaction] * len(pages)

        # Assign to each page this page as parent with the right reaction
        for p, r in zip(pages, root_reaction):
            # First, create the parent link
            r_link = ReactLink(r, self)

            # Then associate this link to the page
            p.root = r_link

    ######################## Display of the Tree ###############################

    def content(self):
        """
        This method is called by the Help, to display the content of a Page.
        This will display the main message of the Page, as well as the message
        describing each Link of the Page.
        This method simply construct the string to send to the channel.

        Returns:
            str: Content to display to user.
        """
        content = self.msg
        content += self.sep
        content += self.links_sep.join([l.description for l in self.links if \
            l.description is not None])
        if self.msg_link is not None and self.msg_link.description is not None:
            content += self.links_sep + self.msg_link.description
        return content

    def reactions(self):
        """
        This method is called by the Help, to retrieve the list of reactions 
        that the user can use to interact with the help.

        Returns:
            list of str: List of reactions (str) that the user can use for this
                page.
        """
        return [l.reaction for l in self._all_links()]

    def need_user_input(self):
        """ Method to know if the Help display needs to wait for the user to 
        input something. 

        If the page contains a MsgLink, then the helper needs to wait the user 
        to input something.

        Returns:
            bool: True if there is MsgLink, False otherwise.
        """
        return self.msg_link is not None

    def next_link(self, reaction=None):
        """Accessing the next Link.

        This function access the next Link based on the reaction given. If the 
        reaction is `None`, retrieve the MsgLink. If the reaction is not valid 
        (no link associated to this reaction), `None` is returned.

        Args:
            reaction (str, optional): Reaction chosen by the user, representing 
                a Link. If `None`, the link returned is MsgLink. Default to None. 

        Returns:
            Link or None: The next link to display, based on the reaction of 
                the user, or `None` if the choice of the user is not valid.
        """
        if reaction is None:
            return self.msg_link

        next_link = None
        for l in self._all_links():
            if l.reaction == reaction:
                next_link = l
        return next_link

    ############################## Private #####################################

    def _all_links(self):
        """ Private function

        Return a list of available ReactLink for this page.

        Returns:
            list of ReactLink: All links.
        """
        all_links = self.links
        if self.parent is not None:
            all_links += [self.parent]
        if self.root is not None:
            all_links += [self.root]
        return all_links

