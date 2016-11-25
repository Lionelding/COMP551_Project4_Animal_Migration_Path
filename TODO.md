# TODO

[x] Determine structure of data points:
    Q: is there a point for each animal at each time? i.e. are tracking devices coordinated in their measurements?
    A: in general no
    Q: are there the same number of points for each animal?
    A: in general, no
[x] Does DTW require that each time series have measurements taken at the same times?
    A: No, doesn't actually care about times or time interval between points

## Preprocessing
[ ] handle this based on above research
[ ] group by year

## Sites
Similarity Measures
http://stats.stackexchange.com/questions/27861/similarity-measures-between-curves
Clustering and classification examples
https://github.com/alexminnaar/time-series-classification-and-clustering

Procrustes - similar to dtw in that it will align curves
https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.spatial.procrustes.html

Questions we want to be able to answer:
1. Comparing migrations between animals for a given year
    - Can we spot outliers? Animals doing things differently?
2. Comparing migrations for a single animal over many years
    - Does the animal always take the same path?
        - if so, how similar are the paths it takes? Identical? Roughly the same?
        All the same except for a point or two? Can we find and explain outliers in the paths?
3. Cluster a species based on migrations
    - can we discover natural "herds" of animals? i.e. ones that take different
    migrational paths or the same path but at different times?

We need to be able to compare paths spatially and temporally.
For spatial comparison, we can use dtw or Procrustes
Seems we can also use dtw to detect a phase in paths!!!
For temporal comparison, we have the following idea:

Idea:
- use interpolation to create additional time points so that each animal has locations for the same times
- then use simple Euclidean distance between each pair of points
- we can then cluster using 1-nn
