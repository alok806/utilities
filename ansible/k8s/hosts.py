from __future__ import print_function
from yaml import load

with open('inv') as inv:
 x = load(inv)
all_hosts = x['all']['hosts']
with open('roles/hostname/files/hosts', 'w') as hosts_f:
 for ip,host_d in all_hosts.iteritems(): # because Python 2
  print(ip, host_d['hostname'])
  hosts_f.write("{} {}\n".format(ip, host_d['hostname']))
