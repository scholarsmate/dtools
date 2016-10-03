import hashlib
import uuid

RECORD = None
RECORD_COUNT = 0


def Field(field):
    return RECORD[field]


def ToUpper(s):
    return s.upper()


def ToLower(s):
    return s.lower()


def Reverse(s):
    return s[::-1]


def Capitalize(s):
    return s.capitalize()


def CapWords(s):
    return string.capwords(s)


def MD5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def Concat(*args):
    return ''.join([str(arg) for arg in args])


def Join(j, a1, a2, *args):
    arr = [str(a1), str(a2)]
    arr.extend([str(a) for a in args])
    return j.join(arr)


def Length(s):
    return len(s)


def RecordCount():
    return RECORD_COUNT


def Uuid():
    return uuid.uuid4()
