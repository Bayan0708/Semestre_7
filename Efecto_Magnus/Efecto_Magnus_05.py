from numpy import *
from matplotlib import*
from matplotlib.pyplot import *
from __future__ import division

Dimeter  = 0.067
r   = (Dimeter/2)         # radius of sphere (meters)
s        = 1.0         # spin in revolutions per second (positive is backspin)
p  = 1.225 # air density in kg/m^3
dragCoef = 0.5  # drag coefficient
m        =  0.0585        # mass of the ball in kilograms
g        = 9.82        # gravitational constant
dt       = 0.01
A        =  (pi*r**2)
Cd       = 0.5
Cl       = 1.5
v        = 30
t       = 0.470
n= (t/dt)

a = zeros(n)
v = zeros(n)
x = zeros(n)
Fg = zeros(n)
Fd = zeros(n)
t =  zeros(n)

v[0] = 0
x[0] = 0
i = 0

while i <= (n-2):
    Fg[i] = (m*g)
    Fd[i] = (.5*p*A*Cd*(v[i]**2)*sign(-v[i]))
    a[i] = ((Fg[i] + Fd[i]) / m)
    v[i+1] = (v[i] + a[i]*dt)
    x[i+1] = (x[i] +v[i]*dt +.5*a[i]*(dt**2))
    t[i+1] = (t[i] + dt)
    i = i+1


print ("My distance is",max(x)-min(x), "meters")
print ("At t=", argmax(x)/100, "s")
plot(x,label="position")
legend()