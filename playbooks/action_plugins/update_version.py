from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import constants as C
from ansible.plugins.action import ActionBase
from ansible.utils.vars import merge_hash
from ansible.errors import AnsibleError

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        self._supports_async = False
        results = super(ActionModule, self).run(tmp, task_vars)

        if "services" not in self._task.args and "services" in task_vars:
            self._task.args["services"] = task_vars["services"]

        if results.get("skipped"):
            return results

        return self._execute_module(task_vars=task_vars)
