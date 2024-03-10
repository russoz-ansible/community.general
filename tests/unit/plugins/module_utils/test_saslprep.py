# -*- coding: utf-8 -*-
# Copyright (c) 2019, Andrey Tuzhilin <andrei.tuzhilin@gmail.com>
# Copyright (c) 2020, Andrew Klychkov (@Andersson007) <aaklychkov@mail.ru>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.general.plugins.module_utils.saslprep import saslprep


VALID = [
    ('', ''),
    ('\u00A0', ' '),
    ('a', 'a'),
    ('й', 'й'),
    ('\u30DE\u30C8\u30EA\u30C3\u30AF\u30B9', '\u30DE\u30C8\u30EA\u30C3\u30AF\u30B9'),
    ('The\u00ADM\u00AAtr\u2168', 'TheMatrIX'),
    ('I\u00ADX', 'IX'),
    ('user', 'user'),
    ('USER', 'USER'),
    ('\u00AA', 'a'),
    ('\u2168', 'IX'),
    ('\u05BE\u00A0\u05BE', '\u05BE\u0020\u05BE'),
]

INVALID = [
    (None, TypeError),
    (b'', TypeError),
    ('\u0221', ValueError),
    ('\u0007', ValueError),
    ('\u0627\u0031', ValueError),
    ('\uE0001', ValueError),
    ('\uE0020', ValueError),
    ('\uFFF9', ValueError),
    ('\uFDD0', ValueError),
    ('\u0000', ValueError),
    ('\u06DD', ValueError),
    ('\uFFFFD', ValueError),
    ('\uD800', ValueError),
    ('\u200E', ValueError),
    ('\u05BE\u00AA\u05BE', ValueError),
]


@pytest.mark.parametrize('source,target', VALID)
def test_saslprep_conversions(source, target):
    assert saslprep(source) == target


@pytest.mark.parametrize('source,exception', INVALID)
def test_saslprep_exceptions(source, exception):
    with pytest.raises(exception) as ex:
        saslprep(source)
