#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Stephan Schwarz <stearz@gmx.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: utm_proxy_auth_profile

author:
  - Stephan Schwarz (@stearz)

short_description: Create, update or destroy reverse_proxy auth_profile entry in Sophos UTM

description:
  - Create, update or destroy a reverse_proxy auth_profile entry in SOPHOS UTM.
  - This module needs to have the REST Ability of the UTM to be activated.
attributes:
  check_mode:
    support: none
  diff_mode:
    support: none

options:
  name:
    type: str
    description:
      - The name of the object that identifies the entry.
    required: true
  aaa:
    type: list
    elements: str
    description:
      - List of references to utm_aaa objects (allowed users or groups).
    required: true
  basic_prompt:
    type: str
    description:
      - The message in the basic authentication prompt.
    required: true
  backend_mode:
    type: str
    description:
      - Specifies if the backend server needs authentication ([Basic|None]).
    default: None
    choices:
      - Basic
      - None
  backend_strip_basic_auth:
    description:
      - Should the login data be stripped when proxying the request to the backend host.
    type: bool
    default: true
  backend_user_prefix:
    type: str
    description:
      - Prefix string to prepend to the username for backend authentication.
    default: ""
  backend_user_suffix:
    type: str
    description:
      - Suffix string to append to the username for backend authentication.
    default: ""
  comment:
    type: str
    description:
      - Optional comment string.
    default: ""
  frontend_cookie:
    type: str
    description:
      - Frontend cookie name.
  frontend_cookie_secret:
    type: str
    description:
      - Frontend cookie secret.
  frontend_form:
    type: str
    description:
      - Frontend authentication form name.
  frontend_form_template:
    type: str
    description:
      - Frontend authentication form template.
    default: ""
  frontend_login:
    type: str
    description:
      - Frontend login name.
  frontend_logout:
    type: str
    description:
      - Frontend logout name.
  frontend_mode:
    type: str
    description:
      - Frontend authentication mode (Form|Basic).
    default: Basic
    choices:
      - Basic
      - Form
  frontend_realm:
    type: str
    description:
      - Frontend authentication realm.
  frontend_session_allow_persistency:
    description:
      - Allow session persistency.
    type: bool
    default: false
  frontend_session_lifetime:
    type: int
    description:
      - Session lifetime.
    required: true
  frontend_session_lifetime_limited:
    description:
      - Specifies if limitation of session lifetime is active.
    type: bool
    default: true
  frontend_session_lifetime_scope:
    type: str
    description:
      - Scope for frontend_session_lifetime (days|hours|minutes).
    default: hours
    choices:
      - days
      - hours
      - minutes
  frontend_session_timeout:
    type: int
    description:
      - Session timeout.
    required: true
  frontend_session_timeout_enabled:
    description:
      - Specifies if session timeout is active.
    type: bool
    default: true
  frontend_session_timeout_scope:
    type: str
    description:
      - Scope for frontend_session_timeout (days|hours|minutes).
    default: minutes
    choices:
      - days
      - hours
      - minutes
  logout_delegation_urls:
    type: list
    elements: str
    description:
      - List of logout URLs that logouts are delegated to.
    default: []
  logout_mode:
    type: str
    description:
      - Mode of logout (None|Delegation).
    default: None
    choices:
      - None
      - Delegation
  redirect_to_requested_url:
    description:
      - Should a redirect to the requested URL be made.
    type: bool
    default: false

extends_documentation_fragment:
  - community.general.utm
  - community.general.attributes
"""

EXAMPLES = r"""
- name: Create UTM proxy_auth_profile
  community.general.utm_proxy_auth_profile:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestAuthProfileEntry
    aaa: [REF_OBJECT_STRING, REF_ANOTHEROBJECT_STRING]
    basic_prompt: "Authentication required: Please login"
    frontend_session_lifetime: 1
    frontend_session_timeout: 1
    state: present

- name: Remove UTM proxy_auth_profile
  community.general.utm_proxy_auth_profile:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestAuthProfileEntry
    state: absent

- name: Read UTM proxy_auth_profile
  community.general.utm_proxy_auth_profile:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestAuthProfileEntry
    state: info
"""

RETURN = r"""
result:
  description: The utm object that was created.
  returned: success
  type: complex
  contains:
    _ref:
      description: The reference name of the object.
      type: str
    _locked:
      description: Whether or not the object is currently locked.
      type: bool
    _type:
      description: The type of the object.
      type: str
    name:
      description: The name of the object.
      type: str
    aaa:
      description: List of references to utm_aaa objects (allowed users or groups).
      type: list
    basic_prompt:
      description: The message in the basic authentication prompt.
      type: str
    backend_mode:
      description: Specifies if the backend server needs authentication ([Basic|None]).
      type: str
    backend_strip_basic_auth:
      description: Should the login data be stripped when proxying the request to the backend host.
      type: bool
    backend_user_prefix:
      description: Prefix string to prepend to the username for backend authentication.
      type: str
    backend_user_suffix:
      description: Suffix string to append to the username for backend authentication.
      type: str
    comment:
      description: Optional comment string.
      type: str
    frontend_cookie:
      description: Frontend cookie name.
      type: str
    frontend_form:
      description: Frontend authentication form name.
      type: str
    frontend_form_template:
      description: Frontend authentication form template.
      type: str
    frontend_login:
      description: Frontend login name.
      type: str
    frontend_logout:
      description: Frontend logout name.
      type: str
    frontend_mode:
      description: Frontend authentication mode (Form|Basic).
      type: str
    frontend_realm:
      description: Frontend authentication realm.
      type: str
    frontend_session_allow_persistency:
      description: Allow session persistency.
      type: bool
    frontend_session_lifetime:
      description: Session lifetime.
      type: int
    frontend_session_lifetime_limited:
      description: Specifies if limitation of session lifetime is active.
      type: bool
    frontend_session_lifetime_scope:
      description: Scope for frontend_session_lifetime (days|hours|minutes).
      type: str
    frontend_session_timeout:
      description: Session timeout.
      type: int
    frontend_session_timeout_enabled:
      description: Specifies if session timeout is active.
      type: bool
    frontend_session_timeout_scope:
      description: Scope for frontend_session_timeout (days|hours|minutes).
      type: str
    logout_delegation_urls:
      description: List of logout URLs that logouts are delegated to.
      type: list
    logout_mode:
      description: Mode of logout (None|Delegation).
      type: str
    redirect_to_requested_url:
      description: Should a redirect to the requested URL be made.
      type: bool
"""

from ansible_collections.community.general.plugins.module_utils.utm_utils import UTM, UTMModule
from ansible.module_utils.common.text.converters import to_native


def main():
    endpoint = "reverse_proxy/auth_profile"
    key_to_check_for_changes = ["aaa", "basic_prompt", "backend_mode", "backend_strip_basic_auth",
                                "backend_user_prefix", "backend_user_suffix", "comment", "frontend_cookie",
                                "frontend_cookie_secret", "frontend_form", "frontend_form_template",
                                "frontend_login", "frontend_logout", "frontend_mode", "frontend_realm",
                                "frontend_session_allow_persistency", "frontend_session_lifetime",
                                "frontend_session_lifetime_limited", "frontend_session_lifetime_scope",
                                "frontend_session_timeout", "frontend_session_timeout_enabled",
                                "frontend_session_timeout_scope", "logout_delegation_urls", "logout_mode",
                                "redirect_to_requested_url"]

    module = UTMModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            aaa=dict(type='list', elements='str', required=True),
            basic_prompt=dict(type='str', required=True),
            backend_mode=dict(type='str', default="None", choices=['Basic', 'None']),
            backend_strip_basic_auth=dict(type='bool', default=True),
            backend_user_prefix=dict(type='str', default=""),
            backend_user_suffix=dict(type='str', default=""),
            comment=dict(type='str', default=""),
            frontend_cookie=dict(type='str'),
            frontend_cookie_secret=dict(type='str', no_log=True),
            frontend_form=dict(type='str'),
            frontend_form_template=dict(type='str', default=""),
            frontend_login=dict(type='str'),
            frontend_logout=dict(type='str'),
            frontend_mode=dict(type='str', default="Basic", choices=['Basic', 'Form']),
            frontend_realm=dict(type='str'),
            frontend_session_allow_persistency=dict(type='bool', default=False),
            frontend_session_lifetime=dict(type='int', required=True),
            frontend_session_lifetime_limited=dict(type='bool', default=True),
            frontend_session_lifetime_scope=dict(type='str', default="hours", choices=['days', 'hours', 'minutes']),
            frontend_session_timeout=dict(type='int', required=True),
            frontend_session_timeout_enabled=dict(type='bool', default=True),
            frontend_session_timeout_scope=dict(type='str', default="minutes", choices=['days', 'hours', 'minutes']),
            logout_delegation_urls=dict(type='list', elements='str', default=[]),
            logout_mode=dict(type='str', default="None", choices=['None', 'Delegation']),
            redirect_to_requested_url=dict(type='bool', default=False)
        )
    )
    try:
        UTM(module, endpoint, key_to_check_for_changes).execute()
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
