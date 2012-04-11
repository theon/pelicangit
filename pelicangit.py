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

sourceRepo = GitRepo("/work/blog", "origin", "master")
deployRepo = GitRepo("/work/theon.github.com", "origin", "master")

COMMIT_MESSAGE="Auto Blog Rebuild from PelicanGit"

WHITELISTED_FILES = [
    "googled50a97559ea3af0e.html"
]

class GitHookRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.do_response(GET_RESPONSE_BODY)

    def do_POST(self):
        try:
            #Hard reset both repos so they match the remote (origin) master branches
            self.hard_reset_repos()
            
            # Git Remove all deployRepo files (except those whitelisted) and then rebuild with pelican
            self.nukeGitWorkingDir(deployRepo) 
            main()

            # Add all files newly created by pelican, then commit and push everything
            deployRepo.add(['.'])

            deployRepo.commit(COMMIT_MESSAGE, ['-a'])
            deployRepo.push([deployRepo.origin, deployRepo.master])

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
        sourceRepo.fetch([sourceRepo.origin])
        sourceRepo.reset(['--hard', sourceRepo.originMaster])
        
        deployRepo.fetch([deployRepo.origin])
        deployRepo.reset(['--hard', deployRepo.originMaster])

    def nukeGitWorkingDir(self, gitRepo):
        for root, dirs, files in os.walk(gitRepo.repoDir):
            #If we are anywhere in the .git directory, then skip this iteration
            if re.match("^.*\.git(/.*)?$", root): continue

            localPath = root.replace(gitRepo.repoDir + "/", "")
            localPath = localPath.replace(gitRepo.repoDir, "")

            for f in files:
                if localPath not in WHITELISTED_FILES:
                    gitRepo.rm(['-r', os.path.join(localPath, f)])
        

httpd = SocketServer.ForkingTCPServer(('', PORT), GitHookRequestHandler)
print "PelicanGit listening on port", PORT
httpd.serve_forever()
