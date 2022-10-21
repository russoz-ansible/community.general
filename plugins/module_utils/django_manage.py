# -*- coding: utf-8 -*-
# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.community.general.plugins.module_utils.cmd_runner import CmdRunner, cmd_runner_fmt as fmt


def pipx_runner(module, command, **kwargs):
    runner = CmdRunner(
        module,
        command=command,
        arg_formats=dict(

            state=fmt.as_map(_state_map),
            name=fmt.as_list(),
            name_source=fmt.as_func(fmt.unpack_args(lambda n, s: [s] if s else [n])),
            install_deps=fmt.as_bool("--include-deps"),
            inject_packages=fmt.as_list(),
            force=fmt.as_bool("--force"),
            include_injected=fmt.as_bool("--include-injected"),
            index_url=fmt.as_opt_val('--index-url'),
            python=fmt.as_opt_val('--python'),
            _list=fmt.as_fixed(['list', '--include-injected', '--json']),
            editable=fmt.as_bool("--editable"),
            pip_args=fmt.as_opt_val('--pip-args'),
        ),
        environ_update={'USE_EMOJI': '0'},
        check_rc=True,
        **kwargs
    )
    return runner


class CleanupRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(command=('./manage.py', 'cleanup'), arg_formats={}, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order=[], *args, **kwargs)


class CollectStaticRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command=('./manage.py', 'collectstatic'),
            arg_formats=dict(
                database=fmt.as_opt_val('--database'),
                cache_table=fmt.as_list(),
            ),
            *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order='database cache_table', *args, **kwargs)


class CreateCacheTableRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command=('./manage.py', 'createcachetable'),
            arg_formats=dict(
                database=fmt.as_opt_val('--database'),
                cache_table=fmt.as_list(),
            ),
            *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order='database cache_table', *args, **kwargs)


def create_runner(module, command, *args, **kwargs):
    runners = dict(
        cleanup=CleanupRunner,
        createcachetable=CreateCacheTableRunner,
    )

    return runners[command](module, *args, **kwargs)
