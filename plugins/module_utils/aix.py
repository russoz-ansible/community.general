# -*- coding: utf-8 -*-
# Copyright (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.community.general.plugins.module_utils.cmd_runner import CmdRunner, cmd_runner_fmt
from itertools import repeat, chain

def crfs_runner_ctx(module):

    runner = CmdRunner(
        module,
        command=["crfs", "-v"],
        arg_formats=dict(
            fs_type=cmd_runner_fmt.as_list(),
            filesystem=cmd_runner_fmt.as_opt_val("-m"),
            vg=cmd_runner_fmt.as_opt_val("-g"),
            device=cmd_runner_fmt.as_opt_val("-d"),
            mount_group=cmd_runner_fmt.as_opt_val("-u"),
            auto_mount=cmd_runner_fmt.as_map({
                True: ["-A", "yes"],
                False: ["-A", "no"],
            }),
            account_subsystem=cmd_runner_fmt.as_map({
                True: ["-t", "yes"],
                False: ["-t", "no"],
            }),
            permissions=cmd_runner_fmt.as_opt_val("-p"),
            size=cmd_runner_fmt.as_func(lambda v: ["-a", "size={0}".format(v)]),
            attributes=cmd_runner_fmt.as_func(lambda v: chain.from_iterable(zip(repeat("-a"), v))),
        ),
        check_rc=False,
    )

    ctx = runner("fs_type vg device filesystem mount_group auto_mount account_subsystem permissions size attributes",
                 check_mode_skip=True, check_mode_return="")
    return ctx
