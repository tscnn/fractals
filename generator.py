#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb

cgitb.enable(format="text")
print "Content-Type: image/svg+xml;charset=utf-8"
print

import cgi
import urllib
from svg import svg
import lsys

def decode(s):
    s = urllib.unquote(s)
    s = s.replace("><", "+")
    return s

arguments = cgi.FieldStorage()

angle = float(decode(arguments['angle'].value))
iterations = int(decode(arguments['iterations'].value))
axiom = decode(arguments['axiom'].value)
rules = decode(arguments['rules'].value).split(",")
border = 20
width = 820
bgcolor = "#404040"

subject = lsys.subject(axiom)
result = subject.replace([lsys.rule(rule) for rule in rules], iterations)
points, kinds = result.track(angle)
points = points / points[:,0].max() * (width - border) + border/2
height = points[:,1].max() + border/2

image = svg(width, height, bg=bgcolor)
image.path(points, kinds)
print image

