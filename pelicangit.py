#!/usr/bin/python

import SocketServer
import SimpleHTTPServer
import urllib
import os
import shutil
import re
from git import *
from pelican import main

PORT = 8080
GET_RESPONSE_BODY = """<h1>PelicanGit is Running</h1>"""
POST_RESPONSE_BODY = """<h1>Pelican Project Rebuilt</h1>"""
ERROR_RESPONSE_BODY = """<h1>Error</h1>"""

SOURCE_GIT_REPO="/work/blog"
SOURCE_GIT_REMOTE_NAME="origin"
SOURCE_GIT_BRANCH="master"

DEPLOY_GIT_REPO="/work/theon.github.com"
DEPLOY_GIT_REMOTE_NAME="origin"
DEPLOY_GIT_BRANCH="master"

COMMIT_MESSAGE="Auto Blog Rebuild from PelicanGit"

WHITELISTED_FILES = [
    "googled50a97559ea3af0e.html"
]

class GitHookRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.do_response(GET_RESPONSE_BODY)

    def do_POST(self):
        try:
            #TODO: Logging rather than prints
            print "Pulling Source Git Repo." 
            sourceRepo = Repo(SOURCE_GIT_REPO)
            sourceOrigin = sourceRepo.remote(SOURCE_GIT_REMOTE_NAME)
            sourceOrigin.pull(SOURCE_GIT_BRANCH)

            deployRepo = Repo(DEPLOY_GIT_REPO)
            deployIndex = deployRepo.index

            print "Clean Deploy Git Working Directory"
            self.nukeGitWorkingDir(DEPLOY_GIT_REPO, deployIndex)

            print "Running Pelican Build." 
            main()

            #TODO: Check if there are any changes and if we actually need to commit/push. 
            #This is_dirty() check doesn't seem to work 
            #if deployRepo.is_dirty():
            print "Adding new files."
            deployIndex.add(deployRepo.untracked_files)

            print "Commiting Deploy Git Repo."
            deployIndex.commit(COMMIT_MESSAGE)

            print "Pushing Deploy Git Repo"
            deployOrigin = deployRepo.remote(DEPLOY_GIT_REMOTE_NAME)
            deployOrigin.push(DEPLOY_GIT_BRANCH)

            #else:
            #    print "Nothing was pulled from remote source git repo! Not pushing anything to deploy repo."

            self.do_response(POST_RESPONSE_BODY)
        except Exception as e:
            print e
            self.do_response(ERROR_RESPONSE_BODY)


    def do_response(self, resBody):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(resBody))
        self.end_headers()
        self.wfile.write(resBody)

    def nukeGitWorkingDir(self, path, index):
        for root, dirs, files in os.walk(path):
            #If we are anywhere in the .git directory, then skip this iteration
            if re.match("^.*\.git(/.*)?$", root): continue

            localPath = root.replace(path + "/", "")
            localPath = localPath.replace(path, "")

            for f in files:
                if(localPath not in WHITELISTED_FILES)
                    os.unlink(os.path.join(root, f))
                    print os.path.join(localPath, f)
                    index.remove([os.path.join(localPath, f)])
        

httpd = SocketServer.ForkingTCPServer(('', PORT), GitHookRequestHandler)
print "PelicanGit listening on port", PORT
httpd.serve_forever()
