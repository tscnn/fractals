#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb

cgitb.enable()
print "Content-Type: text/html;charset=utf-8"
print

from ConfigParser import ConfigParser
import cgi
import urllib
import random

arguments = cgi.FieldStorage()

config = ConfigParser()
config.read("examples.ini")

examples_contents = []
for section in config.sections():
    link = "/?load=%s" % urllib.quote_plus(section)
    name = section
    image = config.get(section, "image")
    examples_contents.append((
        "<li>"
        "<a href='%s'>%s<br /><img src='%s' width='110' height='80' /></a>"
        "</li>\n" % (link, name, image)))

f = open("index.html", "r")
content = f.read()
content = content.replace("{examples_content}", "".join(examples_contents))

if arguments.has_key("load"):
    load = urllib.unquote_plus(arguments['load'].value)
else:
    load = random.choice(config.sections())

angle = config.get(load, "angle")
iterations = config.get(load, "iterations")
constants = config.get(load, "constants")
axiom = config.get(load, "axiom")
rules = config.get(load, "rules").replace(",","\n")
rotate = config.get(load, "rotate") if config.has_option(load, "rotate") else "0"
thickness = config.get(load, "thickness") if config.has_option(load, "thickness") else "1"
content = content.replace("{param_angle}", angle)
content = content.replace("{param_iterations}", iterations)
content = content.replace("{param_constants}", constants)
content = content.replace("{param_axiom}", axiom)
content = content.replace("{param_rules}", rules)
content = content.replace("{param_rotate}", rotate)
content = content.replace("{param_thickness}", thickness)
constants = constants.encode("hex")
axiom = axiom.encode("hex")
rules = rules.encode("hex")
image_src = "/generator.py?angle=%s&iterations=%s&constants=%s&axiom=%s&rules=%s&rotate=%s&thickness=%s" % (angle, iterations, constants, axiom, rules, rotate, thickness)
content = content.replace("{image_src}", image_src)

f.close()

print content
