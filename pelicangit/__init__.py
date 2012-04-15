from pelicangit.githook import *
from pelicangit.args import parse_arguments
from pelicangit.log import setup_logging
from pelican import read_settings
import logging
import os
import pwd

logger = logging.getLogger('pelicangit')

def main():
    
    args = parse_arguments()
    settings = read_settings(args.settings)
   
    user = settings['PELICANGIT_USER']
    change_user(user)
    
    setup_logging()
    
    source_repo = GitRepo(
        settings['PELICANGIT_SOURCE_REPO'],
        settings['PELICANGIT_SOURCE_REMOTE'],
        settings['PELICANGIT_SOURCE_BRANCH']
    )

    deploy_repo = GitRepo(
        settings['PELICANGIT_DEPLOY_REPO'],
        settings['PELICANGIT_DEPLOY_REMOTE'],
        settings['PELICANGIT_DEPLOY_BRANCH']
    )

    whitelisted_files = settings['PELICANGIT_WHITELISTED_FILES']

    port = settings['PELICANGIT_PORT']

    httpd = GitHookServer(('', port), GitHookRequestHandler, source_repo, deploy_repo, whitelisted_files)
    logger.info("PelicanGit listening on port " + str(port))
    httpd.serve_forever()
    
def change_user(user):
    pw_record = pwd.getpwnam(user)
    os.setgid(pw_record.pw_uid)
    os.setuid(pw_record.pw_gid)
