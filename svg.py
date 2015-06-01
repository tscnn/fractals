

class svg:
    def __init__(self, width, height, bg=None):
        self.__width = width
        self.__height = height
        self.__header = ("<?xml version='1.0' encoding='utf-8' ?>\n"
                         "<svg width='%spx' height='%spx' version='1.2'>\n") % (width, height)
        self.__defs = "<defs>\n"
        self.__body = ""
        if bg != None:
            self.add("<rect fill='%s' x='0' y='0' width='%spx' height='%spx' />" % (bg, width, height))
    
    def adddef(self, s):
        self.__defs += "%s\n" % s
    
    def path(self, points, fill="none", stroke='#009EE0', strokewidth='1', strokelinecap='round', strokelinejoin='bevel', style=''):
        d = "".join(["%s%s %s " % ("M" if m==0 else "L",x,y) for x,y,m in points])
        self.add(("<path "
                  "fill='%s' "
                  "stroke='%s' "
                  "stroke-width='%s' "
                  "stroke-linecap='%s' "
                  "stroke-linejoin='%s' "
                  "style='%s' "
                  "d='%s' />") % (fill, stroke, strokewidth, strokelinecap, strokelinejoin, style, d))
    
    def add(self,s):
        self.__body += "%s\n" % s
    
    def save(self, filename):
        f = open(filename,"w")
        f.write(self.__header)
        f.write(self.__defs)
        f.write("</defs>\n")
        f.write(self.__body)
        f.write("</svg>\n")
        f.close()
