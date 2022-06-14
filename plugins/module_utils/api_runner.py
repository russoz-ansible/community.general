# -*- coding: utf-8 -*-
# (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import traceback
from functools import wraps

import ansible.module_utils.urls as _urls
from ansible.module_utils.six.moves.urllib.parse import urlparse
from ansible.module_utils.common.collections import is_sequence
from ansible.module_utils.six import iteritems


REQUESTS_IMP_ERR = None
try:
    import requests
except ImportError:
    REQUESTS_IMP_ERR = traceback.format_exc()
    REQUESTS_FOUND = False
else:
    REQUESTS_FOUND = True


def _ensure_list(value):
    return list(value) if is_sequence(value) else [value]



class APIRunnerException(Exception):
    pass


class MissingArgumentFormat(APIRunnerException):
    def __init__(self, arg, args_order, args_formats):
        self.args_order = args_order
        self.arg = arg
        self.args_formats = args_formats

    def __repr__(self):
        return "MissingArgumentFormat({0!r}, {1!r}, {2!r})".format(
            self.arg,
            self.args_order,
            self.args_formats,
        )

    def __str__(self):
        return "Cannot find format for parameter {0} {1} in: {2}".format(
            self.arg,
            self.args_order,
            self.args_formats,
        )


class MissingArgumentValue(APIRunnerException):
    def __init__(self, args_order, arg):
        self.args_order = args_order
        self.arg = arg

    def __repr__(self):
        return "MissingArgumentValue({0!r}, {1!r})".format(
            self.args_order,
            self.arg,
        )

    def __str__(self):
        return "Cannot find value for parameter {0} in {1}".format(
            self.arg,
            self.args_order,
        )


class FormatError(APIRunnerException):
    def __init__(self, name, value, args_formats, exc):
        self.name = name
        self.value = value
        self.args_formats = args_formats
        self.exc = exc
        super(FormatError, self).__init__()

    def __repr__(self):
        return "FormatError({0!r}, {1!r}, {2!r}, {3!r})".format(
            self.name,
            self.value,
            self.args_formats,
            self.exc,
        )

    def __str__(self):
        return "Failed to format parameter {0} with value {1}: {2}".format(
            self.name,
            self.value,
            self.exc,
        )


class _ArgFormat(object):
    def __init__(self, func, ignore_none=None):
        self.func = func
        self.ignore_none = ignore_none

    def __call__(self, value, ctx_ignore_none):
        ignore_none = self.ignore_none if self.ignore_none is not None else ctx_ignore_none
        if value is None and ignore_none:
            return []
        f = self.func
        return [str(x) for x in f(value)]


class _Format(object):
    @staticmethod
    def as_bool(args):
        return _ArgFormat(lambda value: _ensure_list(args) if value else [])

    @staticmethod
    def as_bool_not(args):
        return _ArgFormat(lambda value: [] if value else _ensure_list(args), ignore_none=False)

    @staticmethod
    def as_optval(arg, ignore_none=None):
        return _ArgFormat(lambda value: ["{0}{1}".format(arg, value)], ignore_none=ignore_none)

    @staticmethod
    def as_opt_val(arg, ignore_none=None):
        return _ArgFormat(lambda value: [arg, value], ignore_none=ignore_none)

    @staticmethod
    def as_opt_eq_val(arg, ignore_none=None):
        return _ArgFormat(lambda value: ["{0}={1}".format(arg, value)], ignore_none=ignore_none)

    @staticmethod
    def as_list(ignore_none=None):
        return _ArgFormat(_ensure_list, ignore_none=ignore_none)

    @staticmethod
    def as_fixed(args):
        return _ArgFormat(lambda value: _ensure_list(args), ignore_none=False)

    @staticmethod
    def as_func(func, ignore_none=None):
        return _ArgFormat(func, ignore_none=ignore_none)

    @staticmethod
    def as_map(_map, default=None, ignore_none=None):
        return _ArgFormat(lambda value: _ensure_list(_map.get(value, default)), ignore_none=ignore_none)

    @staticmethod
    def as_default_type(_type, arg="", ignore_none=None):
        fmt = _Format
        if _type == "dict":
            return fmt.as_func(lambda d: ["--{0}={1}".format(*a) for a in iteritems(d)],
                               ignore_none=ignore_none)
        if _type == "list":
            return fmt.as_func(lambda value: ["--{0}".format(x) for x in value], ignore_none=ignore_none)
        if _type == "bool":
            return fmt.as_bool("--{0}".format(arg))

        return fmt.as_opt_val("--{0}".format(arg), ignore_none=ignore_none)

    @staticmethod
    def unpack_args(func):
        @wraps(func)
        def wrapper(v):
            return func(*v)
        return wrapper

    @staticmethod
    def unpack_kwargs(func):
        @wraps(func)
        def wrapper(v):
            return func(**v)
        return wrapper


class APIRunner(object):
    """
    Wrapper for ``ansible.module_utils.urls.fetch_url()``.

    It aims to provide a reusable runner with consistent argument formatting
    and sensible defaults.
    """

    def __init__(self, base_url, module=None, use_json=True, **kwargs):

        self.base_url = base_url
        self._module = module
        # self.base_url_parts = urlparse(base_url)
        # if url_params_formats is None:
        #     url_params_formats = {}
        # self.url_params_formats = url_params_formats
        self.use_json = use_json

        # fetch_url_passthrough = ["use_proxy", "force", "last_mod_time", "timeout", "use_gssapi", "unix_socket", "ca_path", "cookies", "unredirected_headers"]
        # self.fetch_url_params = dict(kwargs)

        # for mod_param_name, spec in iteritems(module.argument_spec):
        #     if mod_param_name not in self.arg_formats:
        #         self.arg_formats[mod_param_name] = _Format.as_default_type(spec['type'], mod_param_name)

    @property
    def module(self):
        return self._module

    @module.setter
    def module_set(self, module):
        if self._module is not None:
            raise AttributeError("Cannot re-assign a module to APIRunner instance")
        self._module = module

    def __call__(self, ignore_value_none=True, check_mode_skip=False, check_mode_return=None, **kwargs):
        if self.module is None:
            raise RuntimeError('APIRunner: must set module')
        return _APIRunnerContext(runner=self,
                                 ignore_value_none=ignore_value_none,
                                 check_mode_skip=check_mode_skip,
                                 check_mode_return=check_mode_return, **kwargs)


class _APIRunnerContext(object):
    def __init__(self, runner, ignore_value_none, check_mode_skip, check_mode_return, **kwargs):
        self.runner = runner
        self.ignore_value_none = ignore_value_none
        self.check_mode_skip = check_mode_skip
        self.check_mode_return = check_mode_return

    def get(self, path, **kwargs):
        runner = self.runner
        module = self.runner.module

        url = runner.base_url + path

        return requests.get(url,)


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# fmt = _Format()
