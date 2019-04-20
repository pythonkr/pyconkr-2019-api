#!/usr/bin/env python

import pytest
import textwrap

from .utils import load_permitted_settings_from_ini

def test_load_permitted_settings_from_ini(tmpdir, settings):
    inifile = tmpdir.join("test.ini")
    inifile.write(textwrap.dedent("""
    [SMTP]
    EMAIL_HOST_PASSWORD=PaSSw$SX
    EMAIL_PORT=42
    VERY_SECRET_PASSWORD=Diversity$$"""))
    assert inifile.check()
    configured_settings = load_permitted_settings_from_ini(inifile.open().name)
    assert len(configured_settings) == 2
    assert 'EMAIL_HOST_PASSWORD' in configured_settings
    assert 'VERY_SECRET_PASSWORD' not in configured_settings
    assert hasattr(settings, "EMAIL_HOST_PASSWORD") is True
    assert hasattr(settings, "VERY_SECRET_PASSWORD") is False
    assert settings.EMAIL_HOST_PASSWORD == 'PaSSw$SX'
    assert settings.EMAIL_PORT == '42'
