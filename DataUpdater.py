from Config.Config import Crawl_Config
from Utils.DataCrawler import DataUpdater
from Utils.DataHelper import DataHelper


def main():
    config = Crawl_Config()
    data_updater = DataUpdater(config)
    data_updater.get_器者_urls_list()
    data_updater.get_器者_data()
    data = data_updater.器者_data
    DataHelper.save_to_sqlite(data, "./Data/器者.db")


if __name__ == "__main__":
    main()
