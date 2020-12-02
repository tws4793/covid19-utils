import argparse
from .actions import generate_list

def arguments():
    parser = argparse.ArgumentParser(
        prog = 'covid19',
        description = 'Utilities for COVID-19 from MOH',
        allow_abbrev = False
    )

    argument_group_operations(parser)
    argument_group_figures(parser)
    argument_group_url(parser)

    return parser

def argument_group_operations(parser):
    group = parser.add_argument_group('Operations', 'Operations')

    group.add_argument(
        '-d', '--debug',
        help = 'debug mode',
        action = 'store_true'
    )

    group.add_argument(
        '--update',
        help = 'Update',
        action = 'store_true'
    )

    group.add_argument(
        '--generate-report',
        help = 'Generate report',
        action = 'store_false'
    )

    group.add_argument(
        '--generate-urls',
        help = 'Generate an initial list of URLs',
        action = 'store_const',
        const = generate_list
    )

    return group

def argument_group_figures(parser):
    group = parser.add_argument_group('Figures', 'Update figures')

    group.add_argument(
        '--new-community',
        help = 'Number of community cases',
        type = int,
        default = 0
    )

    group.add_argument(
        '--new-dormitory',
        help = 'Number of cases in dormitories',
        type = int,
        default = 0
    )

    group.add_argument(
        '--new-non-dormitory',
        help = 'Number of cases not in dormitories',
        type = int,
        default = 0
    )

    group.add_argument(
        '--new-imported',
        help = 'Number of imported cases',
        type = int,
        default = 0
    )

    group.add_argument(
        '--new-cases-group',
        help = 'Number of new cases, in the order: community, dormitory, imported',
        type = int,
        nargs = 3,
        default = [0, 0, 0],
        metavar = ('COMMUNITY', 'DORMITORY', 'IMPORTED')
    )

    group.add_argument(
        '--total-icu',
        help = 'Total number of cases in critical condition',
        type = int,
        default = 0
    )

    # New Cases
    total = group.add_mutually_exclusive_group()

    total.add_argument(
        '--new-cases',
        help = 'Number of new cases',
        type = int,
        default = 0
    )

    total.add_argument(
        '--total-cases',
        help = 'Total number of cumulative cases',
        type = int,
        default = 0
    )

    # Recoveries
    recovered = group.add_mutually_exclusive_group()

    recovered.add_argument(
        '--new-recovered',
        help = 'Additional number of recovered cases',
        type = int,
        default = 0
    )

    recovered.add_argument(
        '--total-recovered',
        help = 'Total number of recovered cases',
        type = int,
        default = 0
    )

    # Deaths
    deaths = group.add_mutually_exclusive_group()

    deaths.add_argument(
        '--new-deaths',
        help = 'Additional number of deaths',
        type = int,
        default = 0
    )

    deaths.add_argument(
        '--total-deaths',
        help = 'Total number of deaths',
        type = int,
        default = 0
    )

    return group

def argument_group_url(parser):
    group = parser.add_argument_group('Links', 'URLs to Press Releases')

    group.add_argument(
        '--generate-init-list',
        help = 'Generate the initial list'
    )

    return group
