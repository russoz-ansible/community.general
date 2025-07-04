# -*- coding: utf-8 -*-
# Copyright (c) 2017, Edward Nunez <edward.nunez@cyberark.com>
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
author: Unknown (!UNKNOWN)
name: cyberarkpassword
short_description: Get secrets from CyberArk AIM
requirements:
  - CyberArk AIM tool installed
description:
  - Get secrets from CyberArk AIM.
options:
  _command:
    description: Cyberark CLI utility.
    type: string
    env:
      - name: AIM_CLIPASSWORDSDK_CMD
    default: '/opt/CARKaim/sdk/clipasswordsdk'
  appid:
    description: Defines the unique ID of the application that is issuing the password request.
    type: string
    required: true
  query:
    description: Describes the filter criteria for the password retrieval.
    type: string
    required: true
  output:
    description:
      - Specifies the desired output fields separated by commas.
      - 'They could be: Password, PassProps.<property>, PasswordChangeInProcess.'
    type: string
    default: 'password'
  _extra:
    description: For extra_params values please check parameters for clipasswordsdk in CyberArk's "Credential Provider and
      ASCP Implementation Guide".
notes:
  - For Ansible on Windows, please change the -parameters (C(-p), C(-d), and C(-o)) to /parameters (C(/p), C(/d), and C(/o))
    and change the location of C(CLIPasswordSDK.exe).
"""

EXAMPLES = r"""
- name: passing options to the lookup
  ansible.builtin.debug:
    msg: '{{ lookup("community.general.cyberarkpassword", cyquery) }}'
  vars:
    cyquery:
      appid: "app_ansible"
      query: "safe=CyberArk_Passwords;folder=root;object=AdminPass"
      output: "Password,PassProps.UserName,PassProps.Address,PasswordChangeInProcess"


- name: used in a loop
  ansible.builtin.debug:
    msg: "{{item}}"
  with_community.general.cyberarkpassword:
    appid: 'app_ansible'
    query: 'safe=CyberArk_Passwords;folder=root;object=AdminPass'
    output: 'Password,PassProps.UserName,PassProps.Address,PasswordChangeInProcess'
"""

RETURN = r"""
_result:
  description: A list containing one dictionary.
  type: list
  elements: dictionary
  contains:
    password:
      description:
        - The actual value stored.
    passprops:
      description: Properties assigned to the entry.
      type: dictionary
    passwordchangeinprocess:
      description: Did the password change?
"""

import os
import subprocess
from subprocess import PIPE
from subprocess import Popen

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.common.text.converters import to_bytes, to_native
from ansible.utils.display import Display

display = Display()

CLIPASSWORDSDK_CMD = os.getenv('AIM_CLIPASSWORDSDK_CMD', '/opt/CARKaim/sdk/clipasswordsdk')


class CyberarkPassword:

    def __init__(self, appid=None, query=None, output=None, **kwargs):

        self.appid = appid
        self.query = query
        self.output = output

        # Support for Generic parameters to be able to specify
        # FailRequestOnPasswordChange, Queryformat, Reason, etc.
        self.extra_parms = []
        for key, value in kwargs.items():
            self.extra_parms.append('-p')
            self.extra_parms.append(f"{key}={value}")

        if self.appid is None:
            raise AnsibleError("CyberArk Error: No Application ID specified")
        if self.query is None:
            raise AnsibleError("CyberArk Error: No Vault query specified")

        if self.output is None:
            # If no output is specified, return at least the password
            self.output = "password"
        else:
            # To avoid reference issues/confusion to values, all
            # output 'keys' will be in lowercase.
            self.output = self.output.lower()

        self.b_delimiter = b"@#@"  # Known delimiter to split output results

    def get(self):

        result_dict = {}

        try:
            all_parms = [
                CLIPASSWORDSDK_CMD,
                'GetPassword',
                '-p', f'AppDescs.AppID={self.appid}',
                '-p', f'Query={self.query}',
                '-o', self.output,
                '-d', self.b_delimiter]
            all_parms.extend(self.extra_parms)

            b_credential = b""
            b_all_params = [to_bytes(v) for v in all_parms]
            tmp_output, tmp_error = Popen(b_all_params, stdout=PIPE, stderr=PIPE, stdin=PIPE).communicate()

            if tmp_output:
                b_credential = to_bytes(tmp_output)

            if tmp_error:
                raise AnsibleError(f"ERROR => {tmp_error} ")

            if b_credential and b_credential.endswith(b'\n'):
                b_credential = b_credential[:-1]

            output_names = self.output.split(",")
            output_values = b_credential.split(self.b_delimiter)

            for i in range(len(output_names)):
                if output_names[i].startswith("passprops."):
                    if "passprops" not in result_dict:
                        result_dict["passprops"] = {}
                    output_prop_name = output_names[i][10:]
                    result_dict["passprops"][output_prop_name] = to_native(output_values[i])
                else:
                    result_dict[output_names[i]] = to_native(output_values[i])

        except subprocess.CalledProcessError as e:
            raise AnsibleError(e.output)
        except OSError as e:
            raise AnsibleError(f"ERROR - AIM not installed or clipasswordsdk not in standard location. ERROR=({e.errno}) => {e.strerror} ")

        return [result_dict]


class LookupModule(LookupBase):

    """
    USAGE:

    """

    def run(self, terms, variables=None, **kwargs):
        display.vvvv(f"{terms}")
        if isinstance(terms, list):
            return_values = []
            for term in terms:
                display.vvvv(f"Term: {term}")
                cyberark_conn = CyberarkPassword(**term)
                return_values.append(cyberark_conn.get())
            return return_values
        else:
            cyberark_conn = CyberarkPassword(**terms)
            result = cyberark_conn.get()
            return result
