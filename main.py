#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hooks.hook import configuration_parser
from hooks.install import Installer
from rcmanager.loader import SettingFile

def main():
    installer = Installer()
    setting_file = SettingFile()
    #fixme
    for line in setting_file.get_lines():
        for li in line:
            hook = configuration_parser(li)
            installer.install(hook)
    installer.ch_script_mode()

if __name__ == '__main__':
    main()

