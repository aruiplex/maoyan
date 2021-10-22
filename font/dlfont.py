import re
import requests

f = open("./detail.html", "r")
c = f.read()

font_file = re.findall(
    r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', c)[0]
font_url = 'https://vfile.meituan.net/colorstone/' + font_file

new_file = requests.get(font_url)
with open('./font/' + font_file, 'wb') as f:
    f.write(new_file.content)
