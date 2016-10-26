from collections import OrderedDict


# If you know the header and don't need the records generated as a dicts (they're generated as lists here), this gives
# better (~3x) performance
def read_delimited(fileobj, sep='|'):
    for row in fileobj:
        yield row.rstrip().split(sep)


# Generates records as ordered dicts
def read_records(fileobj, header=None, sep='|'):
    if header is None:
        header = fileobj.readline().rstrip().split(sep)
    num_rows = len(header)
    for row in read_delimited(fileobj, sep):
        if len(row) != num_rows:
            raise ValueError('Expected {0:d} columns, but got {1:d}:\n{2}\n{3}'.format(num_rows, len(row), sep.join(header), sep.join(row)))
        yield OrderedDict(zip(header, row))


def cut_fields(fileobj, desired_fields, header=None, sep='|'):
    if header is None:
        header = fileobj.readline().rstrip().split(sep)
    for rec in read_records(fileobj, header, sep):
        yield [rec[i] for i in desired_fields]
