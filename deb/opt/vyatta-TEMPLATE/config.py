#!/usr/bin/env python3
import os

from sys import exit

from vyos.config import Config
from vyos.configdict import dict_merge
from vyos.configverify import verify_vrf
from vyos.util import call
from vyos.template import render
from vyos import ConfigError
from vyos import airbag
from jinja2 import Template


airbag.enable()

config_file = r'/etc/default/TEMPLATE'

def get_config(config=None):
    if config:
        conf = config
    else:
        conf = Config()
    base = ['service', 'monitoring', 'TEMPLATE']
    if not conf.exists(base):
        return None

    template_config = conf.get_config_dict(base, get_first_key=True)

    return template_config

def verify(template_config):
    if template_config is None:
        return None

    verify_vrf(template_config)
    return None

def generate(template_config):
    if template_config is None:
        if os.path.isfile(config_file):
            os.unlink(config_file)
        return None

    with open('/opt/vyatta-TEMPLATE/config.j2', 'r') as tmpl, open(config_file, 'w') as out:
        template = Template(tmpl.read()).render(data=template_config)
        out.write(template)

    # Reload systemd manager configuration
    call('systemctl daemon-reload')

    return None

def apply(template_config):
    if node_exporter is None:
        # template_config is removed in the commit
        call('systemctl stop TEMPLATE.service')
        return None

    call('systemctl restart TEMPLATE.service')
    return None

if __name__ == '__main__':
    try:
        c = get_config()
        verify(c)
        generate(c)
        apply(c)
    except ConfigError as e:
        print(e)
        exit(1)
