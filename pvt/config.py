##################################################
# Copyright (C) 2017, All rights reserved.
##################################################

class Config(object):
    def __init__(self, dir):
        self._dir = dir

    @property
    def dir(self): return self._dir
