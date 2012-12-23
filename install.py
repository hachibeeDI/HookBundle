#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from commands import getoutput

class Installer(object):
    """ install hook on hook-dir. """

    def __init__(self):
        # なんか他にいい方法ないか検討したいけど、これでいいかなぁ感もある
        rev_parse = getoutput('git rev-parse --git-dir')
        rev_parse = './' + rev_parse if rev_parse == '.git' else rev_parse
        self.git_hook_dir = path.join(rev_parse, 'hooks')
        self.__is_currentdir_managed_git(self.git_hook_dir)

    def __is_currentdir_managed_git(self, rev_parse_result):
        # depends on git's error message style
        if rev_parse_result.split(':')[0] == 'fatal':
            print 'not a git repository'
            #TODO InvailedDirExceptionだかを適当に作る
            raise Exception

    def install(self, hook):
        hook.install(self.git_hook_dir)

