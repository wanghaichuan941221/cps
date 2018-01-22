import time


class Logger:
    """The Logger class is used to print messages to the console without directly calling the built-in print function,
    which provides more control over and simplifies formatting as well as some other aspects.
    """

    def __init__(self):
        """The constructor for the Logger class."""

        # Set the variable log_on to the initial value of True.
        self.log_on = True

    def log(self, src, msg):
        """This function prints a message, including the time and source of the message, nicely formatted."""

        # Check if logging is enabled:
        if self.log_on:
            print('{:<21}'.format(str(time.time())), '{:<24}'.format(src), msg)

    def print(self, msg):
        """Just a simple print function to be consistent with not using the built-in print function in any other
        classes.
        """
        
        print(msg)
