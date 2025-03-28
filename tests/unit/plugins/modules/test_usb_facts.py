# Copyright (c) Ansible project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.internal_test_tools.tests.unit.compat import mock
from ansible_collections.community.internal_test_tools.tests.unit.compat import unittest
from ansible.module_utils import basic
from ansible_collections.community.general.plugins.modules import usb_facts
from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import AnsibleExitJson, set_module_args, exit_json, fail_json


def get_bin_path(self, arg, required=False):
    """Mock AnsibleModule.get_bin_path"""
    if arg == 'lsusb':
        return '/usr/bin/lsusb'
    else:
        if required:
            fail_json(msg='%r not found !' % arg)


class TestUsbFacts(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = mock.patch.multiple(basic.AnsibleModule,
                                                      exit_json=exit_json,
                                                      fail_json=fail_json,
                                                      get_bin_path=get_bin_path)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)
        self.testing_data = [
            {
                "input": "Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub",
                "bus": "001",
                "device": "001",
                "id": "1d6b:0002",
                "name": "Linux Foundation 2.0 root hub"
            },
            {
                "input": "Bus 003 Device 002: ID 8087:8008 Intel Corp. Integrated Rate Matching Hub",
                "bus": "003",
                "device": "002",
                "id": "8087:8008",
                "name": "Intel Corp. Integrated Rate Matching Hub"
            }
        ]
        self.output_fields = ["bus", "device", "id", "name"]

    def test_parsing_single_line(self):
        for data in self.testing_data:
            with mock.patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
                command_output = data["input"]
                mock_run_command.return_value = 0, command_output, None
                with self.assertRaises(AnsibleExitJson) as result:
                    with set_module_args({}):
                        usb_facts.main()
                for output_field in self.output_fields:
                    self.assertEqual(result.exception.args[0]["ansible_facts"]["usb_devices"][0][output_field], data[output_field])

    def test_parsing_multiple_lines(self):
        input = ""
        for data in self.testing_data:
            input += ("%s\n" % data["input"])
        with mock.patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            mock_run_command.return_value = 0, input, None
            with self.assertRaises(AnsibleExitJson) as result:
                with set_module_args({}):
                    usb_facts.main()
            for index in range(0, len(self.testing_data)):
                for output_field in self.output_fields:
                    self.assertEqual(result.exception.args[0]["ansible_facts"]["usb_devices"][index][output_field],
                                     self.testing_data[index][output_field])
