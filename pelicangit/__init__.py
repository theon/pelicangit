from pelicangit.githook import *
from pelican import read_settings
from pelicangit.args import parse_arguments
import logging

def main():
    
    logging.basicConfig(filename='/var/log/pelicangit.log', level=logging.DEBUG)
    
    args = parse_arguments()
    settings = read_settings(args.settings)

    source_repo = GitRepo(
        settings['PELICANGIT_SOURCE_REPO'],
        settings['PELICANGIT_SOURCE_REMOTE'],
        settings['PELICANGIT_SOURCE_BRANCH'],
        settings['PELICANGIT_SOURCE_USER']
    )

    deploy_repo = GitRepo(
        settings['PELICANGIT_DEPLOY_REPO'],
        settings['PELICANGIT_DEPLOY_REMOTE'],
        settings['PELICANGIT_DEPLOY_BRANCH'],
        settings['PELICANGIT_DEPLOY_USER']
    )

    whitelisted_files = settings['PELICANGIT_WHITELISTED_FILES']

    port = settings['PELICANGIT_PORT']

    httpd = GitHookServer(('', port), GitHookRequestHandler, source_repo, deploy_repo, whitelisted_files)
    print "PelicanGit listening on port", port
    httpd.serve_forever()
