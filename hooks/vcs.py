#!/usr/bin/env python
# -*- coding: utf-8 -*-

from commands import getoutput

class Git(object):

    __rev_parse = getoutput('git rev-parse --git-dir')

    @classmethod
    def rev_parse(self):
        rev = self.__rev_parse
        return './' + rev if rev == '.git' else rev

