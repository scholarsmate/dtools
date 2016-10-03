import sys
from dtools_lib import delimited_record


def cut(fileobj, desired_fields, rec_header=None, sep='|'):
    if rec_header is None:
        rec_header = sys.stdin.readline().rstrip().split(sep)
    for rec in delimited_record.delimited_record_reader(fileobj, sep, rec_header):
        yield [rec[i] for i in desired_fields]

sep = '|'
desired_fields = sys.argv[1].split(',')
print sep.join(desired_fields)
for fields in cut(sys.stdin, desired_fields, sep=sep):
    print sep.join(fields)
