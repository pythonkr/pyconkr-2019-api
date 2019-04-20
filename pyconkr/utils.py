#!/usr/bin/env python

import os, sys
from configparser import ConfigParser


def load_from_ini(inifile):
    from django.conf import settings
    config_dict = {}
    try:
        config = ConfigParser()
        config.read_file(open(inifile))
    except:
        return None
    for section_name in config.sections():
        section_kv = {}
        for key in config[section_name]:
            value = config[section_name][key]
            section_kv[key.upper()] = value
        if len(section_kv) > 0:
            if not hasattr(settings, section_name):
                setattr(settings, section_name, section_kv)
            config_dict[section_name] = section_kv
    return config_dict


