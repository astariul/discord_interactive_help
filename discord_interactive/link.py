"""Module containing the definition of the `Link` classes. These classes are
not public-facing, they are used only internally.
User can create links using the `link()` method in the `Page` class.
"""


class Link:
    """Base class for all type of link.

    Links represent branches of the help tree.
    All links can have callbacks, and a description.
    Links also have a list of child pages. Most of the time, we want simple link,
    so the link have a single child, which is displayed if the link is taken.
    But sometimes, we want something more complex, like if the user take link1,
    ans user is a specific role, we will display a different page. That's why
    links can have several child pages.
    By default, if callbacks does not change this behavior, the first child of
    the list is selected.

    Attributes:
        pages (list of Page): List of pages associated to this link.
        description (str): Description of this link, to explain to user the
            effect of this link.
        callbacks (list): List of functions to call when taking this link.
        path (int): Which child page will be displayed. Default to 0 (the first
            Page of the list).
    """

    def __init__(self, pages, description=None, callbacks=[]):
        """Link constructor.

        Create a Link with a list of child pages, a description, and
        callbacks optionally.

        Args:
            pages (list of Page or Page): List of pages associated to this link.
            description (str, optional): Description of this link, to explain to
                user the effect of this link. Defaults to `None`.
            callbacks (list, optional): List of functions to call when taking
                this link. Defaults to empty list.
        """
        # Normalize input
        if type(pages) == list:
            self.pages = pages
        else:
            self.pages = [pages]
        if type(callbacks) == list:
            self.callbacks = callbacks
        else:
            self.callbacks = [callbacks]

        self.description = description
        self.path = 0

    def page(self):
        """This method is called by the Help, after calling the callbacks.
        So the path was updated (or not) to select the right page, and we should
        return the appropriate page.

        Returns:
            Page: The page selected by callbacks (or default choice).
        """
        return self.pages[self.path]


class ReactLink(Link):
    """Class for link using reaction to naviguate to next page.

    Attributes:
        reaction (str): Reaction needed by this link to display the page.
    """

    def __init__(self, reaction, pages, description=None, callbacks=[]):
        """ReactLink constructor.

        Create a ReactLink to other pages, with a reaction, and a possibly a
        description, as well as callbacks.

        Args:
            reaction (str): Reaction needed by this link to display the page.
            pages (list of Page or Page): Page to display when this link is used.
            description (str, optional): Description of this link, to explain to
                user the effect of this link. Defaults to `None`.
            callbacks (list, optional): List of functions to call when taking
                this link. Defaults to empty list.
        """
        super(ReactLink, self).__init__(pages, description, callbacks)
        self.reaction = reaction

        # We need to update the description of this link to add the reaction
        if self.description is not None:
            self.description = self.reaction + " " + self.description


class MsgLink(Link):
    """Class for link using message to naviguate to next page."""

    def __init__(self, pages, description=None, callbacks=[]):
        """MsgLink constructor.

        Create a MsgLink with a list of child pages, a description, and
        callbacks optionally.

        Args:
            pages (list of Page or Page): List of pages associated to this link.
            description (str, optional): Description of this link, to explain to
                user the effect of this link. Defaults to `None`.
            callbacks (list, optional): List of functions to call when taking
                this link. Defaults to empty list.
        """
        super(MsgLink, self).__init__(pages, description, callbacks)


class RootLink(Link):
    """Class for the first link of the help tree."""

    def __init__(self, pages, callbacks=[]):
        """RootLink constructor.

        RootLink is like any other links (callbacks included), but there is no
        description.

        Args:
            pages (list of Page or Page): List of pages associated to this link.
            callbacks (list, optional): List of functions to call when taking
                this link. Defaults to empty list.
        """
        super(RootLink, self).__init__(pages, callbacks=callbacks)
