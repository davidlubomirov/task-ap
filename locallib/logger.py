from distutils.log import debug
import sys
import logging

DEBUG_ENABLED = False


class SystemLogger(logging.Logger):
    def __init__(self, name: str):
        global DEBUG_ENABLED

        if not isinstance(name, str):
            raise TypeError("{}: invalid type for 'name' parameter. Expecting: string, got {}".format(
                self.__class__.__name__, type(name)))

        logging.Logger.__init__(self, name=name)

        consoleHandler = logging.StreamHandler(sys.stdout)

        if DEBUG_ENABLED:
            consoleHandler.setLevel(logging.DEBUG)
        else:
            consoleHandler.setLevel(logging.INFO)

        consoleFormatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        consoleHandler.setFormatter(consoleFormatter)

        self.addHandler(consoleHandler)


def update_debug_enabled(debug_enabled: bool) -> None:
    global DEBUG_ENABLED

    DEBUG_ENABLED = debug_enabled
