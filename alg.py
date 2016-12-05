
from __future__ import print_function

class Individual(object):
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end

    def __str__(self):
        return '(' + str(self.start) + ', ' + str(self.end) + ')'

'''
def get_subsets(l):
    print(l)
    if len(l) == 0:
        return [[]]
    else:
        x = l[0]
        xs = l[1:]
        ss_wo_x = get_subsets(xs)
        #print(ss_wo_x)
        return [ss.append(x) for ss in ss_wo_x] + ss_wo_x

def get_times(indivs):
    latest_start_time = 0.
    earliest_end_time = float('inf')
    for indiv in indivs:
        if indiv.start > latest_start_time:
            latest_start_time = indiv.start
        if indiv.end < earliest_end_time:
            earliest_end_time = indiv.end
    return latest_start_time, earliest_end_time

def max_subset(indivs, t):

    # throw out indivs that we can't possibly take
    new_indivs = []
    for invid in indivs:
        if (indiv.end - indiv.start) >= t:
            new_indivs.append(indiv)

    # get all subsets
    subsets = get_subsets(new_indivs)

    print('Number of subsets')
    print(len(subsets))

    # for each subset, get the overlap
    best_subset = None
'''

times = [
  (0,10),
  (3,10),
  (2,8),
  (0,6)
]

indivs = [
    Individual(1, 0, 10),
    Individual(2, 3, 10),
    Individual(3, 2, 8),
    Individual(4, 0, 6)
]

def solve(indivs, s):
  starts = sorted(indivs, key=lambda x: x.start)
  ends = sorted(indivs, key=lambda x: x.end)

  current_stack = []

  largest = []

  while len(starts) + len(ends) > 0:
    while len(starts) > 0 and starts[0].start <= ends[0].end:
      current_stack.append(starts.pop(0))

      for i in range(0, len(current_stack) - len(largest)):

        if current_stack[i].end - current_stack[-1].start >= s:

          amax = max(current_stack, key=lambda x: x.start)
          foo = filter(lambda x: (x.end >= amax.start + s), current_stack)
          if len(foo) > len(largest):
            largest = foo[:]
          continue

    if len(starts) == 0: break

    while ends[0].end < starts[0].start:
      current_stack.remove(ends.pop(0))

  return largest

indivs_to_keep = solve(indivs, 7)
for i in indivs_to_keep:
    print(i, end=' ')
print()

'''
def solve(t, s):
  starts = sorted(t, key=lambda x: x[0])
  ends = sorted(t, key=lambda x: x[1])

  current_stack = []

  largest = []

  while len(starts) + len(ends) > 0:
    while len(starts) > 0 and starts[0][0] <= ends[0][1]:
      current_stack.append(starts.pop(0))

      for i in range(0, len(current_stack) - len(largest)):

        if current_stack[i][1] - current_stack[-1][0] >= s:

          amax = max(current_stack, key=lambda x: x[0])
          foo = filter(lambda x: (x[1] >= amax[0] + s), current_stack)
          if len(foo) > len(largest):
            largest = foo[:]
          continue

    if len(starts) == 0: break

    while ends[0][1] < starts[0][0]:
      current_stack.remove(ends.pop(0))

  return largest
'''
