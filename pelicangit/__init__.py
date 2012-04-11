from pelicangit.githook import *
from pelican import read_settings
from pelicangit.args import parse_arguments

def main():
    
    PORT = 8080

    args = parse_arguments()
    settings = read_settings(args.settings)

    source_repo = GitRepo(
        settings['SOURCE_GIT_REPO'],
        settings['SOURCE_GIT_REMOTE'],
        settings['SOURCE_GIT_BRANCH']
    )

    deploy_repo = GitRepo(
        settings['DEPLOY_GIT_REPO'],
        settings['DEPLOY_GIT_REMOTE'],
        settings['DEPLOY_GIT_BRANCH']
    )

    whitelisted_files = settings['GIT_WHITELISTED_FILES']

    httpd = GitHookServer(('', PORT), GitHookRequestHandler, source_repo, deploy_repo, whitelisted_files)
    print "PelicanGit listening on port", PORT
    httpd.serve_forever()
