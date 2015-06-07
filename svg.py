
MOVE = 0
LINE = 1

class svg:
    def __init__(self, width, height, bg=None):
        self.__header = (
             '<?xml version="1.0" encoding="UTF-8"?>\n'
             '<svg xmlns="http://www.w3.org/2000/svg"'
             ' xmlns:xlink="http://www.w3.org/1999/xlink"'
             ' xmlns:ev="http://www.w3.org/2001/xml-events"'
             ' version="1.1"'
             ' baseProfile="full"'
             ' width="%s" height="%s">\n') % (width, height)
        self.__defs = "<defs>\n"
        self.__body = ""
        if bg != None:
            self.add('<rect fill="%s" x="0" y="0" width="%s" height="%s" />' % (bg, width, height))
    
    def adddef(self, s):
        self.__defs += "%s\n" % s
    
    def path(self, points, kinds, fill="none", stroke='#009EE0', strokewidth='1', strokelinecap='round', strokelinejoin='bevel', style=''):
        d = " ".join(["%s%s %s" % (kinds[i], points[i][0], points[i][1]) for i in xrange(len(points))])
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
