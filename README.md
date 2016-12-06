# README

Add the csv to the ./data/ folder

## k-means clustering

### Use `run_1.py` to cluster spatially

See `run_1.py`
Run with `python run_1.py [options]`.
An example with options: `python run_1.py turkey_vultures.csv --clust_range 1 8 1 --st .05 --dt .2 --interval 3`
**IMPORTANT**: Running this will result in pickled output being saved in `./postprocessed_data/`. You'll probably want to change the name that the file is saved with so you know what it is.
Run `python run_1.py --h` for a list of options.
**Brief explanation of the options**:
- `fpath`       [Required]: The name of the csv file (in the ./data/ folder)
- `rdr`         [Optional]: Relative date range in the form start_month start_day end_month end_day. For example, if you want to select points for each year from March 6 to November 12, you would use `--rdr 3 6 11 12`. Note that this will **NOT** work correctly if you want to use a range that spans the start of a new year (e.g. November 12 to February 20). This is a bug. I assume we won't need such date ranges - if we do, let me know.
- `it`         [Optional]: Inclusion threshold used when splitting the data. Decides what fraction of the desired interval time a set of points needs to cover to be included as a time series. For example, if the desired interval time is one year, and `it` is 0.5, then a set of points needs to only cover six months out of the year to be included. Default is 0.5. **NOTE**: The smaller this is, the more time series will be considered but the more likely it is that some of the time series don't consist of many months. The closer to 1 this is, the fewer time series will be considered but you can be sure that all time series have a good breadth of points.
- `n_clusts`    [Optional]: Use this if you don't want to cross-validate and just want to get results for a designated number of clusters. Default is 1.
- `clust_range` [Optional]: Use this to specify the range of number of clusters to cross-validate over. For example, `--clust_range 1 8 1` will result in `range(1, 8+1, 1)` being used as the number of clusters to try. **Recommendation**: use a larger range than you think is necessary, so that we will see errors converge. i.e. if you thing there are 5 clusters in the data, try a range like `1 8 1` instead of `1 5 1` or `3 5 1`, etc.
- `norm`        [Optional]: `1` if you want DTW to use an L1 norm and `2` if you want it to us the L2 norm
- `max_iters`   [Optional]: The maximum number of centroid updates (iterations) that will be used in clustering. The default is 15.
- `st`          [Optional]: Stopping threshold used during clustering (i.e. if the difference between the last iteration's error and the current iteration's error is less than `st`, then stop). Default is 0.05.
- `dt`          [Optional]: Difference threshold used to determine the best number of clusters. This isn't that important as all clusters will be pickled when the algorithm is done. For example, if 3 clusters gave an error of 2.5 and 4 clusters gave an error of 2.3, and `dt` is >= 0.2, then we will say that 3 is the best number of clusters. Default is 0.5
- `it`          [Optional]: Inclusion threshold used when
- `plot`        [Optional]: Plot some results using matplotlib. Default is False.

**NOTE**: I don't claim to have come up with the best default values, though they seem to be decent. Feel free to play around or ask questions!

### Use `run_2.py` to load pickled results

We still need code to cluster temporally! But for now, you can always load the results pickled by `run_1.py` using `run_2.py`.
Run with `python run_2.py [source_path]`, where `source_path` is the name of the pickled results `run_1.py` saved in `./postprocessed_data/`.
For an example, run with `python run_2.py example.pkl`
