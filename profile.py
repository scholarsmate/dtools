import sys
import operator


class ColumnarTable(object):
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
        prof = {}
        for val in self.ctable_[column]:
            if val in prof:
                prof[val] += 1
            else:
                prof[val] = 1
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
        p = table.profile_column(col)
        dv = len(p)
        print '*' * 79
        print "column name: %s\ndistinct values: %d" % (col, dv)
        print '=' * 79
        l = 0
        for i in sorted(p.items(), key=operator.itemgetter(1), reverse=True):
            sys.stdout.write('\'' + i[0] + '\': ' + str(i[1]) + ', ')
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
