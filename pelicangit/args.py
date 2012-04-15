import argparse

# Look to import this function from pelican module when pelican 3 is released.
# Dupe it here for now for backwards compatibility with versions 2.x of pelican
def parse_arguments():
    parser = argparse.ArgumentParser(description="""A tool to generate a
    static blog, with restructured text input files.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    parser.add_argument(dest='path', nargs='?', help="Path where to find content files", default=None)
    parser.add_argument('-s', '--settings', dest='settings', help='The settings of the application.')
        
    return parser.parse_args()