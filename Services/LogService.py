import string
from datetime import datetime
from os import path

import Configurations.Configuration

class LogService:

    @staticmethod
    def log(message: string):
        content = '{}\t{}'.format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), message)
        if (Configurations.Configuration.LOG_TO_CONSOLE):
            LogService.__logToConsole(content)

        if (Configurations.Configuration.LOG_TO_FILE):
            LogService.__logToFile(content)

    @staticmethod
    def debug(message: string):
        if (Configurations.Configuration.DEBUG):
            LogService.log(message)

    @staticmethod
    def clearFileContents():
        fileName = Configurations.Configuration.LOG_FILE_NAME
        if path.exists(fileName):
            file = open(fileName, 'r+')
            file.truncate(0)
        else:
            open(fileName, 'w').close()

    @staticmethod
    def __logToConsole(message: string):
        print(message)

    @staticmethod
    def __logToFile(message: string):

        # naive and dumb solution
        # should in fact make one write-out of the accumulated messages at the end of the execution or at least with some periodicity

        fileName = Configurations.Configuration.LOG_FILE_NAME

        file = open(fileName, "a")
        file.write(message + "\n")
        file.close()