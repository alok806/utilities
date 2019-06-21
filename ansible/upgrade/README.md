# Upgrading a "_hard way_" k8s cluster

## Setup

The setup comprises of a kubernetes cluster that has been brought up the [hard way](https://github.com/kelseyhightower/kubernetes-the-hard-way). This setup is a bit _hard-er_ because it varies a little bit:

1. CentOS 7.6 VMs running on vSphere 6.5
2. Behind corporate proxy, which makes everything harder anyway
3. Two masters/etcd based on the setup [here](https://github.com/mmumshad/kubernetes-the-hard-way)

> Disclaimer: Not to be used in production

## Procedure

Tested on Ansible 2.8

`ansible-playbook -i inv upgrade.yml` 