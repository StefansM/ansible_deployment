#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os.path

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        services=dict(type='dict', required=True),
        deploy_root=dict(type='str', required=True),
    )


    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    result = dict(changed=False)
    result.update(module.params)

    for service_name, service in module.params["services"].items():
        final_dir = service_name + "_" + str(service["version"])

        service["dest_dir"] = os.path.join(
                module.params["deploy_root"],
                "packages",
                service_name,
                final_dir)

        service["prefix"] = os.path.join(
                module.params["deploy_root"],
                "deployments",
                "current",
                service_name,
                final_dir)

    result["ansible_facts"] = {"services": module.params["services"]}
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
