#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.core import management


settings.configure()
if __name__ == "__main__":
    if sys.argv[1] == 'startproject':
        if len(sys.argv) < 2:
            raise management.CommandError("accepet accepts one argument - the name of the project to create.")
        management.call_command(
            'startproject', sys.argv[2],
            template='https://github.com/opps/opps-project-template/zipball/master',
            extensions=('py', 'md', 'dev')
        )
