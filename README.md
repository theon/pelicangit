# PelicanGit

PelicanGit is a python script that will automatically build your Pelican powered blog whenever you commit a blog post into git.

The script will start a simple HTTP server. When the server recieves a POST (from a git service hook, indicating you have pushed a new blog post), it will pull from the git repository where you keep you source blog posts (markdown or restructuredtext), run pelican to compile them to HTML and then commit and push that HTML into another git repository (e.g. github pages repo).

## Installing

Prerequisites:

 * Install setuptools [](http://pypi.python.org/pypi/setuptools)
 * Install pip with `curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python` (http://www.pip-installer.org/en/latest/installing.html
 * Install pelican with `sudo pip install pelican` (http://pelican.notmyidea.org/en/2.8/getting_started.html#installing)
 ** Be sure to install markdown if required with `sudo pip install Markdown` and any themes you require with `pelican-themes` 
 * Install gitpython with `sudo easy_install gitpython`

Installing pelicangit:

 * Clone git repo with `git clone git@github.com:theon/pelican-git.git`
 * Set the variables at the top of the script to appropriate values, especially the ones starting SOURCE_GIT and DEPLOY_GIT
 ** TODO: explain what these variables are
 ** TODO: move these variables to a seperate config py file (combine with pelican config file?)
 * Call the script with the same arguments you would call pelican. For example, I call it with `pelicangit.py -s /path/to/pelican.conf.py /path/to/markdown`
 ** *Important:* at the moment you have to call the script with the same user who owns the valid SSH keypair for the git repos 
 ** TODO: Create init.d scripts 