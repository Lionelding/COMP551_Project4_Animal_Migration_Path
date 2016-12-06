'''interpolation'''
from __future__ import print_function

import numpy as np
import sys
import time
import datetime

from preprocess import downsample_all
from preprocess import RelativeDate

from constants import SECS_PER_DAY

# Now, we have a bunch of points within a given time frame
# We need to fucking interpolate at a constant interval
# For example, say we are given points that spread a range of 1 year.
# Then we might want a point each day.

def interpolate(p1, p2, time):
    '''given two points (lat1, lon1, time1), (lat2, lon2, time2) and a time
    return the lat, lon interpolation between the points for the time'''
    lon1, lat1, t1 = p1
    lon2, lat2, t2 = p2
    if time == t1:
        return lon1, lat1
    elif time == t2:
        return lon2, lat2
    time_difference = t2 - t1
    t = time - t1
    time_ratio = t / time_difference
    new_lat = lat1 + (lat2 - lat1) * time_ratio
    new_lon = lon1 + (lon2 - lon1) * time_ratio
    return new_lon, new_lat

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

def get_closest_position(ts, t):
    '''returns the lat, lon at a time in the time series closest to time t
    will only ever be called for times t outside the range of the time series,
    so we will return either the first point or the last in the series'''
    if t < ts[0][2]:
        return ts[0][0], ts[0][1]
    else:
        return ts[-1][0], ts[-1][1]

def interpolate_ts(ts, times):
    '''given a timeseries and a sequence of times, interpolate for each time'''
    new_ts = []
    for time in times:
        next_idx = get_sandwich_points(ts, time)
        if next_idx == -1:
            # extrapolate to the closest point
            lon, lat = get_closest_position(ts, time)
        else:
            lon, lat = interpolate(ts[next_idx-1], ts[next_idx], time)
        new_ts.append([lon, lat, time])
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

def get_months(secs):
    return secs / (60. * 60. * 24. * 30.)

def fix_date_range(ts, relative_date_range):
    '''Returns the start and end time stamps of the date range relative to the time series
    this implementation makes some strong assumptions about the relative date range!'''
    # assumptions
    #   the relative date range spans only up to one year, and its start and end are in the same year
    year = datetime.datetime.fromtimestamp(ts[0][2]).year
    if relative_date_range:
        range_start = relative_date_range.start
        range_end = relative_date_range.end
    else:
        range_start = RelativeDate(1, 1)
        range_end = RelativeDate(12, 31)
    start = datetime.datetime(year, range_start.month, range_start.day)
    end = datetime.datetime(year, range_end.month, range_end.day)
    return time.mktime(start.timetuple()), time.mktime(end.timetuple())

def normalize_time_series_objects(tsos, interval, relative_date_range):
    # for each time series, we need to interpolate points every interval days over
    # the course of date range
    shortest = sys.maxint
    for tso in tsos:
        start_timestamp, end_timestamp = fix_date_range(tso.series, relative_date_range)
        # now we can interpolate for the times:
        times = np.arange(start_timestamp, end_timestamp + 1., interval*SECS_PER_DAY)
        if len(times) < shortest:
            shortest = len(times)
        new_ts = interpolate_ts(tso.series, times)
        tso.set_interpolated_series(new_ts)

    # some of the time series may be one or two points longer than another due to a leapyear
    # or something like that
    for tso in tsos:
        tso.interpolated_series = tso.interpolated_series[:shortest]

def normalize_time_series(tss, downsample_factor=None):
    # determine the latest start time and the earliest stop time
    start, end = get_time_limits(tss)
    print('Latest start time:')
    print(start)
    print('Earliest end time:')
    print(end)
    print('Difference in months')
    print(get_months(end - start))
    print()

    # determine all the times within this window across all time series
    common_times = get_all_times_in_window(tss, start, end)

    # replace each time series with its interpolations for each of the times in this window
    new_tss = interpolate_tss(tss, common_times)
    new_tss = np.array(new_tss)

    print('Shape of normalized time series:')
    print(new_tss.shape)
    print()

    if downsample_factor:
        print('Downsampling all time series by a factor of %d' % downsample_factor)
        print()
        new_tss = downsample_all(new_tss, downsample_factor)
        new_tss = np.array(new_tss)

    return new_tss


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

'''
if __name__ == '__main__':
    tss = [[[1.,1.,1.], [2.,2.,2.], [2.3, 2.3, 2.8], [3.,3.,3.], [4.,4.,4.]],[[1.25, 1.25, 1.1], [1.5, 1.5, 1.5], [2.5,2.5,2.5], [3.5,3.5,3.5], [4.5,4.5,4.5]]]
    print(tss[0])
    print(tss[1])
    new_tss = normalize_time_series(tss)

    print(new_tss)
'''
