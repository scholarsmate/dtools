import hashlib
import random
import re
import string
import uuid
from collections import defaultdict

from dtools_lib import delimited_record

OBJECT_CACHE_ = {}

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


def Pattern(s):
    pattern = ''
    alpha = 0
    digit = 0
    punct = 0
    space = 0
    for c in s:
        if c.isalpha():
            if alpha == 0:
                if digit > 0:
                    pattern += 'D' if digit == 1 else 'D+'
                    digit = 0
                elif punct > 0:
                    pattern += 'P' if punct == 1 else 'P+'
                    punct = 0
                elif space > 0:
                    pattern += ' '
                    space = 0
            alpha += 1
        elif c.isdigit():
            if digit == 0:
                if alpha > 0:
                    pattern += 'L' if alpha == 1 else 'L+'
                    alpha = 0
                elif punct > 0:
                    pattern += 'P' if punct == 1 else 'P+'
                    punct = 0
                elif space > 0:
                    pattern += ' '
                    space = 0
            digit += 1
        elif c.isspace():
            if space == 0:
                if alpha > 0:
                    pattern += 'L' if alpha == 1 else 'L+'
                    alpha = 0
                elif punct > 0:
                    pattern += 'P' if punct == 1 else 'P+'
                    punct = 0
                elif digit > 0:
                    pattern += 'D' if digit == 1 else 'D+'
                    digit = 0
            space += 1
        else:
            if punct == 0:
                if alpha > 0:
                    pattern += 'L' if alpha == 1 else 'L+'
                    alpha = 0
                elif digit > 0:
                    pattern += 'D' if digit == 1 else 'D+'
                    digit = 0
                elif space > 0:
                    pattern += ' '
                    space = 0
            punct += 1
    if alpha > 0:
        pattern += 'L' if alpha == 1 else 'L+'
    elif digit > 0:
        pattern += 'D' if digit == 1 else 'D+'
    elif punct > 0:
        pattern += 'P' if punct == 1 else 'P+'
    elif space > 0:
        pattern += ' '
    return pattern


def CreateMap(filename, key, value, sep='|'):
    object_key = '__MAP__:' + '\t'.join([filename, key, value])
    if object_key not in OBJECT_CACHE_:
        m = {}
        with open(filename) as fin:
            for rec in delimited_record.delimited_record_reader(fin, sep):
                m[rec[key]] = rec[value]
        OBJECT_CACHE_[object_key] = m
    return object_key


def CreateList(filename, key=None, sep='|'):
    object_key = '__LIST__:' + filename if key is None else '\t'.join([filename, key])
    if object_key not in OBJECT_CACHE_:
        with open(filename) as fin:
            OBJECT_CACHE_[object_key] = [line.rstrip() for line in fin] if key is None else \
                [rec[key] for rec in delimited_record.delimited_record_reader(fin, sep)]
    return object_key


def CreateMultiMap(filename, key, value, sep='|'):
    object_key = '__MULTIMAP__:' + '\t'.join([filename, key, value])
    if object_key not in OBJECT_CACHE_:
        with open(filename) as fin:
            m = defaultdict(list)
            for rec in delimited_record.delimited_record_reader(fin, sep):
                m[rec[key]].append(rec[value])
                OBJECT_CACHE_[object_key] = m
    return object_key


def RandomChoice(list_key):
    return random.choice(OBJECT_CACHE_[list_key])


def Lookup(s, map_key, default=None):
    if default is None:
        default = s
    return OBJECT_CACHE_[map_key][s] if s in OBJECT_CACHE_[map_key] else default


def RandomChoiceLookup(s, multi_map_key, default=None):
    return random.choice(OBJECT_CACHE_[multi_map_key][s]) if s in OBJECT_CACHE_[multi_map_key] else default


def SubstWords(s, map_key):
    return ' '.join([Lookup(w, map_key) for w in s.split()])
