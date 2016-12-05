- We are having lots of trouble with years/seasons etc.
1. Perhaps it is not worth the trouble trying to split at a finer grain than years
    - should we still be concerned with splitting a migration in half?
2. Rather than worrying about clustering by year, we could cluster over paths for which
we have a full year's worth of data. So for each individual, we take all years for which
we have a full year's worth of data, and cluster all these paths. We can cluster
spatially with ease. Clustering temporally will require that we have evenly time-spaced
points for each path, and the same number for each path. This will work as we know that
the 1st point for each path represents January 1 and the 5th represents January 11, for
instance.

- We have till Friday. We need to be done with results by Wednesday I think.
So by the end of the meeting we should
    - know more or less exactly what we are doing
    - have planned datasets and experiments for each dataset
And by the end of the day:
    - fully functional code
