import bisect
import random


class Chooser(object):
    def __init__(self, choices):
        self.choices_ = choices

    def choices(self):
        return self.choices_

    def choose(self):
        return random.choice(self.choices_)


class WeightedChooser(Chooser):
    def __init__(self, weighted_choices):
        """
        Create an object that makes a weighted choice where choices with higher weights are more likely to be chosen.

        :param weighted_choices: an iterable of tuples where the first element is a choice and the second element is a
            weight
        """
        choices, weights = zip(*weighted_choices)
        super(WeightedChooser, self).__init__(choices)
        self.total_ = 0
        self.cumulative_weights_ = []
        for w in weights:
            self.total_ += w
            self.cumulative_weights_.append(self.total_)

    def choose(self):
        return self.choices_[bisect.bisect(self.cumulative_weights_, random.random() * self.total_)]
