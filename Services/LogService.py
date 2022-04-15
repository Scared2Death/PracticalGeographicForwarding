import string

import Configurations.Configuration

class LogService:

    @staticmethod
    def log(message: string):

        if (Configurations.Configuration.LOG_TO_CONSOLE):
            LogService.__logToConsole(message)

        if (Configurations.Configuration.LOG_TO_FILE):
            LogService.__logToFile(message)

    @staticmethod
    def __logToConsole(message: string):
        print(message)

    @staticmethod
    def __logToFile(message: string):
        # implementation required
        return