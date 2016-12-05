# TODO

## General TODOS
- For turkey vultures, use years, for geese use March-October for all years possible
- *DONE* Implement preprocessing for this
- **TODO** For interpolation, will have to implement constant intervals
- **TODO** Cross-validation implementation

- **TODO** Figure out how to analyze clusters


- implement cross-validation for clustering
    - which means, add a loss function as well
- implement euclidean distance and clustering by euclidean distance
- modify preprocessing/interpolation to work with timeframes rather than simply years






[x] Determine structure of data points:
    Q: is there a point for each animal at each time? i.e. are tracking devices coordinated in their measurements?
    A: in general no
    Q: are there the same number of points for each animal?
    A: in general, no
[x] Does DTW require that each time series have measurements taken at the same times?
    A: No, doesn't actually care about times or time interval between points
[x] Implement interpolation
[x] Replace custom keogh and dtw in clustering alg with python dtw implementations


## Notes

### Sites
Similarity Measures
http://stats.stackexchange.com/questions/27861/similarity-measures-between-curves
Clustering and classification examples
https://github.com/alexminnaar/time-series-classification-and-clustering
Procrustes - similar to dtw in that it will align curves
https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.spatial.procrustes.html

Frechet distance might help find outliers or at least tell us that outliers exist

Questions we want to be able to answer:
1. Comparing migrations between individuals for a given year
    - Can we spot outliers? Animals doing things differently?
2. Comparing migrations for a single animal over many years
    - Does the animal always take the same path?
        - if so, how similar are the paths it takes? Identical? Roughly the same?
        All the same except for a point or two? Can we find and explain outliers in the paths?
3. Cluster a species based on migrations
    - can we discover natural "herds" of animals? i.e. ones that take different
    migrational paths or the same path but at different times?

IN GENERAL
We need to be able to compare paths spatially and temporally.
For spatial comparison, we can use dtw or Procrustes, or similar
    Seems we can also use dtw to detect a phase in paths!!!
If dtw scores are low, and no phase, then cluster the two animals
If dtw scores are low, but phase, then paths are the same but different temporally (one is delayed)
If dtw scores are rather different, then paths are rather different

==> Do we even need Euclidean distance? Only if we can't use the dtw phase as we think we can.
For temporal comparison, we can use Euclidean distance (or just phase shift)

Idea for temporal clustering:
- use interpolation to create additional time points so that each animal has locations for the same times
- then use simple Euclidean distance between each pair of points
- we can then cluster using 1-nn
