#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import datetime

config_path = '/boot/wifi_config.txt'
interface_path = '/etc/network/interfaces'
replace_needle = '#@@@replace@@@'

def read_wifi_conf():
    with open(config_path) as f:
        return f.read()
    return ''

def conf_status():
    old_conf = ''
    with open(interface_path, 'r') as f:
        old_conf = f.read()
    pre, cnt, back = old_conf.split(replace_needle)
    new_conf = '{}{}\n{}{}{}'.format(pre,replace_needle,read_wifi_conf(),replace_needle,back)
    return (not (old_conf == new_conf)), new_conf

def write_interface(cnt):
    with open(interface_path, 'w') as f:
        f.write(cnt)


if __name__ == '__main__':
    need, conf = conf_status() 
    cmt = ''
    if(need):
        write_interface(conf)
        cmt = os.popen("service networking restart").read()
    
    ifconfig = os.popen('ifconfig').read()

    with open('/tmp/mystartup.log','a+') as f:
        f.write('\n%s:%s\n' % (datetime.datetime.now(), cmt))
        f.write('%s\n' % ifconfig)
    with open('/boot/mystartup.log','a+') as f:
        f.write('\n%s:%s\n' % (datetime.datetime.now(), cmt))
        f.write('%s\n' % ifconfig)
    os.system('/usr/lib/autossh/autossh -M 20000 -N -R 19998:localhost:22 -p remote_port root@remote_ip &')
    print 'I am working....'

