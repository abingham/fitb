"""Extension points to use in tests.
"""

import pytest
import fitb


def report_in_all_caps(message, loud):
    if loud:
        message += "!!!"
    print(message.upper())


def report_in_lower(message):
    print(message.lower())


def calm():
    return "You are in your happy place"


def frantic():
    return "The roof is on fire"


@pytest.fixture()
def reporters():
    # Create the extension point
    reporters = fitb.ExtensionPoint('reporters')

    # Define an "activate" function for all-caps
    def all_caps_extension(full_config, extension_config):
        def report(message):
            report_in_all_caps(message, loud=extension_config['loud'])
        return report

    # Add the all-caps extension. Note that it has a config option.
    reporters.add(
        name='all-caps',
        description='Report in all caps',
        config_options=(fitb.Option(
            name='loud', description='Report loudly', default=False),),
        activate=all_caps_extension)

    # Add the lower extension. Note that it has no config options
    reporters.add(
        name='lower',
        description='Report in lower case',
        activate=lambda full, ext: report_in_lower)

    return reporters


@pytest.fixture()
def generators():
    generators = fitb.ExtensionPoint('generators')

    generators.add(
        name='calm',
        description='A calm message',
        activate=lambda full, ext: calm)

    generators.add(
        name='frantic',
        description='A frantic message',
        activate=lambda full, ext: frantic)

    return generators
