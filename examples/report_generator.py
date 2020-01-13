"""A simple example of how to use fitb.
"""

import argparse

import fitb

# These two functions are the core "reporting" implementations. They will be exposed to the larger program via extension
# points.


def report_in_all_caps(message, loud):
    if loud:
        message += "!!!"
    print(message.upper())


def report_in_lower(message):
    print(message.lower())


# These function define our message generation implementations.


def calm():
    return "You are in your happy place"


def frantic():
    return "The roof is on fire"


# This creates an extension point and adds the two reporting functions to it as extensions.
def configure_extensions():
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

    # Do the same for message generators
    generators = fitb.ExtensionPoint('generators')

    generators.add(
        name='calm',
        description='A calm message',
        activate=lambda full, ext: calm)

    generators.add(
        name='frantic',
        description='A frantic message',
        activate=lambda full, ext: frantic)

    return reporters, generators


def parse_command_line():
    report_parser = argparse.ArgumentParser()
    report_parser.add_argument('reporter')
    report_parser.add_argument('generator')
    report_parser.add_argument('--loud', action='store_true')

    return report_parser.parse_args()


def main():
    args = parse_command_line()

    # Get the reporters ExtensionPoint
    reporters, generators = configure_extensions()

    # Get the default configuration for the ExtensionPoint
    config = fitb.default_config(reporters, generators)

    # At this point you could modify `config`, perhaps based on command line flags or saves configuration information.
    config['reporters']['all-caps']['loud'] = args.loud

    print('config:', config)
    print('available reporters:', list(reporters))
    print('available generators:', list(generators))

    # Get the reporter the user requested
    reporter = reporters.activate(args.reporter, config)

    # Generate a report
    message = generators.activate(args.generator, config)()
    reporter(message)


if __name__ == '__main__':
    main()
