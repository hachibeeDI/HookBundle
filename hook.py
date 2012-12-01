#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shutil import copyfile
from os import path

import requests
import json


"""
hook.py
----------

install, description(info), original_path
"""

class Hook(object):
    """ abstract class. This work as hook contents. """

    def __init__(self, install_dir):
        self.install_dir = install_dir

    def install(self, contents_path):
        #TODO あとで
        raise Exception()

    def _write(self, file_name, code):
        with open(path.join(self.install_dir, file_name), 'w') as hook_file:
            hook_file.write(code)


class GistHook(Hook):

    def __init__(self, install_dir):
        Hook.__init__(self, install_dir)

    def install(self, contents_path):
        gist = Gist(contents_path)
        raw_url = gist.get_raw_url()
        print u'get from raw-url: %s\n' % raw_url
        print u'description: %s\n' % gist.get_description()
        hook_code = requests.get(raw_url).content
        self._write(gist.get_filename(), hook_code)


class LocalHook(Hook):

    def __init__(self, install_dir):
        Hook.__init__(self,install_dir)

    def install(self, contents_path):
        file_path = contents_path.split('/')[-1]
        copyfile(contents_path, file_path)


class InstalledHook(Hook):

    def __init__(self, install_dir):
        Hook.__init__(self,install_dir)

    def install(self, contents_path):
        full_path = self.install_dir + contents_path.split('/')[-1]
        copyfile(contents_path, full_path)


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




