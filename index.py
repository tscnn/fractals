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
axiom = config.get(load, "axiom")
rules = config.get(load, "rules")
content = content.replace("{param_angle}", angle)
content = content.replace("{param_iterations}", iterations)
content = content.replace("{param_axiom}", axiom)
content = content.replace("{param_rules}", rules.replace(",","\n"))
angle = urllib.quote(angle)
iterations = urllib.quote(iterations)
axiom = urllib.quote(axiom)
rules = urllib.quote(rules)
image_src = "/generator.py?angle=%s&iterations=%s&axiom=%s&rules=%s" % (angle, iterations, axiom, rules)
content = content.replace("{image_src}", image_src)

f.close()

print content
