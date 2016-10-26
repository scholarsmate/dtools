from collections import MutableMapping
from copy import copy
from inspect import getargspec
from threading import RLock


# --- lazy_property implementation --- #
class lazy_property(object):
    """
    Decorator for lazy evaluation of an object attribute.
    Property should be non-mutable data, as it replaces itself.
    """

    def __init__(self, fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value


# ------------------------------------------------------------------------------------
# LazyDictionary code is from https://github.com/janrain/lazydict (MIT license)
# ------------------------------------------------------------------------------------
# Copyright (c) 2014 Janrain, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------

# --- LazyDictionary Exceptions --- #
class LazyDictionaryError(Exception):
    pass


class CircularReferenceError(LazyDictionaryError):
    pass


class ConstantRedefinitionError(LazyDictionaryError):
    pass


# --- LazyDictionary implementation --- #
class LazyDictionary(MutableMapping):
    """
    A LazyDicitonary behaves mostly like an ordinary dict, except:

    * item values are frozen upon reading, and
    * values that are callable and take 1 or 0 arguments are called once before freezing
            + if the value takes 1 argument, the LazyDictionary instance will be supplied as the argument.
            + if calling the value raises an error, that error is frozen, and will be raised upon each subsequent read.

    These features allow values in the dictionary to be dependent on other values in the dictionary without regard to
    order of assignment. It also allows lazily not executing unused code
    """

    def __init__(self, values={}):
        self.lock = RLock()
        self.values = copy(values)
        self.states = {}
        for key in self.values:
            self.states[key] = 'defined'

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, key):
        with self.lock:
            if key in self.states:
                if self.states[key] == 'evaluating':
                    raise CircularReferenceError('value of "%s" depends on itself' % key)
                elif self.states[key] == 'error':
                    raise self.values[key]
                elif self.states[key] == 'defined':
                    value = self.values[key]
                    if callable(value):
                        (args, varargs, keywords, defaults) = getargspec(value)
                        if len(args) == 0:
                            self.states[key] = 'evaluating'
                            try:
                                self.values[key] = value()
                            except Exception as ex:
                                self.values[key] = ex
                                self.states[key] = 'error'
                                raise ex
                        elif len(args) == 1:
                            self.states[key] = 'evaluating'
                            try:
                                self.values[key] = value(self)
                            except Exception as ex:
                                self.values[key] = ex
                                self.states[key] = 'error'
                                raise ex
                    self.states[key] = 'evaluated'
            return self.values[key]

    def __contains__(self, key):
        return key in self.values

    def __setitem__(self, key, value):
        with self.lock:
            if key in self.states and self.states[key][0:4] == 'eval':
                raise ConstantRedefinitionError('"%s" is immutable' % key)
            self.values[key] = value
            self.states[key] = 'defined'

    def __delitem__(self, key):
        with self.lock:
            if key in self.states and self.states[key][0:4] == 'eval':
                raise ConstantRedefinitionError('"%s" is immutable' % key)
            del self.values[key]
            del self.states[key]

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return "LazyDictionary({0})".format(repr(self.values))


# Test / example of a lazy_property decorator
if __name__ == '__main__':

    import time

    from string import Template


    def template_variables(template):
        """Extract the variable names from a string.Template.

        Returns a list of all variable names found in the template, in the order
        in which they occur.  If an invalid escape sequence occurs, the same
        error will be raised as if an attempt was made to expand the template.
        """
        result = []
        for match in template.pattern.finditer(template.template):
            if match.group('invalid') is not None:
                # Raises ValueError
                template._invalid(match)
            if match.group('escaped') is not None:
                continue
            # The "or None" should be moot.  It is there to ensure equivalent
            # treatment for an empty 'named' and an empty 'braced'.
            result.append(match.group('named') or match.group('braced') or None)
        return result


    def populate_template(t, d):
        # The unfortunate thing here is that template substitutions hit all items in the dictionary even when the
        # template doesn't need it.  To fix this we need to process the template string for the possible keys and
        # only send in a dict with those keys.
        return t.safe_substitute(dict((k, d[k]) for k in template_variables(t) if k in d))


    def expensive_function():
        print 'Expensive function ...'
        time.sleep(2)
        return range(10)

    def fun(d):
        d.update({'f': lambda: expensive_function()})
        d['g'] = lambda: expensive_function()

    class Test(object):

        @lazy_property
        def a(self):
            print 'Calculating a ...'
            return expensive_function()


    t = Test()
    for i in range(5):
        print t.a

    d = LazyDictionary({'a': 1, 'b': lambda: expensive_function()})
    d.update({'e': lambda: expensive_function()})
    fun(d)

    # Updating one lazy dictionary with another causes the dictionary being added to call it's expensive functions
    # d2 = LazyDictionary({'c': 3})
    # d2.update(d)

    t = Template('a=$a, c=$c, d=$d, g=$g')
    print populate_template(t, d)
    for i in range(5):
        print d['b']
