##################################################
# Copyright (C) 2017, All rights reserved.
##################################################

class Informational(Exception):
    def __init__(self, message):
        super(Informational, self).__init__(message)
