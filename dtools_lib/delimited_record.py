def delimited_record_reader(fileobj, sep='|', header=None):
    if header is None:
        header = fileobj.readline().rstrip().split(sep)
    for row in fileobj:
        yield dict(zip(header, row.rstrip().split(sep)))
