import requests;

class WebSpider(object):
    def __init__(self):
        self.url = 'https://bbs-api.mihoyo.com/post/wapi/getForumPostList?forum_id=49'

        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/92.0.4515.107 Safari/537.36'
    }

    def parse(self):
        img_dict_data = {}


if __name__ == '__main__':
    self = WebSpider()
    proxies = {"http": None, "https": None}
    res = requests.get(self.url, headers=self.headers, verify=False, proxies=proxies).content.decode('utf-8')