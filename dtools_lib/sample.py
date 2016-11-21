import random


class Sample(object):
    def __init__(self, percent, seed=None, period=100):
        if seed is not None:
            random.seed(seed)
        self.period_ = period
        self.shuffled_ = list(range(period))
        self.threshold_ = int(period * percent)
        self.index_ = 0
        random.shuffle(self.shuffled_)

    def is_selected(self):
        selected = self.shuffled_[self.index_] < self.threshold_
        self.index_ += 1
        if self.index_ == self.period_:
            random.shuffle(self.shuffled_)
            self.index_ = 0
        return selected
