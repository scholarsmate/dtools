import hashlib
import random
import string
import uuid
from collections import defaultdict

RECORD = None
RECORD_COUNT = 0


def String(s):
    return str(s)


def Integer(s):
    return int(s)


def Float(s):
    return float(s)


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


def LStrip(s):
    return s.lstrip()


def RStrip(s):
    return s.rstrip()


def Strip(s):
    return s.strip()


def Substr(s, start, length):
    return s[start:start + length]


def FirstN(s, length):
    return s[:length]


def LastN(s, length):
    return s[length:]


def SqueezeWhite(s):
    return ' '.join(s.split())


def PunctWhite(s):
    return s.translate(string.maketrans(string.punctuation, ' ' * len(string.punctuation)))


def Replace(s, old, new, max=None):
    return s.replace(old, new, max)


def TitleCase(s):
    return s.title()


def SwapCase(s):
    return s.swapcase()


def RJust(s, width, fillchar=None):
    return s.rjust(width, fillchar)


def LJust(s, width, fillchar=None):
    return s.ljust(width, fillchar)


def Length(s):
    return len(s)


def RecordCount():
    return RECORD_COUNT


def Uuid():
    return uuid.uuid4()


def RandomInteger(min, max):
    return random.randint(min, max)


def SwapChars(s, b1, b2=None):
    if b2 is None:
        b2 = b1 + 1
    t = list(s)
    t[b1], t[b2] = t[b2], t[b1]
    return ''.join(t)


def Shuffle(s):
    random.shuffle(s)
    return s


RANDOM_CHOICE_CACHE = {}


def RandomChoice(filename, skip_first_line=False):
    if filename not in RANDOM_CHOICE_CACHE:
        with open(filename) as fin:
            if skip_first_line:
                fin.readline()
            RANDOM_CHOICE_CACHE[filename] = [line.rstrip() for line in fin]
    return random.choice(RANDOM_CHOICE_CACHE[filename])


LOOKUP_CACHE = {}


def Lookup(s, filename, skip_first_line=False, sep='|', default=None):
    if default is None:
        default = s
    if filename not in LOOKUP_CACHE:
        with open(filename) as fin:
            if skip_first_line:
                fin.readline()
            m = {}
            for line in fin:
                (key, value) = line.rstrip().split(sep, 2)
                m[key] = value
        LOOKUP_CACHE[filename] = m
    lookup_map = LOOKUP_CACHE[filename]
    return lookup_map[s] if s in lookup_map else default


RANDOM_CHOICE_LOOKUP_CACHE = {}


def RandomChoiceLookup(s, filename, skip_first_line=False, sep='|', default=None):
    if default is None:
        default = s
    if filename not in RANDOM_CHOICE_LOOKUP_CACHE:
        with open(filename) as fin:
            if skip_first_line:
                fin.readline()
            m = defaultdict(list)
            for line in fin:
                (key, value) = line.rstrip().split(sep, 2)
                m[key].append(value)
            RANDOM_CHOICE_LOOKUP_CACHE[filename] = m
    lookup_map = RANDOM_CHOICE_LOOKUP_CACHE[filename]
    return random.choice(lookup_map[s]) if s in lookup_map else default
