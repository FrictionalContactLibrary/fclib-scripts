#!/usr/bin/env python
from math import cos, sin, pi
from numpy.linalg import norm
from siconos.mechanics.collision.bullet import btQuaternion
from siconos.mechanics.collision.bullet import __mul__ as mul
from random import random
from math import cos, sin, pi


theta1 = pi / 2
a1 = 1
b1 = 0
c1 = 0
n1 = sin(theta1 / 2) / norm((a1, b1, c1))

r1 = btQuaternion(a1 * n1, b1 * n1, c1 * n1, cos(theta1 / 2))


def s_v(v):
    return ' '.join('{0}'.format(iv) for iv in v)

alpha = pi / 2.
scale = 0.001
with open('input.dat', 'w') as f:
    # ground
    a = 0
    b = 1
    c = 0
    n = sin(pi / 4.) / norm((a, b, c))
    r = btQuaternion(a*n, b*n, c*n, cos(pi/4.))
    r.normalize()
    q = (0, 0, -.5*scale)
    o = (r.w(), r.x(), r.y(), r.z())
    
    f.write('3 -3 1 {0} {1} 0 0 0 0 0 0\n'.format(s_v(q),s_v(o)))
    
    #f.write('2 -2 0 0  0 -.5 cos(pi/4.) 0 cos(pi/4.) 0 0 0 0 0 0 0\n')

    for k in range(0,1):

        for i in range(0,4):

            theta = i * alpha
            a = 0
            b = 0
            c = 1
            n = sin(theta / 2) / norm((a, b, c))

            r = btQuaternion(a*n, b*n, c*n, cos(theta/2))
            r = mul(r, r1)

            r.normalize()

            q = (20.*cos(i*alpha)*scale, 20.*sin(i*alpha)*scale, (2.5 * k + 5)*scale)
            o = (r.w(), r.x(), r.y(), r.z())

            f.write('2 -2 1 {0} {1} 0 0 0 0 0 0\n'.format(s_v(q),s_v(o)))




    radius = 0.9 *scale
    density= 1000
    volume = 4./3.*pi* radius**3
    mass= volume*density
    print('mass', mass)
    inertia = 2/5. * mass * radius**2
    print('inertia', inertia)
    for x in range(0,10):
        for y in range(0,10):
            for i in range(0,2):

                theta = 0
                a = 0
                b = 0
                c = 1
                n = sin(theta / 2) / norm((a, b, c))
             
                q1 = ((10-2*x+random()/10.)*scale, (10-2*y+random()/10.)*scale, (2*i + 5)*scale)
                
                r = btQuaternion(a * n, b * n, c * n, cos(theta / 2))
                r = mul(r, r1)
                r.normalize()

                o = (r.w(), r.x(), r.y(), r.z())
                v1 = (0, 0, 0, 0, 0, 0)

                f.write('0 0 {0} {1} {2} {3}\n'.format(mass, s_v(q1), s_v(o), s_v(v1)))
