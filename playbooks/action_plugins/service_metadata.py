from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import constants as C
from ansible.plugins.action import ActionBase
from ansible.utils.vars import merge_hash
from ansible.errors import AnsibleError

import pprint

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        self._supports_async = False
        results = super(ActionModule, self).run(tmp, task_vars)

        if not results.get("skipped"):
            if "services" not in task_vars:
                raise AnsibleError("`services' not defined in host_vars.")

            results = merge_hash(
                results,
                self._execute_module(
                    module_args=merge_hash(
                        {"services": task_vars["services"]},
                        self._task.args),
                    task_vars=task_vars))

        return results

        return self._execute_module(
                module_name='command',
                module_args={"argv": ["echo", "123"]},
                task_vars=task_vars)
