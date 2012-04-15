# pelicangit

pelicangit is a python script that will automatically build your Pelican powered blog whenever you commit a blog post into git.

The script will start a simple HTTP server. When the server recieves a POST (from a git service hook, indicating you have pushed a new blog post in markdown or restructuredtext), it will pull down these updates, run pelican to compile them to HTML and then commit and push the resulting HTML into another git repository (e.g. a github pages repo). This can be especially useful when writing blog posts on a client which cannot run pelican locally (e.g. a chromebook)

*Note: Currently pelicangit only works on unix environments and has only been tested on Ubuntu.* 

Here is an example:
![pelicangit example](http://lh4.googleusercontent.com/-KPeKZ92FhaE/T4IeoedMY_I/AAAAAAAACXE/fSpxiJ_iCwE/s876/PelicanGit.png)

## To Do

 * Submit as a python package [here](http://pypi.python.org/pypi?%3Aaction=submit_form)

## Installing

### Prerequisites:

 * Install [setuptools](http://pypi.python.org/pypi/setuptools)
 * Install [pip](http://www.pip-installer.org/en/latest/installing.html) with `curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python` 
 * Install [pelican](http://pelican.notmyidea.org/en/2.8/getting_started.html#installing) with `sudo pip install pelican`
 ** Be sure to install markdown if required with `sudo pip install Markdown` and any themes you require with `pelican-themes` 
 * Install gitpython with `sudo easy_install gitpython`

### Installing pelicangit:

1) Clone git repo with `git clone git@github.com:theon/pelican-git.git`

Todo: submit as python package so we can instead install with `pip` or `easy_install` 

2) Add these variables to your pelican config file (the file you pass with the `-s` argument to pelican
        
    PELICANGIT_SOURCE_REPO="/path/to/source/markdown/repo"
    PELICANGIT_SOURCE_REMOTE="origin"
    PELICANGIT_SOURCE_BRANCH="master"

    PELICANGIT_DEPLOY_REPO="/path/to/deploy/html/repo"
    PELICANGIT_DEPLOY_REMOTE="origin"
    PELICANGIT_DEPLOY_BRANCH="master"

    PELICANGIT_USER = "ubuntu"
    PELICANGIT_WHITELISTED_FILES = [
        "README.md"
    ]
    
    PELICANGIT_PORT=8080

 * `PELICANGIT_SOURCE_REPO` is the git repo you push new blog articles to in markdown or restructuredtext.
 * `PELICANGIT_DEPLOY_REPO` is the git repo pelicangit will push your HTML converted blog articles to.
 * `PELICANGIT_USER` is the name of the unix user that will be used to run the git and pelican commands. Ensure this user has a valid SSH keypair to pull/push from/to the git repositories.
 * `GIT_WHITELISTED_FILES` is a list of files pelicangit will not delete. By default, pelicangit assumes everything in the `PELICANGIT_DEPLOY_REPO` git repo is the output from pelican, and everytime it runs, it does a `git rm` on all files before regenerating your entire blog. If you have any files in your `PELICANGIT_DEPLOY_REPO` that are not the output from pelican then add them to this whitelist variable. I currently use this for a google webmaster tools verification html file and a github readme file.    
 * `PELICANGIT_PORT` is the port the pelicangit will listen on for the git service hook you will configure in the next step

3) Setup your git hook

The git service hook is the mechanism which informs pelicangit whenever you commit content (markdown/restructuredtext) to your `PELICANGIT_SOURCE_REPO` and gets it to kick off pelican. 
For github:

 * Go to your github repo where you keep your source markdown (i.e. the `PELICANGIT_SOURCE_REPO` you set in step 2)
 * Click the 'Administration' button
 * Click 'Service Hooks' from the left hand nav
 * Click 'Post-Receive URLs' service hook
 * Add the URL/IP of the server you are running pelicangit. Note pelicangit currently runs on port 8080 (todo: make this configurable)
 * Once you have pelicangit running (see instructions below) you can use the 'Test Hook' button to check the hook is working 

### Running pelicangit

#### Running Directly

Call the pelicangit.py script with the same arguments you would call pelican. For example, for my blog I would call it with `pelicangit.py -s /path/to/pelican.conf.py /path/to/markdown`

#### Running with Upstart

Upstart will keep pelicangit long running (will restart it if it crashes, or the machine reboots).
This git repo contains an upstart config I have used on ubuntu running in Amazon EC2.

*Note: Even if upstart runs pelicangit as the root user, pelican git will change to the unix user sepcified by the `PELICANGIT_USER` variable to run git and pelican commands* 

 * Update the upstart/pelicangit.conf `exec` line to use your pelicangit command.
 * Copy upstart/pelicangit.conf to /etc/init/
 * Run `sudo start pelicangit`

## Logging

If you need to do any debugging, logs currently live at `/home/${PELICANGIT_USER}/pelicangit.log` where `PELICANGIT_USER` is the variable specified in your pelican config file. 

## Also See

[Blog article](http://theon.github.com/powering-your-blog-with-pelican-and-git.html)