#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb

cgitb.enable(format="text")
print "Content-Disposition: inline; filename=fractal.svg"
print "Content-Type: image/svg+xml;charset=utf-8"
print

import urllib
from svg import svg
import lsys
import cgi

arguments = cgi.FieldStorage()

angle = float(arguments['angle'].value)
iterations = int(arguments['iterations'].value)
constants = set(list(str(arguments['constants'].value).decode("hex")))
axiom = str(arguments['axiom'].value).decode("hex")
rules = str(arguments['rules'].value).decode("hex").split("\n")
rotate = float(arguments['rotate'].value)
thickness = str(arguments['thickness'].value)
border = 100
width = 820
bgcolor = "#404040"

subject = lsys.subject(axiom)
result = subject.replace([lsys.rule(rule) for rule in rules], iterations)
points, kinds = result.track(angle, constants, start_rotation=rotate)
points = points / points[:,0].max() * (width - border) + border/2
height = points[:,1].max() + border/2

image = svg(width, height, bg=bgcolor)
image.path(points, kinds, strokewidth=thickness)
print image

