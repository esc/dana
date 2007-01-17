#!/usr/bin/env python

import matplotlib.pylab as pylab
import matplotlib.colors as colors

import dana.core as core
import dana.cnft as cnft
import dana.sigmapi as sigmapi
import dana.sigmapi.projection as proj
import dana.sigmapi.projection.combination as combine

import dana.projection as projection
import dana.projection.distance as distance
import dana.projection.density as density
import dana.projection.shape as shape
import dana.projection.profile as profile

import dana.view as view

import time, random, math
import gobject, gtk


print "------------------------------------------------------------------------"
print "Sigmapi Test : Computation of the convolution product between two inputs"
print ""
print "Author:    Jeremy Fix"
print "Date:      13-12-2006"
print "------------------------------------------------------------------------"
print ""


# Create a new network
net = core.Network ()
width  = 40
height = width

# Create an Input map
Input = core.Map((width,height), (0,0))
Input.append(core.Layer())
Input[0].fill(core.Unit)
Input.name='Input'
net.append(Input)

# Create a second Input map

Input2 = core.Map((width,height), (0,2))
Input2.append(core.Layer())
Input2[0].fill(core.Unit)
Input2.name='Input2'
net.append(Input2)

# Create the output map with sigmapi units

Output = core.Map((width,height), (1,1))
Output.append(core.Layer())
Output[0].fill(sigmapi.Unit)
Output.name='Output'
Output.spec = cnft.Spec();
net.append(Output)

Output.spec.alpha = 7.0

## Define the connections

p          = projection.projection()
p.self     = True
p.distance = distance.euclidean(False)
p.density  = density.full(1)
p.shape    = shape.box(1,1)
p.profile  = profile.constant(1)
p.src      = Input[0]
p.dst      = Output[0]
p.connect()


p1 = proj.projection()
p1.combination = combine.linear(1,1,1,1,1,1,width/2.0,height/2.0,0.2)
p1.src1= Input[0]
p1.src2 = Input2[0]
p1.dst = Output[0]
p1.connect();

# Show network
netview = view.View (net)

manager = pylab.get_current_fig_manager()

def updatefig(*args):
    netview.update()
    return True

def clamp(map,x0,y0,r):
    for u in map[0]:
	u.potential = u.potential +math.exp(-float((u.position[0]-x0)*(u.position[0]-x0)+(u.position[1]-y0)*(u.position[1]-y0))/float(r*r))
    return True

def clear(map):
	for u in map[0]:
		u.potential = 0

is_run = 0
dtheta = math.pi/10.0
theta = 0.0
epochs = 20
is_init = 0

def step_init(nb):
	global is_init
	clear(Input)
	is_init = 1
	for i in range(nb):
		x0 = random.randint(0,width)
		y0 = random.randint(0,height)
		clamp(Input,x0,y0,4)
	
def step(radius,is_threaded):
	global is_init
	if(is_init==0):
		print "Don't forget to run step_init before running step"
	global dtheta,theta,epochs
	theta+= dtheta
	x1 = width/2.0+radius*math.cos(theta)
	y1 = height/2.0+radius*math.sin(theta)
	clear(Input2)
	clamp(Input2,x1,y1,4)
	net.evaluate(epochs,is_threaded)
	
def net_init(widget,data=None):
	step_init(4)	
	
def net_step(widget,data=None):
	step(width/4.0,False)

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_border_width(12)
vbox = gtk.VBox(True, 6)

init_button = gtk.Button("Init")
init_button.connect("clicked",net_init)
vbox.add(init_button)

step_button = gtk.Button("Step")
step_button.connect("clicked",net_step)
vbox.add(step_button)

window.add (vbox)
window.show_all()	
	
	
gobject.idle_add(updatefig)
pylab.show()


