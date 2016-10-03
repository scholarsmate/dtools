import sys

from dtools_lib import delimited_record, sample

seed = None
sep = '|'
sampler = sample.Sample(percent=float(sys.argv[1]), seed=seed)
header = sys.stdin.readline().rstrip().split(sep)
print sep.join(header)
for rec in delimited_record.delimited_record_reader(sys.stdin, sep=sep, header=header):
    if sampler.is_selected():
        print sep.join([rec[col] for col in header])
