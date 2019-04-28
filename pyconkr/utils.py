#!/usr/bin/env python

from configparser import ConfigParser


def load_permitted_settings_from_ini(inifile):
    PERMITTED_SETTINGS = ["EMAIL_USE_TLS", "EMAIL_HOST", "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD",
                          "EMAIL_PORT", "SLACK_TOKEN", "IMP_KEY", "IMP_SECRET"]
    from django.conf import settings
    configured = {}
    try:
        config = ConfigParser()
        config.read_file(open(inifile))
    except:
        return None
    for section_name in config.sections():
        for key in config[section_name]:
            setting_name = key.upper()
            if setting_name in PERMITTED_SETTINGS:
                value = config[section_name][key]
                setattr(settings, setting_name, value)
                configured[setting_name] = value
    return configured
