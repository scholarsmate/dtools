import operator
import sys
from dtools_lib import transforms


class ColumnarTable(object):
    class Profile(object):
        value_histogram = None
        pattern_histogram = None
        minimum_length = sys.maxint
        maximum_length = 0

    def __init__(self, header):
        self.header_ = header
        self.ctable_ = {}
        for col in header:
            self.ctable_[col] = []
        self.numcols_ = len(header)

    def add_row(self, row):
        if len(row) != self.numcols_:
            raise ValueError('number of columns in the given row does not match the number of columns in this table')
        for col in range(0, self.numcols_):
            self.ctable_[self.header_[col]].append(row[col])

    def get_header(self):
        return self.header_

    def profile_column(self, column):
        prof = self.Profile()
        value_histogram = {}
        pattern_histogram = {}
        for val in self.ctable_[column]:
            prof.minimum_length = min(len(val), prof.minimum_length)
            prof.maximum_length = max(len(val), prof.maximum_length)
            if val in value_histogram:
                value_histogram[val] += 1
            else:
                value_histogram[val] = 1
            pattern = transforms.Pattern(val)
            if pattern in pattern_histogram:
                pattern_histogram[pattern] = (pattern_histogram[pattern][0] + 1, pattern_histogram[pattern][1])
            else:
                pattern_histogram[pattern] = (1, val)
        prof.value_histogram = value_histogram
        prof.pattern_histogram = pattern_histogram
        return prof


def populate_columnar_table(fileobj, sep='|', header=None):
    if header is None:
        header = fileobj.readline().rstrip().split(sep)
    result = ColumnarTable(header)
    for row in fileobj:
        result.add_row(row.rstrip().split(sep))
    return result


def profile(table, limit=100):
    for col in table.get_header():
        profile = table.profile_column(col)
        distinct_values = len(profile.value_histogram)
        distinct_patterns = len(profile.pattern_histogram)
        print '*' * 79
        print "column name: %s\nminimum length: %d, maximum length: %d\ndistinct values: %d, distinct patterns: %d" % \
              (col, profile.minimum_length, profile.maximum_length, distinct_values, distinct_patterns)
        print '=' * 79
        l = 0
        p = profile.value_histogram
        for i in sorted(p.items(), key=operator.itemgetter(1), reverse=True):
            sys.stdout.write('\'' + i[0] + '\': ' + str(i[1]) + ', ')
            #            sys.stdout.write('\'' + i[0] + '\', ')
            l += 1
            if l == limit:
                sys.stdout.write('...')
                break
        print
        print '=' * 79
        l = 0
        p = profile.pattern_histogram
        for i in sorted(p.items(), key=operator.itemgetter(1), reverse=True):
            sys.stdout.write('\'' + i[0] + '\': ' + str(i[1][0]) + ' [' + i[1][1] + '], ')
            #            sys.stdout.write('\'' + i[0] + '\', ')
            l += 1
            if l == limit:
                sys.stdout.write('...')
                break
        print

table = None
sep = '|'
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
        table = populate_columnar_table(f, sep)
else:
    table = populate_columnar_table(sys.stdin, sep)
profile(table)
