import string
import calendar
import time

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

        # naive and dumb solution
        # should in fact make one write-out of the accumulated messages at the end of the execution or at least with some periodicity

        # gmtime = time.gmtime()
        # timestamp = calendar.timegm(gmtime)

        fileName = "{}.txt".format(Configurations.Configuration.BASE_LOG_FILE_NAME)

        file = open(fileName, "a")
        file.write(message + "\n")
        file.close()