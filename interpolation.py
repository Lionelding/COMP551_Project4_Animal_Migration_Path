'''interpolation'''

import numpy as np

# need to convert times to timestamps
# then can interpolate

# given two points (lat1, lon1, time1), (lat2, lon2, time2) and a time
# return the lat, lon interpolation between the points for the time
def interpolate(p1, p2, time):
    lat1, lon1, t1 = p1
    lat2, lon2, t2 = p2
    time_difference = t2 - t1
    t = time - t1
    time_ratio = t / time_difference
    return (lat1, lon1) + ((lat2, lon2) - (lat1, lon1)) * time_ratio

# method to find two points sandwiching a time
def get_sandwich_points(ts, time):
    '''returns index of point with time just after the given time'''
    if time < ts[0][2] or time > ts[len(ts) - 1][2]:
        return -1
    prev = ts[0]
    for i in range(1, len(ts)):
        curr = ts[1]
        if prev[2] <= time and curr[2] >= time:
            return i
        prev = curr
    # should never make it here
    return -1

# given a timeseries and a sequence of times, interpolate for each time
def extend_ts(ts, time_set, times):
    '''time_set is a hashset of times this time series already has'''
    for time in times:
        if time not in time_set:
            next_idx = get_sandwich_points(ts, time)
            lat, lon = interpolate(ts[next_idx-1], ts[next_idx], time)
            ts.insert(next_idx, [lat, lon, time])

# TODO
# determine the latest start time and the earliest stop time
# for each series, remove points that lie outside this window
# determine all the times within this window across all timeseries
# for each time in this window, if a time series does not already have a measurement at
#   this time, then interpolate one and add it to the time series

# given a list of time series, find the latest start time and earliest end time
def get_time_limits(tss):
    pass
    # TODO


# given a list of time series, truncate them based on latest start time and earliest end time
def trucate_time_series(tss):
    start, end = get_time_limits(tss)
    # TODO
