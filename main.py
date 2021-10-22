import io
import math
import os
import pickle
import random
import re
import time
import json
import bs4
# import pandas as pd
import requests
from fontTools.ttLib import TTFont
from loguru import logger
from lxml import etree
from fontTools.pens.recordingPen import RecordingPen


class CharToNumDraw():

    def __init__(self):
        self.font_base_draw_list = []
        # base font
        self.font_base = TTFont("./font/iconfont0.woff")
        for i in range(0, 10):
            glyph = self.font_base.getGlyphSet()[self._base_number_to_code(i)]
            p = RecordingPen()
            glyph.draw(p)
            self.font_base_draw_list.append(set(p.value))

    def set_new_fonts(self, font_new_path):
        self.font_new = TTFont(font_new_path)
        logger.debug(f"font_keys: {self.font_new['glyf'].keys()}")

    def char2num(self, new_code: str):
        # fonts.saveXML("./iconfont0.xml")
        new_code = "uni" + \
            new_code.encode("unicode_escape").decode()[-4:].upper()
        glyph = self.font_new.getGlyphSet()[new_code]
        p = RecordingPen()
        glyph.draw(p)
        s = set(p.value)
        one_hot = []
        for i in self.font_base_draw_list:
            one_hot.append(
                len(
                    s.intersection(i)
                )
            )

        return one_hot.index(max(one_hot))

    def _base_number_to_code(self, x):
        return {
            1: "uniE83C",
            2: "uniEA5E",
            3: "uniF6D1",
            4: "uniF882",
            5: "uniE39D",
            6: "uniF139",
            7: "uniF223",
            8: "uniF7A6",
            9: "uniEBF7",
            0: "uniF1C0"
        }[x]


class CharToNum():
    """从猫眼官网上的font的char到数字。
    """

    def __init__(self):
        # base font
        self.font_base = TTFont("./font/iconfont0.woff")
        for i in range(0, 10):
            self.font_base["glyf"][self._base_number_to_code(i)].coordinates = sorted(
                list(self.font_base["glyf"][self._base_number_to_code(i)].coordinates))

    def _max_points_in_region(self, l, d):
        n = 0
        for dd in d:
            for ll in l:
                # Find the nearest point
                r = math.sqrt((dd[0]-ll[0])**2 + (dd[1]-ll[1])**2)
                if r <= 10:
                    n += 1
                    l.remove(ll)
                    break
        # Accuracy
        p = n / len(d)
        logger.debug(f"正确率：{p*100}%")
        return p

    def _relative_distance(self, l0, l1):
        """use every point distance to check number which is best

        Args:
            l0 (list): base font points list
            l1 (list): new font points list

        Returns:
            distance: \sigma every point distance
        """
        # TODO
        if abs(len(l0) - len(l1)) > 9:
            return float("inf")
        dis = 0
        for i0, i1 in zip(l0, l1):
            dis += math.sqrt((i0[0]-i1[0])**2 + (i0[1]-i1[1])**2)
        return dis

    def _base_number_to_code(self, x):
        return {
            1: "uniE83C",
            2: "uniEA5E",
            3: "uniF6D1",
            4: "uniF882",
            5: "uniE39D",
            6: "uniF139",
            7: "uniF223",
            8: "uniF7A6",
            9: "uniEBF7",
            0: "uniF1C0"
        }[x]

    def set_new_fonts(self, font_new_path):
        self.font_new = TTFont(font_new_path)
        logger.debug(f"font_keys: {self.font_new['glyf'].keys()}")

    def char2num(self, new_code: str):
        # fonts.saveXML("./iconfont0.xml")
        new_code = "uni" + \
            new_code.encode("unicode_escape").decode()[-4:].upper()
        coordinates_new = sorted(
            list(self.font_new["glyf"][new_code].coordinates))
        one_hot = []
        for i in range(0, 10):
            coordinates_base = self.font_base["glyf"][self._base_number_to_code(
                i)].coordinates
            one_hot.append(self._max_points_in_region(
                coordinates_new, coordinates_base))

        return one_hot.index(max(one_hot))


# c = CharToNum()
# c.set_new_fonts("./font/iconfont1.woff")
# print(c.char2num("uniE387"))

class Pa():
    s = requests.Session()
    s.headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Cookie": "__mta=220434983.1634193511952.1634450602151.1634450606007.51; uuid_n_v=v1; uuid=58BB89202CB911ECA55FB3CFA9262833BB3ECA70687D4F2B8EB54895C9C14E30; _csrf=8aa7cda1fbcecf89640e9400340425e65ab5feddcb835616893fbdacd2625110; _lxsdk_cuid=17c7d86155b1a-0934cb32140a51-1a2f1c08-1fa400-17c7d86155cc8; ci=55; featrues=[object Object]; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1634193512,1634359559; _lxsdk=58BB89202CB911ECA55FB3CFA9262833BB3ECA70687D4F2B8EB54895C9C14E30; __mta=174488221.1634360855530.1634363365024.1634368138083.3; _lx_utm=utm_source=google&utm_medium=organic; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1634450606; _lxsdk_s=17c8cd8f564-087-17e-c6d||7"
    }

    def req(self, url):
        r = self.s.request("GET", url=url)
        r.encoding = "utf-8"
        return r.text

    def req_raw(self, url):
        r = self.s.request("GET", url=url)
        r.encoding = "utf-8"
        return r.content


class Film:
    pa = Pa()
    char_to_num = CharToNum()

    def __init__(self, html: str):
        soup = bs4.BeautifulSoup(html, "html.parser")
        self.get_font(html)

        self.name_zh = soup.find_all("h1", class_="name")[0].contents[0]
        logger.info(f"{self.name_zh} is starting.")
        self.name_en = soup.find_all("div", class_="ename ellipsis")[
            0].contents[0]
        self.categorys = [category.contents[0].strip()
                          for category in soup.find_all("a", class_="text-link")]  # lambda?
        t = [i.strip() for i in soup.find_all(
            "li", class_="ellipsis")[1].contents[0].split("/")]
        self.area = t[0]
        self.duration = t[1]
        self.date = soup.find_all("li", class_="ellipsis")[2].contents[0]
        self.awards = [award.contents[1].contents[2].strip()
                       for award in soup("li", class_="award-item")]
        stuffs = [stuff.contents[0].strip()
                  for stuff in soup("a", class_="name")]
        self.director = stuffs[0]
        self.actors = stuffs[1:]
        spans = soup("span", class_="stonefont")
        rate_raw = spans[0].contents[0]
        money_unit = soup("span", class_="unit")[0].contents[0] if soup(
            "span", class_="unit") else 1
        self.rate = self._maoyan_formatter(rate_raw)
        rate_num_raw = spans[1].contents[0]
        self.rate_num = self._maoyan_formatter(rate_num_raw)
        if len(spans) == 3:
            money_raw = spans[2].contents[0]
            self.money = self._maoyan_formatter(money_raw, money_unit)
        else:
            self.money = -1

    def _maoyan_formatter(self, chars: bs4.element.NavigableString, money_unit=None):
        units_zh = {"万": 1e4, "亿": 1e8, "万美元": 63900.0}
        result = ""
        base = 1
        # to due with the money unit in the html
        if money_unit != None:
            base *= units_zh[money_unit]

        if chars[-1] in units_zh:
            base *= units_zh[chars[-1]]
            chars = chars[:-1]

        for char in chars:
            if char == ".":
                result += "."
                continue
            i = str(self.char_to_num.char2num(char))
            logger.debug("ans: ", i)
            result += i

        return float(result)*base

    def get_font(self, html):
        font_file = re.findall(
            r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', html)[0]
        font_url = 'https://vfile.meituan.net/colorstone/' + font_file
        logger.debug(f"font file is: {font_file}")
        font_bytes = self.pa.req_raw(font_url)
        font_fd = io.BytesIO(font_bytes)
        self.char_to_num.set_new_fonts(font_fd)


class MaoPiYan():
    path = "https://maoyan.com/board/4?offset="
    movie_prefix = "https://maoyan.com"
    pa = Pa()
    href_links = []
    moives = []

    def save(self):
        with open("./films.pk", "wb") as fd:
            pickle.dump(self, fd)

    def get_top_100_link(self):
        for offset in range(0, 100, 10):
            url = self.path + str(offset)
            txt = self.pa.req(url)
            # logger.info(f"contents in response: {c}")
            if "猫眼验证中心" in txt:
                # raise NeedForVerifyException("猫眼验证中心")
                logger.error("猫眼验证中心: need for verify code")
                break

            if "喵~好像哪里出错了唉.." in txt:
                logger.info("喵~好像哪里出错了唉..")
                break

            tree = etree.HTML(txt)
            for ctr in range(1, 11):
                el = tree.xpath(
                    f"//*[@id='app']/div/div/div[1]/dl/dd[{ctr}]/div/div/div[1]/p[1]/a")[0]
                href = el.attrib["href"]
                self.href_links.append(href)
                logger.info(f"{offset+ctr}, href: {href}")
            # small interval in every request
            self._wait()

        logger.info(f"All href links: {self.href_links}")
        with open("./top100_list", "w") as fd:
            fd.write(str(self.href_links))

    def _wait(self):
        logger.debug("...waiting...")
        time.sleep(random.uniform(10, 15))

    def get_top_100_name(self):
        for offset in range(0, 100, 10):
            url = self.path + str(offset)
            txt = self.pa.req(url)
            # logger.info(f"contents in response: {c}")
            if "猫眼验证中心" in txt:
                # raise NeedForVerifyException("猫眼验证中心")
                logger.error("猫眼验证中心: need for verify code")
                break

            if "喵~好像哪里出错了唉.." in txt:
                logger.info("喵~好像哪里出错了唉..")
                break

            tree = etree.HTML(txt)
            for ctr in range(1, 11):
                el = tree.xpath(
                    f"//*[@id='app']/div/div/div[1]/dl/dd[{ctr}]/div/div/div[1]/p[1]/a")[0]
                href = el.attrib["title"]
                self.href_links.append(href)
                logger.info(f"{offset+ctr}, href: {href}")
            # small interval in every request
            self._wait()

        logger.info(f"All href links: {self.href_links}")
        with open("./top100_list_name", "w") as fd:
            fd.write(str(self.href_links))

    def get_detail(self):
        for index, link in enumerate(self.href_links):
            req_path = self.movie_prefix + link
            html = self.pa.req(req_path)
            f = Film(html)
            # self.moives.append(f)
            logger.success(f"<{index}>name: {f.name_zh} finish!")
            c = json.dumps(f.__dict__, ensure_ascii=False)
            with open(f"./movies/{f.name_zh}.json", "w") as fd:
                fd.write(c)

            self._wait()


def link_seeker(m, ori_href_link):
    movies_num = len(os.listdir("./movies"))
    m.href_links = ori_href_link[movies_num+1:]


def never_gona_give_you_up(m: MaoPiYan, ori_href_link: list):
    link_seeker(m, ori_href_link)
    while True:
        try:
            m.get_detail()
        except IndexError as e:
            logger.error(e)
            link_seeker(m, ori_href_link)
            m._wait()


def main():
    logger.level("INFO")
    # try:
    m = MaoPiYan()
    # m.get_top_100_link()
    fd = open("./top100_list", "r")
    l = fd.read()
    ori_href_link = eval(l)
    m.href_links = ori_href_link
    fd.close()
    never_gona_give_you_up(m, ori_href_link)
    m.save()
    # except Exception as e:
    #     logger.warning(f"something err, saving {str(e)}")
    # m.save()


# main()
m = MaoPiYan()
# m.get_top_100_name()
l = ["/films/1203", "/films/615739"]
m.href_links = l
m.get_detail()