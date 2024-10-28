from datetime import datetime

class Logger:

    log = ""

    def addToLog(self, line):
        self.log += f"{datetime.now()} \t {line} \n"

    def writeFile(self, path):
        file = open(path, "w")
        file.write(self.log)
