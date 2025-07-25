class SmartFile:
    """
    Can be used to build a file-like object in which one can dynamically write.

    This class can be used to create a file-like object in which an action defined by its methods is performed only if its internal
    attribute `enabled` is set to `True`.

    Attributes
    ----------
    enabled: bool
        Checks wether the action is performed or not.
    file: str
        Name of the file to which the action is performed.

    Methods
    -------
    setup(file_name)
        sets the `enabled` attribute to `True` and opens the file.
    write(message)
        writes `message` to the file.
    close()
        closes the opened file.
    """
    def __init__(self):
        """
        Initializes the SmartFile object with `enabled = False` and `file = None` by default.
        """
        self.enabled = False
        self.file = None

    def setup(self, file_name):
        """
        Sets the `enabled` attribute to `True` and opens the file with name `file_name`.

        Args
        ----
        file_name: str
            Name or path of the file that is opened.
        """
        self.enabled = True
        self.file = open(file_name, 'w')

    def write(self, message):
        """
        Writes the string `message` in the file only if `enabled` is set to `True` and `file` is not `None`.

        Args
        ----
        message: str
            string that is written on the file.
        """
        if self.enabled and self.file:
            self.file.write(message + '\n')

    def close(self):
        """
        Closes the file object if `enabled` is set to `True` and `file` is not `None`.
        """
        if self.enabled and self.file:
            self.file.close()
    
        