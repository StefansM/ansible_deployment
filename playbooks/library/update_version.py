#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.utils.display import Display
import os.path

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        services=dict(type='dict', required=True),
        service_name=dict(type='str', required=True),
        set=dict(type='dict', required=True),
        delete=dict(type='list', required=False),
    )


    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    services = module.params["services"].copy()
    service_name = module.params["service_name"]
    to_set = module.params["set"]
    to_del = module.params["delete"]

    changed = False
    service = services[service_name]

    # Need to track if the service changes, so don't just call update()
    for key, value in to_set.items():
        if key not in service or service[key] != value:
            changed = True
            service[key] = value

    if to_del is not None:
        for key in to_del:
            changed = True
            del service[key]

    result = dict(
        changed=changed,
        services=services,
        ansible_facts=dict(services=services))
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
