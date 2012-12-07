#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Installer(object):
    """ install hook on hook-dir. """

    def __init__(self):
        pass

    def install(self, hook, content_id):
        hook.install(content_id)

