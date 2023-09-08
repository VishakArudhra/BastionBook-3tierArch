# Bastionbook Ansible Playbooks

This branch is concerned with the two playbooks written for the setup and the continuous deployment of this application - **setup** and **update**.

`bas10book-application-setup.yaml` is for setup and `bas10book-application-update.yaml` is for update.

## Setting Up Dynamic Inventory for Playbook Execution

Constant manual rewriting of the inventory file with different sets of IP addresses is neither practical nor efficient at scale, therefore as a solution is **Dyanmic Inventory**. Follow [this](https://devopscube.com/setup-ansible-aws-dynamic-inventory/) site for reference for setup method.

*Before going for the dynamic inventory configuration, ensure your target instances will launch with a particular tag specific for the purpose of ansible targetting* for e.g., `ansible-managed: true`

1) Write your dynamic inventory file (`aws_ec2.yaml`) and specify your own match configurations to match your target ec2 instances while executing a playbook:

    ``` yaml
    plugin: aws_ec2
    regions:
        - us-west-2
    filters:
        tag:ansible-managed: true
    ```
The path suggested to place your file in, in the hyper-linked walkthrough is: `/opt/ansible/inventory`

2) If you wish so, you can also make this your default inventory by configurig your `ansible.cfg` file in the below manner:

    ``` CONF
    [defaults]
    host_key_checking = False
    inventory = /opt/ansible/inventory/aws_ec2.yaml

    [inventory]
    enable_plugins = aws_ec2
    ```

This way the there won't be a need to worry about the number of the instances to target when executing the ansible-playbook.

For e.g., if you wanted to have your target instances serve the updated application files from the **main** branch, you could just run:

`ansible-playbook bas10book-application-update.yaml` 

and ansible would automatically retrieve the necessary information from your AWS account to target the right set of EC2 instances. 