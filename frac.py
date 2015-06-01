import sys
from svg import svg
import numpy as np
from random import randint

def rotation_matrix(angle):
    alpha = np.radians(angle)
    return np.matrix([[np.cos(alpha), -np.sin(alpha)],
                      [np.sin(alpha),  np.cos(alpha)]])

def track(route, angle, startdelta=[[0],[1]]):
    #track that route and notice the coordinates
    N = route.count('F') + route.count(']') + 1
    R = rotation_matrix(angle)
    location = np.matrix([[0], [0]], dtype=float)
    delta = np.matrix(startdelta, dtype=float)
    points = np.zeros((N,3), dtype=float)
    points[0,0] = 0 #x coordinate
    points[0,1] = 0 #y coordinate
    points[0,2] = 0 #drawing mode; 0=move, 1=line
    stack = list()
    i = 1
    for turn in route:
        if turn == '+':
            #turn right
            delta = R * delta
        elif turn == '-':
            #turn left
            delta = np.linalg.inv(R) * delta
        elif turn == 'F':
            #move forward
            location += delta
            points[i,0:2] = location.reshape(2)
            points[i,2] = 1
            i += 1
        elif turn == '[':
            #fork
            stack.append((np.copy(location),np.copy(delta)))
        elif turn == ']':
            #go back to last junction
            location, delta = stack.pop()
            points[i,0:2] = location.reshape(2)
            points[i,2] = 0
            i += 1
    points[:,0] -= points[:,0].min()
    points[:,1] -= points[:,1].min()
    return points

def dragon(iterations):
    #generate the route of the dragon curve
    route = 'FX'
    for i in xrange(iterations):
        route = route.replace('X','X+yF')
        route = route.replace('Y','FX-Y')
        route = route.replace('y','Y')
    return track(route, 90)

def doubledragon(iterations):
    #generate the route of the dragon curve
    route = 'FX+FX+'
    for i in xrange(iterations):
        route = route.replace('X','X+yF')
        route = route.replace('Y','FX-Y')
        route = route.replace('y','Y')
    return track(route, 90)

def gosper(iterations):
    #generate the route of the gosper curve
    route = 'A'
    for i in xrange(iterations):
        route = route.replace('A','A-b--b+A++AA+b-')
        route = route.replace('B','+A-BB--B-A++A+B')
        route = route.replace('b','B')
    route = route.replace('A','F')
    route = route.replace('B','F')
    return track(route, 60)

def hilbert(iterations):
    #generate the route of the gosper curve
    route = 'X'
    for i in xrange(iterations):
        route = route.replace('X','-yF+XFX+Fy-')
        route = route.replace('Y','+XF-YFY-FX+')
        route = route.replace('y','Y')
    return track(route, 90)

def koch(iterations):
    #generate the route of the gosper curve
    route = 'F--F--F'
    for i in xrange(iterations):
        route = route.replace('F','F+F--F+F')
    return track(route, 60)

def sierpinsky1(iterations):
    #generate the route of the gosper curve
    route = '++L'
    for i in xrange(iterations):
        route = route.replace('R','-l+R+l-')
        route = route.replace('L','+R-L-R+')
        route = route.replace('l','L')
    route = route.replace('R','F')
    route = route.replace('L','F')
    return track(route, 60)

def plant1(iterations):
    #generate the route of the gosper curve
    route = 'X'
    for i in xrange(iterations):
        route = route.replace('X','f-[[X]+X]+f[+fX]-X')
        route = route.replace('F','FF')
        route = route.replace('f','F')
    return track(route, 22.5, startdelta=[[0],[-1]])

def tosvg(fractal, iterations, filename, stepsize=5, border=80, color="white", bgcolor="black"):
    points = fractal(iterations) * stepsize + border/2
    img = svg(points[:,0].max() + border/2, points[:,1].max() + border/2, bgcolor)
    img.path(points, stroke=color)
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
