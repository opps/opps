#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from django.conf import settings
from django.core import management


settings.configure()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Opps CMS bin file')
    parser.add_argument('operation', help='task to be performed',
                        choices=['startproject'])
    parser.add_argument("project_name", help="Project name", type=str)

    args = parser.parse_args()
    if args.operation == 'startproject':
        management.call_command(
            'startproject', args.project_name,
            template='https://github.com/opps/opps-project-template/zipball/'
            'master',
            extensions=('py', 'md', 'dev')
        )
