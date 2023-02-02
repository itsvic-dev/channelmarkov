import logging
import requests
from html.parser import HTMLParser

class InvidiousVideosParser(HTMLParser):
    logger = logging.getLogger("InvidiousVideosParser")

    def __init__(self):
        super().__init__()
        self.__has_video = False
        self.__has_title = False
        self.__has_next_page = False
        self.__has_footer = False
        self.titles = []
        self.next_page: str = None

    def handle_starttag(self, tag, attrs):
        if tag == 'head':
            self.logger.debug('new page being fed, resetting')
            self.__has_video = False
            self.__has_title = False
            self.__has_next_page = False
            self.__has_footer = False
            self.next_page = None
        if tag == 'a':
            if not self.__has_video:  # look for video start
                for attr in attrs:
                    if attr[0] == 'href' and attr[1].startswith('/watch') and not attr[1].endswith('&listen=1'):
                        self.__has_video = True
                        self.logger.debug("found video tag: %s", attr[1])
            if self.__has_next_page and not self.__has_footer:  # look for next page a
                self.next_page = attrs[0][1]
                self.logger.debug("found next page: %s", self.next_page)
        elif tag == 'p' and self.__has_video:  # look for video title
            if attrs[0][1] == 'auto':
                self.__has_title = True
                self.logger.debug("found title tag")
        elif tag == 'div':  # look for next page div (<div class="pure-u-1 pure-u-lg-1-5" style="text-align:right">)
            if len(attrs) == 2:
                if attrs[0] == ('class', 'pure-u-1 pure-u-lg-1-5') and attrs[1] == ('style', 'text-align:right'):
                    self.logger.debug("found next page div")
                    self.__has_next_page = True
        elif tag == 'footer':
            self.__has_footer = True
    
    def handle_data(self, data):
        if self.__has_title:
            self.logger.debug("title: %s", data)
            self.titles.append(data)
            self.__has_title = False

    def handle_endtag(self, tag):
        if tag == 'a':
            self.__has_video = False
            self.__has_next_page = False
        if tag == 'p':
            self.__has_title = False
        if tag == 'footer':
            self.__has_footer = False

def __parse_page(page, instance, parser):
    logging.debug("getting page: %s", page)
    # get page
    resp = requests.get(f"{instance}{page}")
    parser.feed(resp.content.decode())
    if parser.next_page:
        __parse_page(parser.next_page, instance, parser)
    return parser.titles

def parse_c(c: str, instance = "https://inv.omame.xyz"):
    return __parse_page(f"/c/{c}", instance, InvidiousVideosParser())

def parse_channel(channel: str, instance = "https://inv.omame.xyz"):
    return __parse_page(f"/channel/{channel}", instance, InvidiousVideosParser())

def parse_user(user: str, instance = "https://inv.omame.xyz"):
    return __parse_page(f"/user/{user}", instance, InvidiousVideosParser())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("test parse c: FlyTechVideos and Endermanch")
    print(parse_c("FlyTechVideos"))
    print(parse_c("Endermanch"))
