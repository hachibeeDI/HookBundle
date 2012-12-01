#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from os import path
from commands import getoutput

from hook import GistHook, LocalHook
from install import Installer

def separate_hook(path_str):
    #マシな方法探す
    rev_parse = getoutput('git rev-parse --git-dir')
    rev_parse = './' + rev_parse if rev_parse == '.git' else rev_parse
    hook_dir = path.join(rev_parse, 'hooks')
    if hook_dir.split(':')[0] == 'fatal':
        print 'not a git repository'
        quit()

    def build_hook():
        r = re.compile('^\d+$')
        if r.match(path_str):
            return GistHook(hook_dir)
        else:
            return LocalHook(hook_dir)
    return build_hook()

def main():
    if len(sys.argv) == 2:
        installer = Installer()
        installer.install(separate_hook(sys.argv[1]),sys.argv[1])
    else:
        print 'invailed argments'
        quit()

if __name__ == '__main__':
    main()

