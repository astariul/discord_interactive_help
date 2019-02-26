import collections

DEFAULT_PARENT_REACT = '🔙'
DEFAULT_ROOT_REACT = '🔝'
DEFAULT_LINK_REACTS = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']

class Page:
    """ Class representing a page of the help.

    This class represents a page of the help. A page is displayed to the user, 
    and the user can naviguate through page using reaction. 
    A page have several attributes : a message, and a map of linked pages, 
    based on reaction of the user.

    Attributes:
        msg (str): Message to display to the user when displaying the page.
        connector (str): String used to connect each description of each link.
        links (dict of str to Page): List of linked pages, where each reaction 
            ID is linkied to the appropriate page.
        links_msg (list of str): List of messages for each link. 
        meta_links (dict of str to Page): Similar to links, but contain special
            links (root, parent) : reaction should be displayed at the end.
        input_link (Page): Page to display if user input a message.
        callbacks (list): List of basic callbacks (no user input) to call when 
            displaying the page.
        user_callbacks (list): List of callbacks with user input to call when 
            displaying the page.
    """

    def __init__(self, msg, root=None, parent=None, 
            root_react=DEFAULT_ROOT_REACT, parent_react=DEFAULT_PARENT_REACT,
            connector='\n', callbacks=[], user_callbacks=[]):
        """ Page constructor

        Constructor of the class Page. Create a Page with a message. 
        and optionally a root Page and a parent Page.
        A page without root is a root itself. A page can have no parent if you
        don't want to have a return function.

        Args:
            msg (str): Message to display to the user when displaying the page.
            root (Page, optional): Root Page. Defaults to None.
            parent (Page, optional): Parent Page. Defaults to None.
            root_react (str, optional): Reaction to access the root page.
            parent_react (str, optional): Reaction to access the parent page.
            connector (str, optional): Connector to join each description of 
                each link. Defaults to `\n`.
            callbacks (list, optional): List of basic callbacks (no user input),
                to be called when displaying page. Defaults to empty list.
            user_callbacks (list, optional): List of callbacks with user input,
                to be called when displaying page. Defaults to empty list.
        """
        self.msg = msg
        self.connector = connector
        self.links = collections.OrderedDict()
        self.links_msg = []
        self.meta_links = collections.OrderedDict()
        self.input_link = None

        if parent:
            self.meta_links[parent_react] = parent
        if root:
            self.meta_links[root_react] = root

        self.callbacks = callbacks
        self.user_callbacks = user_callbacks

    def add_link(self, page, msg=None, react=None, after_msg=False):
        """ Method to add a link to the page.

        Args:
            page (Page): Page to link.
            msg (str, optional): Description of this link. This message is 
                supposed to help the user understand to which page he is going
                to be redirected if he clicks this link. Defaults to None.
            react (str, optional): Reaction to access the page. If None is given,
                use defaults emoji (numbers). Defaults to None.
            after_msg (bool, optional): If True, this link represent the next
                page to display after a user input a message. Mutually exclusive
                with the parameter react, and the parameter message (description
                of the page should explain to user what to input). Defaults to 
                False.
        """
        if after_msg:
            if react is not None:
                raise ValueError("No reaction should be given in the case of " \
                                 "a link after a user input")
            if msg is not None:
                raise ValueError("No message should be given to describe a link" \
                                 "after a user input")
            self.input_link = page
            return

        if react is None:
            # Use default emoji for reaction 
            assert len(self.links) < len(DEFAULT_LINK_REACTS), \
                "There is not enough default reaction emoji. Please specify " \
                "emoji explicitly."
            react = DEFAULT_LINK_REACTS[len(self.links)]

        self.links[react] = page

        # Add links message
        if msg is None:
            self.links_msg.append('')
        else:
            self.links_msg.append(msg)

    def content(self):
        """ Method to get the content of a page.

        This method return the content of a page, concatenating the message of 
        the page and the descriptions of each links of the page.

        Returns:
            str: The content of the page.
        """
        content = self.msg
        for reaction, msg in zip(self.get_react_list(), self.links_msg):
            content += self.connector + reaction + ' ' + msg
        return content

    def get_react_list(self):
        """ Method to access the list of reactions of linked pages.

        Returns:
            list: List of str where each str represent a reaction of a linked 
                page.
        """
        return list(self._all_links().keys())

    def need_user_input(self):
        """ Method to know if the Help display needs to wait for the user to 
        input something. 

        If the page contains user callbacks, then the helper needs to wait the 
        user to input something. In other cases, just do the default behavior
        (wait for a reaction of the user).

        Returns:
            bool: True if there is some user callbacks to call, False otherwise.
        """
        return bool(self.user_callbacks)

    def next_page(self, react=None):
        """Accessing the next Page.

        This function access the next page based on the reaction given. If the 
        choice is not valid, None is returned.

        Args:
            react (str, optional): Reaction chosen by the user, representing a 
                linked Page. If None, the page returned is the special input 
                page. Default to None. 

        Returns:
            Page or None: The next page to display, based on the reaction of 
                the user, or None if the choice of the user is not valid.
        """
        if react is None:
            return self.input_link

        try:
            return self._all_links()[react]
        except KeyError:
            return None

    def get_basic_callbacks(self):
        """Accessing the list of basic callbacks.

        Returns:
            List of callbacks: Basics callbacks to call before page is displayed.
        """
        return self.callbacks

    def get_input_callbacks(self):
        """Accessing the list of callbacks requiring input.

        Returns:
            List of callbacks: Callbacks with input to call after user sent its
                input.
        """
        return self.user_callbacks

    def _all_links(self):
        """ Private function

        Return a concatenated dictionnary between links and meta-links.

        Returns:
            OrderedDict: Concatenated links and meta-links.
        """
        return collections.OrderedDict(list(self.links.items()) + \
                                       list(self.meta_links.items()))