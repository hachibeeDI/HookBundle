#!/usr/bin/env python
# -*- coding: utf-8 -*-

from commands import getoutput

import os.path

class Installer(object):
    """ install hook on hook-dir. """

    def __init__(self):
        pass

    def install(self, hook, content_id):
        hook.install(content_id)

