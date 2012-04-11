#!/usr/bin/python

import SocketServer
import SimpleHTTPServer
import urllib
import os
import shutil
import re
from pelican import main
from gitbindings import *

PORT = 8080
GET_RESPONSE_BODY = "<h1>PelicanGit is Running</h1>"
POST_RESPONSE_BODY = "<h1>Pelican Project Rebuilt</h1>"
ERROR_RESPONSE_BODY = "<h1>Error</h1>"

source_repo = GitRepo("/work/blog", "origin", "master")
deploy_repo = GitRepo("/work/theon.github.com", "origin", "master")

whitelisted_files = [
    "README.md",
    "googled50a97559ea3af0e.html"
]

class GitHookRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.do_response(GET_RESPONSE_BODY)

    def do_POST(self):
        try:
            #Hard reset both repos so they match the remote (origin) master branches
            self.hard_reset_repos()
            
            # Git Remove all deploy_repo files (except those whitelisted) and then rebuild with pelican
            self.nuke_git_cwd(deploy_repo) 
            main()

            # Add all files newly created by pelican, then commit and push everything
            deploy_repo.add(['.'])

            commit_message = source_repo.log(['-n1', '--pretty="format:%h %B"'])
            deploy_repo.commit(commit_message, ['-a'])
            deploy_repo.push([deploy_repo.origin, deploy_repo.master])

            self.do_response(POST_RESPONSE_BODY)
        except Exception as e:
            print e
            
            #In the event of an excepion, hard reset both repos so they match the remote (origin) master branches
            self.hard_reset_repos()
            self.do_response(ERROR_RESPONSE_BODY)


    def do_response(self, resBody):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(resBody))
        self.end_headers()
        self.wfile.write(resBody)

    def hard_reset_repos(self):
        source_repo.fetch([source_repo.origin])
        source_repo.reset(['--hard', source_repo.originMaster])
        
        deploy_repo.fetch([deploy_repo.origin])
        deploy_repo.reset(['--hard', deploy_repo.originMaster])

    def nuke_git_cwd(self, git_repo):
        for root, dirs, files in os.walk(git_repo.repoDir):
            #If we are anywhere in the .git directory, then skip this iteration
            if re.match("^.*\.git(/.*)?$", root): continue

            local_path = root.replace(git_repo.repoDir + "/", "")
            local_path = local_path.replace(git_repo.repoDir, "")

            for f in files:
                if local_path not in whitelisted_files:
                    git_repo.rm(['-r', os.path.join(local_path, f)])

httpd = SocketServer.ForkingTCPServer(('', PORT), GitHookRequestHandler)
print "PelicanGit listening on port", PORT
httpd.serve_forever()
