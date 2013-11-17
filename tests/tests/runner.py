#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django_coverage.coverage_runner import CoverageRunner


class Runner(CoverageRunner):
    def build_suite(self, *args, **kwargs):
        suite = super(Runner, self).build_suite(*args, **kwargs)
        tests = []
        for case in suite:
            pkg = case.__class__.__module__.split('.')[0]
            if pkg in ['opps']:
                tests.append(case)
        suite._tests = tests
        return suite
