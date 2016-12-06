'''Cross validation'''

from __future__ import print_function

class CrossValidator(object):

    def __init__(self, n_restarts, tsos):
        self.n_restarts = n_restarts
        self.tsos = tsos

    def cross_validate(self, clusterer):
        '''Clusters the time series objects using the clusterer n_restarts times
        recording the error obtained each time. Returns the average error.'''
        errs = []
        for i in range(self.n_restarts):
            clusterer.k_means_clust(self.tsos, verbose=True)
            err = clusterer.get_assignment_error()
            print('Clustering error for attempt #%d: %f' % (i, err))
            print()
            errs.append(err)
        return sum(errs)/len(errs)

## END
