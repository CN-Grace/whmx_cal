

class Crawl_Config:
    def __init__(self):
        self.root_url = "https://wiki.biligame.com/"
        self.器者_list_url = self.root_url + "whmx/器者图鉴"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.headers = {
            "User-Agent": self.user_agent
        }
        self.parser = "lxml"
        self.encoding = "utf-8"
