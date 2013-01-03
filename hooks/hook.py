#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os import path, mkdir, sep as path_separator

import requests
import json

"""
hook.py
----------

install, description(info), original_path
"""

def configuration_parser(line):
    """ parse dotfile's configration and built Hook object. """
    st = line.rstrip().split(',')
    uri = st[0]
    hooktype = st[1]
    try:
        description = st[2]
    except IndexError:
        print 'no description'

    def build_hook():
        # if there is only numbers, it is gist-id
        #TODO 一旦完成してからもっとまともな実装を
        r = re.compile('^\d+$')
        if r.match(uri):
            return GistHook(uri, hooktype)
        else:
            return LocalHook(uri, hooktype)
    return build_hook()


class HookTimingResolver(object):
    """ judge the hooktype get from setting file is right. """

    # ひとまずこんだけ。ailiasとかはのちのち。もしくは分けるかも
    timing_definitions = [
            u"pre-commit"
            ,u"prepare-commit-msg"
            ,u"commit-msg"
            ,u"post-commit"
            ,u"pre-rebase"
            ,u"post-rebase"
            ,u"post-merge"
            ]

    def __init__(self, hooktiming):
        self.hooktiming = self.__initialize_hook(hooktiming)

    def __initialize_hook(self, hooktiming):
        # そのうちdictとかそういう系にするので
        matchedhook = [h for h in self.timing_definitions if h == hooktiming]
        if len(matchedhook) == 0:
            print u"git has not hooktype such as " + hooktiming
            # TODO InvailedHookTypeExceptionとか
            raise Exception
        return matchedhook[0]

    def dir_name(self):
        return self.hooktiming


class Hook(object):
    """ abstract class.abs.
        This work as hook contents. """

    def __init__(self, _contents_path, _hooktype):
        self._contents_path = _contents_path
        self._hooktype_save_location = HookTimingResolver(_hooktype).dir_name()

    def install(self, git_hook_dir):
        #TODO あとでNotImplementExceptionだか作る
        raise Exception()

    def _write(self, install_path, code):
        sp_tmp = install_path.split(path_separator)
        # 末尾のファイル名を除いた、ディレクトリ名
        targ_dir = path_separator.join([sp_tmp[i] for i in range(1, len(sp_tmp) - 1)])
        if not path.isdir(targ_dir):
            mkdir(targ_dir)
        with open(install_path, 'w') as hook_file:
            hook_file.write(code)

    def _build_fullpath(self, hook_dir, filename):
        return path.join(hook_dir, self._hooktype_save_location, filename)


class GistHook(Hook):

    def __init__(self, _contents_path, _hooktype):
        Hook.__init__(self, _contents_path, _hooktype)

    def install(self, git_hook_dir):
        gist = Gist(self._contents_path)
        raw_url = gist.get_raw_url()
        print u'get from raw-url: %s\n' % raw_url
        print u'description: %s\n' % gist.get_description()
        hook_code = requests.get(raw_url).content
        full_path = self._build_fullpath(git_hook_dir, gist.get_filename())
        self._write(full_path, hook_code)


class LocalHook(Hook):

    def __init__(self, _contents_path, _hooktype):
        Hook.__init__(self, _contents_path, _hooktype)

    def install(self, git_hook_dir):
        hook_code = open(self._contents_path).read()
        full_path = self._build_fullpath(git_hook_dir, self._contents_path.split('/')[-1])
        self._write(full_path, hook_code)
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




