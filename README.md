# PelicanGit

PelicanGit is a python script that will automatically build your Pelican powered blog whenever you commit a blog post into git.

The script will start a simple HTTP server. When the server recieves a POST (from a git service hook, indicating you have pushed a new blog post), it will pull from the git repository where you keep you source blog posts (markdown or restructuredtext), run pelican to compile them to HTML and then commit and push that HTML into another git repository (e.g. github pages repo).
