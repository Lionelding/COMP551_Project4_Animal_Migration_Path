'''interpolation'''
from __future__ import print_function

import numpy as np
import sys
import numpy as np

def interpolate(p1, p2, time):
    '''given two points (lat1, lon1, time1), (lat2, lon2, time2) and a time
    return the lat, lon interpolation between the points for the time'''
    lat1, lon1, t1 = p1
    lat2, lon2, t2 = p2
    if time == t1:
        return lat1, lon1
    elif time == t2:
        return lat2, lon2
    time_difference = t2 - t1
    t = time - t1
    time_ratio = t / time_difference
    new_lat = lat1 + (lat2 - lat1) * time_ratio
    new_lon = lon1 + (lon2 - lon1) * time_ratio
    return new_lat, new_lon

def get_sandwich_points(ts, time):
    '''returns index of point with time just after (or equal to) the given time'''
    if time < ts[0][2] or time > ts[len(ts) - 1][2]:
        return -1
    prev = ts[0]
    for i in range(1, len(ts)):
        curr = ts[i]
        if prev[2] <= time and curr[2] >= time:
            return i
        prev = curr
    # should never make it here
    return -1

def interpolate_ts(ts, times):
    '''given a timeseries and a sequence of times, interpolate for each time'''
    new_ts = []
    for time in times:
        next_idx = get_sandwich_points(ts, time)
        lat, lon = interpolate(ts[next_idx-1], ts[next_idx], time)
        new_ts.append([lat, lon, time])
    return new_ts

def interpolate_tss(tss, times):
    new_tss = []
    for ts in tss:
        new_tss.append(interpolate_ts(ts, times))
    return new_tss

def get_time_limits(tss):
    '''given a list of time series, find the latest start time and earliest end time'''
    latest_st = 0
    earliest_et = sys.maxint
    for ts in tss:
        if ts[0][2] > latest_st:
            latest_st = ts[0][2]
        if ts[len(ts)-1][2] < earliest_et:
            earliest_et = ts[len(ts)-1][2]
    return latest_st, earliest_et

'''
def get_start_and_end_indices(ts, start_time, end_time):
    start = -1
    end = -1
    for i, (_, _, time) in enumerate(ts):
        if time == start_time:
            start = i
        if time == end_time:
            end == i
            break
    return start, end

def truncate_time_series(tss, start, end):
    #given a list of time series, truncate them based on latest start time and earliest end time
    print(tss)
    new_tss = []
    for ts in tss:
        start_idx, end_idx = get_start_and_end_indices(ts, start, end)
        if start_idx == -1 or end_idx == -1:
            print('Could not a datapoint for the given start and end times. Something is wrong')
            sys.exit(1)
        new_tss.append(ts[start_idx:end_idx+1])
    return new_tss
'''

def get_all_times_in_window(tss, start, end):
    '''return all the times, in order, between start and end for all time series'''
    times = set()
    for ts in tss:
        for _, _, time in ts:
            if time >= start and time <= end:
                times.add(time)
    times = list(times)
    times.sort()
    return times

def normalize_time_series(tss):
    # determine the latest start time and the earliest stop time
    start, end = get_time_limits(tss)
    print('Latest start time:')
    print(start)
    print('Earliest end time:')
    print(end)

    # determine all the times within this window across all time series
    common_times = get_all_times_in_window(tss, start, end)

    # replace each time series with its interpolations for each of the times in this window
    new_tss = interpolate_tss(tss, common_times)
    new_tss = np.array(new_tss)

    print('Shape of normalized time series:')
    print(new_tss.shape)

    return new_tss

'''
if __name__ == '__main__':
    tss = [[[1.,1.,1.], [2.,2.,2.], [2.3, 2.3, 2.8], [3.,3.,3.], [4.,4.,4.]],[[1.25, 1.25, 1.1], [1.5, 1.5, 1.5], [2.5,2.5,2.5], [3.5,3.5,3.5], [4.5,4.5,4.5]]]
    print(tss[0])
    print(tss[1])
    new_tss = normalize_time_series(tss)

    print(new_tss)
'''
