#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.utils.display import Display

import datetime
import glob
import os
import os.path
import tempfile

def find_files(root_dir):
    out = {"files": [], "dirs": []}

    for dirpath, dirnames, dirfiles in os.walk(root_dir, followlinks=True):
        out["files"].extend(sorted([
            os.path.relpath(os.path.join(dirpath, f), root_dir)
            for f in dirfiles]))

        out["dirs"].extend(sorted([
            os.path.relpath(os.path.join(dirpath, d), root_dir)
            for d in dirnames]))

    out["files"] = set(out["files"])
    out["dirs"] = set(out["dirs"])
    return out

def deployment_dir(deploy_root):
    deployment_dirs = os.path.join(deploy_root, "deployments")

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    deployments_glob = os.path.join(deployment_dirs, "deployment-%s-*" % date)
    deployments = glob.glob(deployments_glob)

    counter = 0
    if deployments:
        counter = 1 + max([int(d.rsplit("-", 1)[-1]) for d in deployments])

    current_deployment = "deployment-%s-%02d" % (date, counter)
    return os.path.join(deployment_dirs, current_deployment)

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

    services = module.params["services"]
    deploy_root = module.params["deploy_root"]

    current_deploy = os.path.join(deploy_root, "deployments", "current")

    # Files from original deployment
    existing_files = {}
    if os.path.exists(current_deploy):
        existing_files = find_files(current_deploy)

    # File name of the new deployment
    new_deploy_dir = deployment_dir(deploy_root)
    os.makedirs(new_deploy_dir)

    for service_name, service in services.items():
        version = str(service["version"])

        parent = os.path.join(new_deploy_dir, service_name)
        link = os.path.join(parent, service_name + "_" + version)

        os.mkdir(parent)
        os.symlink(service["dest_dir"], link)

    new_files = find_files(new_deploy_dir)

    # Create temporary symlink and rename it into final symlink
    tmp_link = current_deploy + "-tmp"
    if os.path.exists(tmp_link):
        os.unlink(tmp_link)

    os.symlink(new_deploy_dir, tmp_link)
    os.rename(tmp_link, current_deploy)

    changed = new_files != existing_files
    result = dict(changed=changed)
    result["old"] = existing_files
    result["new"] = new_files
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
