#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os import path
from commands import getoutput

from hook import GistHook, LocalHook
from install import Installer
from rcmanager.loader import SettingFile

def separate_hook(path_str):
    #マシな方法探す
    rev_parse = getoutput('git rev-parse --git-dir')
    rev_parse = './' + rev_parse if rev_parse == '.git' else rev_parse
    hook_dir = path.join(rev_parse, 'hooks')
    #depends on git's error message style
    if hook_dir.split(':')[0] == 'fatal':
        print 'not a git repository'
        quit()

    def build_hook():
        # if there is only numbers, it is gist-id
        #TODO 一旦完成してからもっとまともな実装を
        r = re.compile('^\d+$')
        if r.match(path_str):
            return GistHook(hook_dir)
        else:
            return LocalHook(hook_dir)
    return build_hook()

def main():
    installer = Installer()
    setting_file = SettingFile()
    #TODO
    for line in setting_file.get_lines():
        for li in line:
            uri = li.split(',')[0]
            print 'id:' + uri
            installer.install(separate_hook(uri), uri)


if __name__ == '__main__':
    main()

