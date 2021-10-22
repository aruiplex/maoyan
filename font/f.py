from fontTools.ttLib import TTFont

fonts = TTFont("./iconfont0.woff")
fonts.saveXML("./iconfont0.xml")
