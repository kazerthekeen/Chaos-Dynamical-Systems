#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cobweb plot gotten primarily from https://scipython.com/blog/cobweb-plots/ 
and modified to work with my data set.

@author: kazer
"""
import math
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

# Use LaTeX throughout the figure for consistency
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 16})
rc('text', usetex=True)
# Figure dpi
dpi = 72


def colatz(ar):
    if type(ar) != type([]): # changes type so i can do route(num) 
        ar = [ar]            # instead of route([num]) for recursion purposes
    if ar[-1] in ar[:-1]:          # ar[-1] is newest value in my list, if its 1 im done.
        return ar
    if ar[-1]%2 == 0:       # Adds the next number in the sequence to the list
        ar.append(int(ar[-1]/2))
    else:
        ar.append(ar[-1]*5 + 1)
    return colatz(ar)        # recursivly call it to find the next number.


def newtons(f, df, ar, n=20):
    if type(ar) != type([]): # changes type so i can do route(num) 
        ar = [ar]   
    if len(ar) >= n:          # ar[-1] is newest value in my list, if its 1 im done.
        return ar
    x = ar[-1]
    xn = (-f(x)/df(x) + x)
    ar.append(xn)
    return newtons(f,df,ar)

def plot_cobweb(f, x0, name, iterations=20,  bound=[]):
    
    """Make a cobweb plot.

    Plot y = f(x) and y = x for 0 <= x <= 1, and illustrate the behaviour of
    iterating x = f(x) starting at x = x0.

    """
    nmax = iterations*2
    fig = plt.figure(figsize=(600/dpi, 450/dpi), dpi=dpi)
    ax = fig.add_subplot(111)


    # Iterate x = f(x) for nmax steps, starting at (x0, 0).
    px, py = np.empty((2,nmax+1,2))
    px[0], py[0] = x0, 0
    x = []
    for n in range(1, nmax, 2):
        x.append("{:.5} ".format(px[n-1][0]))
        px[n] = px[n-1]
        py[n] = f(px[n-1])
        px[n+1] = py[n]
        py[n+1] = py[n]
    
    if bound ==[]:
        m = np.amax(px)*1.2
        n = np.amin(px)*1.2
    else:
        n = bound[0]
        m = bound[1]
    r = np.linspace(n,m,100)
    
    if n < 0 < m:
        ax.plot(r,np.zeros((100)), c='#444444', lw=1)
        ax.plot(np.zeros((100)),r, c='#444444', lw=1)

    
    # Plot y = f(x) and y = x
    ax.plot(r, r, c='#777777', lw=2)
    ax.plot(r, f(r), c='#000000', lw=2)
            
    # Plot the path traced out by the iteration.
    ax.plot(px, py, c='b', alpha=0.7)
    

            
    # Annotate and tidy the plot.
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.5)
    ax.grid(which='major', alpha=0.5)
    ax.set_aspect('equal')
    
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(f.latex_label)
    ax.set_title(name)

    plt.savefig('cobweb_{:}.png'.format(name), dpi=dpi)
    # print(*x, sep=", ")

class AnnotatedFunction:
    """A small class representing a mathematical function.

    This class is callable so it acts like a Python function, but it also
    defines a string giving its latex representation.

    """

    def __init__(self, func, latex_label):
        self.func = func
        self.latex_label = latex_label

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

#Newtons        
#func = AnnotatedFunction(lambda x: x**2-2, '$x_{n+1} = 6/x_n -1$')
#df = AnnotatedFunction(lambda x: 2*x, '$x_{n+1} = 6/x_n -1$')
#
#print(newtons(func,df, 1.5))


