import os
import numpy as np
from scipy import ndimage 
from libtiff import TIFF 
from .utils.io import *
from .utils.preprocessing import *
from .utils.backtrack import *
from .utils.rendering3 import *

from matplotlib import pyplot as plt


def plotswc(swc, ax):
    ids = [node[0] for node in swc]
    for node in swc:
        # draw a line between this node and its parents when its parent exists 
        if node[6] in ids:
            parent = next(parent for parent in swc if node[6] == parent[0])
            ax.plot([node[3], parent[3]], [node[2], parent[2]], [node[4], parent[4]])


def plot_grad_on_swc(ax, nodes, gradinterp, sampling=0.2):
    randnodeidx = np.random.permutation(np.arange(len(nodes)))
    randnodeidx = randnodeidx[:np.floor(len(randnodeidx) * sampling)]
    nodes = nodes[randnodeidx.astype('int16')]
    dx = gradinterp[0](nodes)
    dy = gradinterp[1](nodes)
    dz = gradinterp[2](nodes)
    ax.quiver([n[0] for n in nodes], [n[1] for n in nodes], [n[2] for n in nodes], dx, dy, dz, length=3.0)


def trace(filepath, **userconfig):
    '''Trace the 3d tif with a single neuron using Rivulet algorithm'''
    config = {'length':5, 'coverage':0.98, 'threshold':0, 'render':False}
    config.update(userconfig)

    print('== Preprocessing')
    dt, t, ginterp, bimg, cropregion = rivulet_preprocessing(filepath, config)
    dtmax = dt.max()
    maxdpt = np.asarray(np.unravel_index(dt.argmax(), dt.shape))

    tt = t.copy()
    tt[bimg <= 0] = -2
    bb = np.zeros(shape=tt.shape) # For making a large tube to contain the last traced branch

    bounds = dt.shape
    viewer = Viewer3(800, 800, 800)
    viewer.set_bounds(0, bounds[0], 0, bounds[1], 0, bounds[2])

    idx = np.where(bimg > 0)

    # Start tracing loop
    nforeground = bimg.sum()
    covermap = np.zeros(bimg.shape) 
    converage = 0.0

    while converage < config['coverage']:
        converage = np.logical_and(tt==-1, bimg > 0).sum() / nforeground
        print('Tracing ', converage*100, '%%', end='\r')

        # Find the geodesic furthest point on foreground time-crossing-map
        endpt = srcpt = np.asarray(np.unravel_index(tt.argmax(), tt.shape)).astype('float64')

        # Trace it back to maxd 
        path = [srcpt,]
        while np.linalg.norm(maxdpt - endpt) > dtmax:
            try:
                endpt = rk4(srcpt, ginterp, t, 1)
                endptint = np.floor(endpt)
                if not inbound(endpt, tt.shape) or tt[endptint[0], endptint[1], endptint[2]] == -1: break;
            except ValueError:
                break

            path.append(endpt)

            # Render the line segment
            l = Line3(srcpt, endpt)
            l.set_color(1., 0., 0)
            viewer.add_geom(l)
            viewer.render(return_rgb_array=False)

            srcpt = endpt

            if len(path) >= 30 and np.linalg.norm(path[-30] - endpt) <= 1:
                break;

        # Erase it from the timemap
        for node in path:
            n = [math.floor(n) for n in node]
            r = getradius(bimg, n[0], n[1], n[2])
            r = r - 1
            r *= 1.5 # To make sure all the foreground voxels are included in bb
            bb[n[0]-r:n[0]+r+1, n[1]-r:n[1]+r+1, n[2]-r:n[2]+r+1] = 1

        startidx = [math.floor(p) for p in path[0]]
        endidx = [math.floor(p) for p in path[0]]
        tt[ tt[startidx[0], startidx[1], startidx[2]] <= tt <= tt[startidx[0], startidx[1], startidx[2]] and bb == 1] = -1

        if len(path) < config['length']:
            continue

        #TODO: Connect it to tree


if __name__ == '__main__':
    trace('tests/test.tif', threshold=0, render=True, length=8)
