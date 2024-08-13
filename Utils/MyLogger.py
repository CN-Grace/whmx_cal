import logging
import os


class MyLogger:
    def __init__(self, name, level=logging.INFO):
        if not os.path.exists("./Logs"):
            os.mkdir("./Logs")

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        self.file_handler = logging.FileHandler(f"./Logs/{name}.log", mode="w")
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def get_logger(self):
        return self.logger
