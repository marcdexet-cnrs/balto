""" Config parsing utilities
"""
import json

from balto.suite import TestSuite


def read_config(config_filepath, em):
    with open(config_filepath, 'r') as config_file:
        raw_config = json.load(config_file)

    return parse_config(raw_config, em)


def parse_config(config, em):
    if not isinstance(config, list):
        config = [config]

    test_suites = dict()

    for suite_id, suite_config in enumerate(config):
        suite_name = suite_config.pop('name', "Suite %d" % (suite_id + 1))
        test_suites[suite_name] = TestSuite(suite_name, **suite_config, em=em)

    return test_suites
