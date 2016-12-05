'''Example using new preprocessing technique'''

from __future__ import print_function

from preprocess import get_data_by_individual, get_time_series, RelativeDate, RelativeDateRange

if __name__ == '__main__':

    # get a map of individual id to all its data, ordered by time
    indiv_to_ts = get_data_by_individual(TODO: filename)

    # optionally define a relative date range, e.g.
    start = RelativeDate(3, 1)
    end = RelativeDate(11, 1)
    rdr = RelativeDateRange(start, end)

    # get all the time series (splits)
    tsos = get_time_series(data, rdr)

    print('Total number of time series')
    print(len(tsos))
    print()

    # Do whatever you need to do with them
