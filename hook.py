#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os import path

import requests
import json

"""
hook.py
----------

install, description(info), original_path
"""

def configuration_parser(line):
    """ parse dotfile's configration and built Hook object. """
    st = line.split(',')
    uri = st[0]
    hooktype = st[1]
    description = st[2]

    def build_hook():
        # if there is only numbers, it is gist-id
        #TODO 一旦完成してからもっとまともな実装を
        r = re.compile('^\d+$')
        if r.match(uri):
            return GistHook(uri, hooktype)
        else:
            return LocalHook(uri, hooktype)
    return build_hook()


class Hook(object):
    """ abstract class. This work as hook contents. """

    # ひとまずこんだけ。ailiasとかはのちのち。もしくは分けるかも
    hooktype_definitions = [
            "pre-commit"
            ,"prepare-commit-msg"
            ,"commit-msg"
            ,"post-commit"
            ,"pre-rebase"
            ,"post-rebase"
            ,"post-merge"
            ]

    def __init__(self, _contents_path, _hooktype):
        self._contents_path = _contents_path
        self._hooktype_save_location = self.__initialize_hook(_hooktype)

    def __initialize_hook(self, hooktype):
        # そのうちdictとかそういう系にするので
        matchedhook = [h for h in self.hooktype_definitions if h == hooktype]
        if matchedhook == None:
            # TODO InvailedHookTypeExceptionとか
            raise Exception
        return matchedhook[0]

    def install(self, git_hook_dir):
        #TODO あとでNotImplementExceptionだか作る
        raise Exception()

    def _write(self, file_name, code):
        target_fullpath = path.join(self.install_dir,
                          self._hooktype_save_location, file_name)
        with open(target_fullpath, 'w') as hook_file:
            hook_file.write(code)


class GistHook(Hook):

    def __init__(self, _contents_path, _hooktype):
        Hook.__init__(self, _contents_path, _hooktype)

    def install(self, git_hook_dir):
        gist = Gist(self._contents_path)
        raw_url = gist.get_raw_url()
        print u'get from raw-url: %s\n' % raw_url
        print u'description: %s\n' % gist.get_description()
        hook_code = requests.get(raw_url).content
        self._write(gist.get_filename(), hook_code)


class LocalHook(Hook):

    def __init__(self, _contents_path, _hooktype):
        Hook.__init__(self, _contents_path, _hooktype)

    def install(self, git_hook_dir):
        file_name = self._contents_path.split('/')[-1]
        hook_code = open(self._contents_path).read()
        self._write(file_name, hook_code)
        print 'install local script'

#class InstalledHook(Hook):
#
#    def __init__(self, _contents_path, _hooktype):
#        Hook.__init__(self, _contents_path, _hooktype)
#
#    def install(self, git_hook_dir):
#        full_path = path.join(self.install_dir, contents_path.split('/')[-1])
#        copyfile(contents_path, full_path)

class HookContent(object):
    __slots__ = ('name', 'description')

#TODO 気が向いたらモジュールにわける
class Gist(object):

    api_base = 'https://api.github.com/gists/'

    def __init__(self, gistid):
        self.gist_info = None
        self.files_key = None

        self.gistid = gistid
        self._initialize()

    def _initialize(self):
        gistapi_json = requests.get(self.api_base + self.gistid).content
        self.gist_info = json.loads(gistapi_json)
        print 'installing from gist... ...'
        self.files_key = self.gist_info[u'files'].keys()[0]

    def get_description(self):
        return self.gist_info[u'description']

    def get_filename(self):
        return self.files_key

    def get_raw_url(self):
        """ Warning: Even if the gist have files, get only head of files. """

        return self.gist_info[u'files'][self.files_key][u'raw_url']




