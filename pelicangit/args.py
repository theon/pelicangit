import argparse

# Look to import these function from pelican module down the line.
# Dupe it here for now for backwards compatibility with older versions of pelican
def parse_arguments():
    parser = argparse.ArgumentParser(description="""A tool to generate a
    static blog, with restructured text input files.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    parser.add_argument(dest='path', nargs='?', help="Path where to find content files", default=None)
    parser.add_argument('-s', '--settings', dest='settings',
        help='The settings of the application.')
        
    return parser.parse_args()