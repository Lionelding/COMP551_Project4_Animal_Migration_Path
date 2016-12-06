'''utils'''

import numpy as np
import matplotlib.pylab as plt

################################################################################
# plotting
################################################################################

# to plot with matplotlib, we need to pass all x (lat) as one list and all y (lon) as another
# but while running dtw, we have x and y as pairs (with t as well) --> all in the form (x, y, t)
# the below funcs help us to convert lists in form [(x1, y1, ...), (x2, y2, ...), ...] into form (x1, x2, ...), (y1, y2, ...)

class Plottable(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

def make_plottable(ts, x_idx=0, y_idx=10):
    x, y = [pt[x_idx] for pt in ts], [pt[y_idx] for pt in ts]
    return Plottable(x, y)

def make_all_plottable(tss, x_idx=0, y_idx=1):
    ptss = []
    for ts in tss:
        ptss.append(make_plottable(ts, x_idx, y_idx))
    return ptss

def plot_series(ss, x_idx=0, y_idx=1, variable_length=False):
    if not variable_length and not hasattr(ss, 'shape'):
        ss = np.array(ss)
    if variable_length or len(ss.shape) == 3:
        plottables = make_all_plottable(ss, x_idx, y_idx)
    else:
        plottables = [make_plottable(ss, x_idx, y_idx)]
    for plble in plottables:
        plt.plot(plble.x, plble.y)
    plt.show()

################################################################################
# extract just lat and lon coordinates from time series
################################################################################

def extract_lat_and_lon(tss):
    ptss = []
    for pts in tss:
        ptss.append([pt[:2] for pt in pts])
    return np.array(ptss)
