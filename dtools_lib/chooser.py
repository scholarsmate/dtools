import bisect
import operator
import random
import numpy


def accumulate(iterable, func=operator.add):
    """Return running totals"""
    # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    it = iter(iterable)
    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        total = func(total, element)
        yield total


class Chooser(object):
    def __init__(self, choices):
        self.choices_ = choices

    def choices(self):
        return self.choices_

    def choose(self):
        return random.choice(self.choices_)


class GaussianChooser(Chooser):
    """Random number chooser with a Gaussian (normal) distribution."""
    def __init__(self, mean, std_dev, samples=1000):
        super(GaussianChooser, self).__init__(numpy.random.normal(mean, std_dev, samples))


class WeightedChooser(Chooser):
    def __init__(self, weighted_choices):
        """
        Create an object that makes a weighted choice where choices with higher weights are more likely to be chosen.

        :param weighted_choices: an iterable of tuples where the first element is a choice and the second element is a
            weight
        """
        choices, weights = zip(*weighted_choices)
        super(WeightedChooser, self).__init__(choices)
        self.cumulative_weights_ = list(accumulate(weights))

    def choose(self):
        return self.choices_[bisect.bisect(self.cumulative_weights_, random.random() * self.cumulative_weights_[-1])]
