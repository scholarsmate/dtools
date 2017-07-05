import hashlib
import math
import random
import string
import time
import unicodedata
import uuid
from collections import defaultdict

import phonenumbers
from faker import Factory

from dtools_lib import delimited_record

OBJECT_CACHE_ = {}

RECORD = {}
RECORD_COUNT = 0


# --- Record data fetch --- #
def Field(field):
    return RECORD[field]


def RecordCount():
    return RECORD_COUNT


def FieldCount():
    return len(RECORD)


# --- Type conversion --- #
def String(s):
    return str(s)


def Integer(s):
    return int(s)


def Float(s):
    return float(s)


def StringToBoolean(s):
    return s.lower() in ('t', 'true', 'y', 'yes', '1')


def BooleanToString(b):
    return 'True' if b else 'False'


# --- String functions --- #
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


def SwapChars(s, b1, b2=None):
    if b2 is None:
        b2 = b1 + 1
    t = list(s)
    t[b1], t[b2] = t[b2], t[b1]
    return ''.join(t)


def Insert(s, s2, pos=0):
    if pos == 0:
        return s2 + s
    if pos >= len(s):
        return s + s2
    return s[:pos] + s2 + s[pos:]


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


def MD5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


# --- Numeric functions --- #
def RandomInteger(min, max):
    return random.randint(min, max)


def Sum(num1, num2, *args):
    result = num1 + num2
    for i in args:
        result += i
    return result


def Product(num1, num2, *args):
    result = num1 * num2
    for i in args:
        result *= i
    return result


def Subtract(num1, num2):
    return num1 - num2


def Divide(num1, num2):
    return num1 / num2


def Remainder(num1, num2):
    return num1 % num2


def Round(num):
    return round(num)


def Floor(num):
    return math.floor(num)


def Ceil(num):
    return math.ceil(num)


def Log(num, base=10):
    return math.log(num, base)


def Pow(num1, num2):
    return math.pow(num1, num2)


def Sqrt(num):
    return math.sqrt(num)


def NearestPowerOfTwo(num):
    return int(2 ** math.ceil(math.log(num, 2)))


# --- Combinatoric functions --- #
def PowerSet(items):
    N = len(items)
    # enumerate the 2**N possible combinations of items
    for i in range(2 ** N):
        combo = []
        for j in range(N):
            # test jth bit of integer i
            if (i >> j) % 2 == 1:
                combo.append(items[j])
        yield combo


# --- Date functions --- #
def EpochToString(e, fmt='%F %Y %T'):
    return time.strftime(fmt, time.gmtime(e))


def StringToEpoch(s, fmt):
    return int(time.mktime(time.strptime(s, fmt)))


def EpochTime():
    return int(time.time())


# --- Boolean Functions --- #
def Equals(term1, term2):
    return term1 == term2


def NotEquals(term1, term2):
    return term1 != term2


def LessThan(term1, term2):
    return term1 < term2


def LessThanOrEquals(term1, term2):
    return term1 <= term2


def GreaterThan(term1, term2):
    return term1 > term2


def GreaterThanOrEquals(term1, term2):
    return term1 >= term2


def Any(*args):
    return any(args)


def All(*args):
    return all(args)


# -- Geo functions --- #
def KilometersToMiles(km):
    return km * 0.621371


def MilesToKilometers(miles):
    return miles * 1.60934


def Haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points on the earth (specified in decimal degrees)
    """
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, (lon1, lat1, lon2, lat2))

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * math.asin(math.sqrt(a)) * r


# --- Ancillary file functions --- #
def CreateMap(filename, key, value, sep='|'):
    object_key = '__MAP__:' + '\t'.join([filename, key, value])
    if object_key not in OBJECT_CACHE_:
        m = {}
        with open(filename) as fin:
            for rec in delimited_record.read_records(fin, sep=sep):
                m[rec[key]] = rec[value]
        OBJECT_CACHE_[object_key] = m
    return object_key


def CreateList(filename, key=None, sep='|'):
    object_key = '__LIST__:' + filename if key is None else '\t'.join([filename, key])
    if object_key not in OBJECT_CACHE_:
        with open(filename) as fin:
            OBJECT_CACHE_[object_key] = [line.rstrip() for line in fin] if key is None else \
                [rec[key] for rec in delimited_record.read_records(fin, sep=sep)]
    return object_key


def CreateMultiMap(filename, key, value, sep='|'):
    object_key = '__MULTIMAP__:' + '\t'.join([filename, key, value])
    if object_key not in OBJECT_CACHE_:
        with open(filename) as fin:
            m = defaultdict(list)
            for rec in delimited_record.read_records(fin, sep=sep):
                m[rec[key]].append(rec[value])
                OBJECT_CACHE_[object_key] = m
    return object_key


# --- Lookup functions --- #
def Lookup(s, map_key, default=None):
    if default is None:
        default = s
    return OBJECT_CACHE_[map_key][s] if s in OBJECT_CACHE_[map_key] else default


def SubstWords(s, map_key):
    return ' '.join([Lookup(w, map_key) for w in s.split()])


# --- Randomization functions --- #
def Uuid():
    return uuid.uuid4()


def Shuffle(s):
    random.shuffle(s)
    return s


def RandomChoice(list_key):
    return random.choice(OBJECT_CACHE_[list_key])


def RandomChoiceLookup(s, multi_map_key, default=None):
    return random.choice(OBJECT_CACHE_[multi_map_key][s]) if s in OBJECT_CACHE_[multi_map_key] else default


def RandomChoiceWordsLookup(s, multi_map_key):
    return ' '.join([RandomChoiceLookup(w, multi_map_key, w) for w in s.split()])


def TransposeRandomBytes(s, num_transposes=1):
    result = list(s)
    len_s = len(result)
    if len_s > 1:
        for _ in range(num_transposes):
            r = random.randint(0, len_s - 2)
            result[r], result[r + 1] = result[r + 1], result[r]
    return ''.join(result)


def PickOne(a, b, prob=0.5):
    return a if random.random() <= prob else b


# --- Decomposition functions --- #
class DecompositionMap(dict):
    CHAR_REPLACEMENT = {
        # latin-1 characters that don't have a unicode decomposition
        0xc6: u"AE",  # LATIN CAPITAL LETTER AE
        0xd0: u"D",  # LATIN CAPITAL LETTER ETH
        0xd8: u"OE",  # LATIN CAPITAL LETTER O WITH STROKE
        0xde: u"Th",  # LATIN CAPITAL LETTER THORN
        0xdf: u"ss",  # LATIN SMALL LETTER SHARP S
        0xe6: u"ae",  # LATIN SMALL LETTER AE
        0xf0: u"d",  # LATIN SMALL LETTER ETH
        0xf8: u"oe",  # LATIN SMALL LETTER O WITH STROKE
        0xfe: u"th",  # LATIN SMALL LETTER THORN
    }

    ##
    # Maps a unicode character code (the key) to a replacement code
    # (either a character code or a unicode string).
    def mapchar(self, key):
        ch = self.get(key)
        if ch is not None:
            return ch
        de = unicodedata.decomposition(unichr(key))
        if de:
            try:
                ch = int(de.split(None, 1)[0], 16)
            except (IndexError, ValueError):
                ch = key
        else:
            ch = DecompositionMap.CHAR_REPLACEMENT.get(key, key)
        self[key] = ch
        return ch

    __missing__ = mapchar


DECOMPOSITION_MAP_ = DecompositionMap()


def ToAscii(utf_string):
    return utf_string.decode('utf-8').translate(DECOMPOSITION_MAP_).encode('ascii', 'ignore')


# --- Standardization functions --- #
def StandardizePhone(s, region=None, phone_format=phonenumbers.PhoneNumberFormat.E164):
    return phonenumbers.format_number(phonenumbers.parse(s, region=region), phone_format)


# --- Generator functions --- #
def CreateGeneratorFactory(seed=None, locale='en_US'):
    object_key = '__DATA_GENERATOR__:' + '\t'.join([locale, str(seed)])
    if object_key not in OBJECT_CACHE_:
        gen = Factory.create(locale)
        gen.seed(seed)
        OBJECT_CACHE_[object_key] = gen
    return object_key


def GenerateCompany(object_key):
    return OBJECT_CACHE_[object_key].company()


def GenerateEmail(object_key):
    return OBJECT_CACHE_[object_key].email()


def GeneratePhoneNumber(object_key):
    return OBJECT_CACHE_[object_key].phone_number()


def GenerateURL(object_key):
    return OBJECT_CACHE_[object_key].url()


def GenerateJob(object_key):
    return OBJECT_CACHE_[object_key].job()


def GenerateDate(object_key):
    return OBJECT_CACHE_[object_key].date()

def GenerateDateBetween(object_key, start_date='-30y', end_date='now', format='%Y-%m-%d', tzinfo=None):
    return OBJECT_CACHE_[object_key].date_time_between(start_date, end_date, tzinfo).strftime(format)
