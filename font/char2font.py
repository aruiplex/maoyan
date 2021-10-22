from fontTools.ttLib import TTFont
import math


class CharToNum():

    def __init__(self):
        # base font
        self.font_base = TTFont("./font/iconfont0.woff")
        for i in range(0, 10):
            self.font_base["glyf"][self.base_number_to_code(i)].coordinates = sorted(
                list(self.font_base["glyf"][self.base_number_to_code(i)].coordinates))

    def relative_distance(self, l0, l1):
        if abs(len(l0) - len(l1)) >= 4:
            return float("inf")
        dis = 0
        for i0, i1 in zip(l0, l1):
            dis += math.sqrt((i0[0]-i1[0])**2 + (i0[1]-i1[1])**2)
        return dis

    def base_number_to_code(self, x):
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

    def char2num(self, new_code):
        # fonts.saveXML("./iconfont0.xml")
        coordinates_new = sorted(
            list(self.font_new["glyf"][new_code].coordinates))
        one_hot = []
        for i in range(0, 10):
            coordinates_base = self.font_base["glyf"][self.base_number_to_code(
                i)].coordinates
            one_hot.append(self.relative_distance(
                coordinates_new, coordinates_base))

        return one_hot.index(min(one_hot))


c = CharToNum()
c.set_new_fonts("./font/iconfont1.woff")

print(c.char2num("uniE387"))
