import subprocess as sp

class GitRepo:
    def __init__(self, repoDir, origin, master):
        self.repoDir = repoDir
        self.origin = origin
        self.master = master
        self.originMaster = origin + '/' + master 

    def push(self, args):
        self.gitCommand('push', args)
        
    def commit(self, message, args):
        self.gitCommand('commit', args + ['-m', '"' + message + '"'])

    def add(self, args):
        self.gitCommand('add', args)

    def rm(self, args):
        self.gitCommand('rm', args)
    
    def fetch(self, args):
        self.gitCommand('fetch', args)
    
    def reset(self, args):
        self.gitCommand('reset', args)

    def gitCommand(self, firstArg, args):
        args.insert(0, firstArg)
        self.gitCommandRaw(args)

    def gitCommandRaw(self, args):
        args.insert(0, 'git')
        sp.call(args, cwd=self.repoDir)
