# -*- coding: utf-8 -*-
# (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.community.general.plugins.module_utils.api_runner import APIRunner
from ansible.module_utils.six.moves.urllib.parse import parse_qs, urlparse

from httmock import response
from httmock import with_httmock
from httmock import urlmatch
import pytest


_test_netloc = r'.*testdomain.com'


def _assert_urls_equal(url1, url2):
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)
    assert parsed1.scheme == parsed2.scheme
    assert parsed1.netloc == parsed2.netloc
    assert parsed1.path == parsed2.path
    assert parsed1.params == parsed2.params
    assert parse_qs(parsed1.query) == parse_qs(parsed2.query)
    assert parsed1.fragment == parsed2.fragment


@urlmatch(netloc=_test_netloc, path='/api/V8/hello')
def hello_resp(url, request):
    return response(request=request, content='Hello World!', headers={'content-type': 'text/plain; charset=utf-8'})


@with_httmock(hello_resp)
def test_simple_get(mocker):
    module = mocker.Mock()
    runner = APIRunner('http://test.testdomain.com/api/V8', module, use_json=False)

    with runner('/hello') as ctx:
        result = ctx.get()
        assert result.text == 'Hello World!'


@urlmatch(netloc=_test_netloc, path='/api/V8/hello_params')
def hello_params_resp(url, request):
    qs = parse_qs(url.query)
    content = 'Hello World Params!\n\n'
    content = content + '\n'.join('{0}: {1}'.format(k, qs[k][0] if len(qs[k]) == 1 else qs[k]) for k in sorted(qs))
    return response(request=request, content=content, headers={'content-type': 'text/plain; charset=utf-8'})


@with_httmock(hello_params_resp)
def test_simple_params(mocker):
    module = mocker.Mock()
    runner = APIRunner('http://test.testdomain.com/api/V8', module, use_json=False)

    with runner('/hello_params') as ctx:
        result = ctx.get(a=1, b="bananas", c="text with space")

        _assert_urls_equal(result.url, r'http://test.testdomain.com/api/V8/hello_params?a=1&b=bananas&c=text+with+space')
        assert result.text == 'Hello World Params!\n\na: 1\nb: bananas\nc: text with space', result.text

        result2 = ctx.get(e='potatoes', d=[1, 2])
        _assert_urls_equal(result2.url, r'http://test.testdomain.com/api/V8/hello_params?e=potatoes&d=1&d=2')
        assert result2.text == "Hello World Params!\n\nd: ['1', '2']\ne: potatoes", result2.text
