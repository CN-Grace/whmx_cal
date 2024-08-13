from requests import session
from bs4 import BeautifulSoup
import pandas as pd
import re
from Model.器者 import 器者
from Utils.MyLogger import MyLogger
from urllib.parse import quote


class DataUpdater:
    def __init__(self, config):
        self.root_url = config.root_url
        self.器者_list_url = config.器者_list_url
        self.parser = config.parser
        self.encoding = config.encoding

        self.logger = MyLogger("Crawler").get_logger()
        self.web_session = session()
        self.web_session.headers.update(config.headers)

        self.器者_urls_dict = {}
        self.器者_data_list = []
        self.器者_data = None

    def get_器者_urls_list(self):
        器者_list_html = self.web_session.get(self.器者_list_url).text
        self.logger.info(f"Get 器者 list from {self.器者_list_url}")
        器者_list_soup = BeautifulSoup(器者_list_html, self.parser)
        self.logger.info("Parse 器者 list")
        器者_list = 器者_list_soup.find("div", id="CardSelectTr").find_all("div", class_="visible-xs")
        self.logger.info(f"Get 器者 lists with length: {len(器者_list)}")
        for 器者 in 器者_list:
            器者_name = 器者.find("a")["title"]
            器者_url = str(self.root_url + 器者.find("a")["href"]).replace(quote(器者_name), f"index.php?title={quote(器者_name)}&action=edit")
            self.logger.info(f"Get 器者: {器者_name}, url: {器者_url}")
            self.器者_urls_dict[器者_name] = 器者_url

    def get_器者_data(self):
        for 器者_name, 器者_url in self.器者_urls_dict.items():
            self.logger.info(f"Get {器者_name} data from {器者_url}")
            器者_data_html = self.web_session.get(器者_url).text
            self.logger.info(f"Parse {器者_name} data")
            器者_data_soup = BeautifulSoup(器者_data_html, self.parser)
            器者_data = 器者_data_soup.find("textarea").text
            self.器者_data_list.append(self.parse_器者_data(器者_data))
            self.器者_data = pd.concat(self.器者_data_list, ignore_index=True)

    def parse_器者_data(self, text):
        result = 器者()
        for line in text.split("\n"):
            for attribute in result.__dict__.keys():
                if line.startswith(f"|{attribute}="):
                    attribute_value = re.sub(string=line, pattern="<.*?>", repl="").split("=")[-1].replace("\t", "")
                    result.__dict__[attribute] = attribute_value
                    self.logger.info(f"Get {attribute} with value: {attribute_value}")
        return pd.DataFrame(result.__dict__, index=[0])
