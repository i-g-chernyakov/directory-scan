# -*- coding: utf-8 -*-

import os

import pytest


@pytest.fixture(scope='session')
def fixture_path():
    """Creates full path to fixture """
    def factory(*path_parts):
        this_dir = os.path.dirname(__file__)
        return os.path.join(this_dir, 'fixtures', *path_parts)

    return factory
