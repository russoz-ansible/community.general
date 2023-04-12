# -*- coding: utf-8 -*-
# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.community.general.plugins.module_utils.cmd_runner import CmdRunner, cmd_runner_fmt as fmt


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


class FlushRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command=('./manage.py', 'flush'),
            arg_formats=dict(
                database=fmt.as_opt_val('--database'),
                cache_table=fmt.as_list(),
            ),
            *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order='database', *args, **kwargs)


class LoadDataRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command=('./manage.py', 'loaddata'),
            arg_formats=dict(
                database=fmt.as_opt_val('--database'),
                cache_table=fmt.as_list(),
            ),
            *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order='database', *args, **kwargs)


class MigrateRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command=('./manage.py', 'migrate'),
            arg_formats=dict(
                database=fmt.as_opt_val('--database'),
                cache_table=fmt.as_list(),
            ),
            *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order='database', *args, **kwargs)


class SyncDBRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command=('./manage.py', 'syncdb'),
            arg_formats=dict(
                database=fmt.as_opt_val('--database'),
                cache_table=fmt.as_list(),
            ),
            *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order='database', *args, **kwargs)


class ValidateRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command=('./manage.py', 'validate'),
            arg_formats=dict(
                database=fmt.as_opt_val('--database'),
                cache_table=fmt.as_list(),
            ),
            *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order='database', *args, **kwargs)


class DefaultRunner(CmdRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command=('./manage.py', 'flush'),
            arg_formats=dict(
                database=fmt.as_opt_val('--database'),
                cache_table=fmt.as_list(),
            ),
            *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(args_order='command', *args, **kwargs)


def create_runner(module, command, *args, **kwargs):
    runners = dict(
        cleanup=CleanupRunner,
        collectstatic=CollectStaticRunner,
        createcachetable=CreateCacheTableRunner,
        flush=FlushRunner,
        loaddata=LoadDataRunner,
        migrate=MigrateRunner,
        syncdb=SyncDBRunner,
        validate=ValidateRunner,
    )
    runner = runners.get(command, DefaultRunner)

    return runner(module, *args, **kwargs)
