import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

def GRAPH(heightener, PointsX,PointsY):
    # make these smaller to increase the resolution
    dx, dy = 0.05, 0.05
    
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(-1, 1 + dy, dy),
                    slice(-1, 1 + dx, dx)]
    x.flatten()
    y.flatten()
    z = np.array([[heightener(x2**2,y2**2) for x2,y2 in zip(xi,yi)] for xi, yi in zip(x,y)])
    
    # x and y are bounds, so z should be the value *inside* those bounds.
    # Therefore, remove the last value from the z array.
    z = z[:-1, :-1]
    levels = MaxNLocator(nbins=15).tick_values(z.min(), z.max())
    
    
    # pick the desired colormap, sensible levels, and define a normalization
    # instance which takes data values and translates those into levels.
    cmap = plt.get_cmap('seismic')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    
    fig, (ax0) = plt.subplots(nrows=1)
    
    # contours are *point* based plots, so convert our bound into point
    # centers
    cf = ax0.contourf(x[:-1, :-1] + dx/2.,
                      y[:-1, :-1] + dy/2., z, levels=levels,
                      cmap=cmap)
    #fig.colorbar(cf, ax=ax0)
    #ax0.set_title('contourf with levels')
    
    # adjust spacing between subplots so `ax1` title and `ax0` tick labels
    # don't overlap
    #fig.tight_layout()
    plt.plot(PointsX[0],PointsX[1],PointsX[2])
    plt.plot(PointsY[0],PointsY[1],PointsY[2])