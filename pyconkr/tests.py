#!/usr/bin/env python

import pytest
import textwrap

from .utils import load_from_ini

def test_load_from_ini(tmpdir, settings):
    inifile = tmpdir.join("test.ini")
    inifile.write(textwrap.dedent("""
    [SMTP]
    SECRET=1
    USER=testUser"""))
    assert inifile.check()
    loaded_config = load_from_ini(inifile.open().name)
    assert loaded_config != None
    assert 'SMTP' in loaded_config
    assert hasattr(settings, "SMTP") is True
    assert "USER" in settings.SMTP
    assert settings.SMTP["USER"] == "testUser"
