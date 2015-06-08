import sys
import math
import numpy as np
import lsys
from svg import svg

def dragon(iterations):
    axiom = lsys.subject('FX')
    route = axiom.replace([lsys.rule('X=>X+YF'), lsys.rule('Y=>FX-Y')], iterations)
    return route.track(90)

def doubledragon(iterations):
    axiom = lsys.subject('FX+FX+')
    route = axiom.replace([lsys.rule('X=>X+YF'), lsys.rule('Y=>FX-Y')], iterations)
    return route.track(90)

def cesaro(iterations, c=1.0, p=0.3):
    """ see also: http://michael.szell.net/fba/kapitel2.html """
    q = c-p
    h = math.sqrt(p*q)
    axiom = lsys.subject('F(1)')
    route = axiom.replace([lsys.rule('F(x)=>F(x*%s)+F(x*%s)--F(x*%s)+F(x*%s)' % (p,h,h,q))], iterations)
    return route.track(86)

def gosper(iterations):
    axiom = lsys.subject('A')
    route = axiom.replace([lsys.rule('A=>A-B--B+A++AA+B-'), lsys.rule('B=>+A-BB--B-A++A+B')], iterations)
    route = route.replace([lsys.rule('A=>F'), lsys.rule('B=>F')])
    return route.track(60)

def hilbert(iterations):
    axiom = lsys.subject('X')
    route = axiom.replace([lsys.rule('X=>-YF+XFX+FY-'), lsys.rule('Y=>+XF-YFY-FX+')], iterations)
    return route.track(90)

def koch(iterations):
    axiom = lsys.subject('F--F--F')
    route = axiom.replace([lsys.rule('F=>F+F--F+F')], iterations)
    return route.track(60)

def sierpinsky1(iterations):
    axiom = lsys.subject('++L')
    route = axiom.replace([lsys.rule('R=>-L+R+L-'), lsys.rule('L=>+R-L-R+')], iterations)
    route = route.replace([lsys.rule('R=>F'), lsys.rule('L=>F')])
    return route.track(60)

def plant1(iterations):
    axiom = lsys.subject('X')
    route = axiom.replace([lsys.rule('X=>F-[[X]+X]+F[+FX]-X'), lsys.rule('F=>FF')], iterations)
    return route.track(22.5)

def tosvg(path, filename, width=500, border=80, color="white", bgcolor="black", linewidth=1):
    points, kinds = path
    points = points / points.max() * width + border/2
    kinds = ['M' if k == lsys.MOVE else 'L' for k in kinds]
    img = svg(points[:,0].max() + border/2, points[:,1].max() + border/2, bgcolor)
    img.path(points, kinds, stroke=color, strokewidth=linewidth)
    img.save(filename)

def svg_double_dragon(iterations, filename, stepsize=5, border=80, color1="#4479ff", color2="#5cc455", bgcolor=None):
    points = track(doubledragon(iterations)) * stepsize + border/2
    points1 = points[:points.shape[0]/2]
    points2 = points[points.shape[0]/2:]
    width = points[:,0].max() + border/2
    height = points[:,1].max() + border/2
    img = svg(width, height, bgcolor)
    img.path(points1, stroke=color1)
    img.path(points2, stroke=color2)
    img.save(filename)
