#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, walk, chmod

from vcs import Git

class Installer(object):
    """ install hook on hook-dir. """

    def __init__(self):
        # なんか他にいい方法ないか検討したいけど、これでいいかなぁ感もある
        rev_parse = Git.rev_parse()
        self.git_hook_dir = path.join(rev_parse, 'hooks')
        self.__is_currentdir_managed_git(self.git_hook_dir)

    def __is_currentdir_managed_git(self, rev_parse_result):
        # depends on git's error message style
        if rev_parse_result.split(':')[0] == 'fatal':
            print u'not a git repository'
            #TODO InvailedDirExceptionだかを適当に作る
            raise Exception

    def install(self, hook):
        hook.install(self.git_hook_dir)

    def ch_script_mode(self):
        for hook in search_files(self.git_hook_dir):
            print u'change %s\'s mode' % hook
            chmod(hook, 0755)


def search_files(dirname):
    for root, dirs, files in walk(dirname):
        for fi in files:
            yield path.join(root, fi)


