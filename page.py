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
        links (dict of str to Page): List of linked pages, where each reaction 
            ID is linkied to the appropriate page.
        meta_links (dict of str to Page): Similar to links, but contain special
            links (root, parent) : reaction should be displayed at the end.
    """

    def __init__(self, msg, root=None, parent=None, 
            root_react=DEFAULT_ROOT_REACT, parent_react=DEFAULT_PARENT_REACT):
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
        """
        self.msg = msg
        self.links = collections.OrderedDict()
        self.meta_links = collections.OrderedDict()

        if parent:
            self.meta_links[parent_react] = parent
        if root:
            self.meta_links[root_react] = root

    def add_link(self, page, react=None):
        """ Method to add a link to the page.

        Args:
            page (Page): Page to link.
            react (str, optional): Reaction to access the page. If None is given,
                use defaults emoji (numbers). Defaults to None.
        """
        if react is None:
            # Use default emoji for reaction 
            assert len(self.links) < len(DEFAULT_LINK_REACTS), \
                "There is not enough default reaction emoji. Please specify " \
                "emoji explicitly."
            react = DEFAULT_LINK_REACTS[len(self.links)]
            
        self.links[react] = page

    def get_react_list(self):
        """ Method to access the list of reactions of linked pages.

        Returns:
            list: List of str where each str represent a reaction of a linked 
                page.
        """
        return list(self._all_links().keys())

    def next_page(self, react):
        """Accessing the next Page.

        This function access the next page based on the reaction given. If the 
        choice is not valid, None is returned.

        Args:
            react (str): Reaction chosen by the user, representing a linked Page. 

        Returns:
            Page or None: The next page to display, based on the reaction of 
                the user, or None if the choice of the user is not valid.
        """
        try:
            return self._all_links()[react]
        except KeyError:
            return None

    def _all_links(self):
        """ Private function

        Return a concatenated dictionnary between links and meta-links.

        Returns:
            OrderedDict: Concatenated links and meta-links.
        """
        return collections.OrderedDict(list(self.links.items()) + \
                                       list(self.meta_links.items()))