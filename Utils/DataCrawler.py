from requests import session
from bs4 import BeautifulSoup
import pandas as pd
import re
from Model.器者 import 器者
from Utils.MyLogger import MyLogger
from urllib.parse import quote
import time


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
            器者_url = str(self.root_url + 器者.find("a")["href"][1:]).replace(quote(器者_name), f"index.php?title={quote(器者_name)}&action=edit")
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
            time.sleep(1)

    def parse_器者_data(self, text):
        result = 器者()
        for line in text.split("\n"):
            for attribute in result.__dict__.keys():
                if line.startswith(f"|{attribute}="):
                    attribute_value = re.sub(string=line, pattern="<.*?>", repl="").split("=")[-1].replace("\t", "")
                    if "/" in attribute_value:
                        attribute_value = self.split_level_data(attribute_value)
                    result.__dict__[attribute] = str(attribute_value)
                    self.logger.info(f"Get {attribute} with value: {attribute_value}")
        return pd.DataFrame(result.__dict__, index=[0])

    def split_level_data(self, data):
        # 获取所有的字符串数据，除掉所有类似于10/20/30或者10%/20%/30%这样的被/分割的数据，保留字符串中单个的数字和百分号
        string_data = re.compile(pattern="[^\d/%]+").findall(data)
        temp_data = re.split(pattern="[^\d/%]", string=data)
        level_data = []
        for item in temp_data:
            if item != "":
                level_data.append(re.compile("[\d%]+").findall(item))
        combine_data = self.combine_data(string_data, level_data)
        result = {"Original": data}
        for i in range(len(combine_data)):
            result[f"level_{i+1}"] = combine_data[i]
        return result

    def combine_data(self, string_data, level_data):
        result = []
        level = max([len(item) for item in level_data])
        level_data_copy = level_data.copy()
        for item in level_data_copy:
            if len(item) < level:
                string_data[level_data.index(item)] = string_data[level_data.index(item)] + item[-1] + string_data[level_data.index(item)+1]
                string_data.pop(level_data.index(item)+1)
                level_data.pop(level_data.index(item))
        for i in range(len(level_data[0])):
            combined_string = ""
            for j in range(len(string_data) - 1):
                combined_string += string_data[j] + level_data[j][i]
            combined_string += string_data[-1]
            result.append(combined_string)
        return result


if __name__ == "__main__":
    from Config.Config import Crawl_Config
    config = Crawl_Config()
    data_updater = DataUpdater(config)
    data_updater.split_level_data("对选定的敌方单体造成自身攻击力290%/310%/340%的物理伤害，并使其进入震怒状态，效果持续2回合；同时使自身进入1层敏捷状态，并获得额外移动机会1次，该次额外移动的移动力减少2。")