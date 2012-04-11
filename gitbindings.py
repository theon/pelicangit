import subprocess as sp

class GitRepo:
    def __init__(self, repoDir, origin, master):
        self.repoDir = repoDir
        self.origin = origin
        self.master = master
        self.originMaster = origin + '/' + master 

    def push(self, args):
        gitCommand('push', args)
        
    def commit(self, message, args):
        gitCommand('commit', args.append('-m', '"' + message + '"'))

    def add(self, args):
        gitCommand('add', args)

    def rm(self, args):
        gitCommand('rm', args)
    
    def fetch(self, args):
        gitCommand('fetch', args)
    
    def reset(self, args):
        gitCommand('reset', args)

    def gitCommand(self, firstArg, args):
        gitCommand(self, args.insert(0, firstArg))

    def gitCommand(self, args):
        sp.call(args.insert(0, 'git'), cwd=self.repoDir)