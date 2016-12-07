
class Test(object):

    def __init__(self):
        self.assignments = {}
        self.assignments_history = []

    def set_assignments(self, a):
        self.assignments = a
        self.save_assignments_to_history()

    def save_assignments_to_history(self):
        self.assignments_history.append(self.assignments)


test = Test()

a = {1: 1, 2: 2}

test.set_assignments(a)

b = {1: 1, 2:2, 3:3}

test.set_assignments(b)

print test.assignments_history
