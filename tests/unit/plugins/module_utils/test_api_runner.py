# -*- coding: utf-8 -*-
# (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.community.general.plugins.module_utils.api_runner import APIRunner
from httmock import response
from httmock import with_httmock
from httmock import urlmatch
import pytest


_test_netloc = r'.*testdomain.com'


@urlmatch(netloc=_test_netloc, path='/api/V8/hello')
def hello_resp(url, request):
    return response(request=request, content='Hello World!', headers={'content-type': 'text/plain; charset=utf-8'})


@with_httmock(hello_resp)
def test_simple_get(mocker):
    module = mocker.Mock()
    runner = APIRunner('http://test.testdomain.com/api/V8', module, use_json=False)

    with runner() as ctx:
        result = ctx.get('/hello')
        assert result.text == 'Hello World!'
