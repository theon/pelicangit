import SocketServer
import SimpleHTTPServer
import os
import re
from pelican import main
from pelicangit.gitbindings import *

GET_RESPONSE_BODY = "<h1>PelicanGit is Running</h1>"
POST_RESPONSE_BODY = "<h1>Pelican Project Rebuilt</h1>"
ERROR_RESPONSE_BODY = "<h1>Error</h1>"

class GitHookServer(SocketServer.TCPServer):
    
    def __init__(self, server_address, handler_class, source_repo, deploy_repo, whitelisted_files):
        self.source_repo = source_repo
        self.deploy_repo = deploy_repo
        self.whitelisted_files = whitelisted_files
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

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
            self.server.deploy_repo.add(['.'])

            commit_message = self.server.source_repo.log(['-n1', '--pretty=format:"%h %B"'])
            self.server.deploy_repo.commit(commit_message, ['-a'])
            self.server.deploy_repo.push([self.server.deploy_repo.origin, self.server.deploy_repo.master])

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
        self.server.source_repo.fetch([self.server.source_repo.origin])
        self.server.source_repo.reset(['--hard', self.server.source_repo.originMaster])
        
        self.server.deploy_repo.fetch([self.server.deploy_repo.origin])
        self.server.deploy_repo.reset(['--hard', self.server.deploy_repo.originMaster])

    def nuke_git_cwd(self, git_repo):
        for root, dirs, files in os.walk(git_repo.repoDir):
            #If we are anywhere in the .git directory, then skip this iteration
            if re.match("^.*\.git(/.*)?$", root): continue

            local_dir = root.replace(git_repo.repoDir + "/", "")
            local_dir = local_dir.replace(git_repo.repoDir, "")

            for f in files:
                local_file = os.path.join(local_dir, f)
                if local_file not in self.server.whitelisted_files:
                    git_repo.rm(['-r', local_file])
