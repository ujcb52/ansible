#!/usr/bin/env python

'''
Example custom dynamic inventory script for Ansible, in Python.
'''

import os
import sys
import argparse
import httplib2
import configparser

config = configparser.ConfigParser()
config.read('/home/ujcb52/fabric/jw_dailyparam/conf/config.ini')

ccip = config['mgmtsrvlist']['CC'] + ':8111'
passwd = config['farm']['pass']

try:
    import json
except ImportError:
    import simplejson as json

def all_ip(flag=None):
    ipList = []
    url = "http://"+ccip+"/admin/viewAllNode"
    h = httplib2.Http('.cache')
    response, content = h.request(url)
    result = json.loads(content.decode('utf-8'))

    hostNodeList = result['HostNode']

    for host in hostNodeList:
         state = host['state']
         if state == 'normal':
              privateIp = host['privateIp']
              ipList.append(privateIp)

    return ipList

class ExampleInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.example_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);

    # Example inventory for testing.
    def example_inventory(self):
        return {
            'group': {
                'hosts': all_ip(),
                'vars': {
                    'ansible_user': 'ujcb52',
                    'ansible_ssh_pass': passwd,
                    'ansible_port': '22007',
                    'ansible_become': 'yes',
                    'ansible_become_method': 'sudo',
                    'ansible_become_user': 'root',
                    'ansible_become_pass': passwd
                }
            },
            '_meta': {
                'hostvars': {
                    '172.16.143.57': {
                        'host_specific_var': 'foo'
                    },
                    '192.168.28.72': {
                        'host_specific_var': 'bar'
                    }
                }
            }
        }

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
ExampleInventory()
