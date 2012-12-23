#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hook import configuration_parser
from install import Installer
from rcmanager.loader import SettingFile

def main():
    installer = Installer()
    setting_file = SettingFile()
    #TODO
    for line in setting_file.get_lines():
        for li in line:
            hook = configuration_parser(li)
            installer.install(hook)

if __name__ == '__main__':
    main()

