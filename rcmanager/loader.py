#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, environ
import codecs


class SettingFile(object):
    """ content url. """

    homepath = environ.get('HOME')
    rc_file = '.hook_bundle'

    def __init__(self):
        pass

    def get_lines(self):
        try:
            with codecs.open(
                    path.join(self.homepath, self.rc_file), 'r', 'UTF-8') as f:
                yield f.readlines()

        except IOError, e:
            print '.hook_bundle is not in your home directory'




