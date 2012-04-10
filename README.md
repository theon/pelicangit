# PelicanGit

PelicanGit is a python script that will automatically build your Pelican powered blog whenever you commit a blog post into git.

The script will start a simple HTTP server. When the server recieves a POST (from a git service hook, indicating you have pushed a new blog post in markdown or restructuredtext), it will pull down these updates, run pelican to compile them to HTML and then commit and push the resulting HTML into another git repository (e.g. a github pages repo).

## To Do

 * Add the ability to whitelist files to keep (at the moment any files not created by pelican get whacked during a build).
 * Move the variables in the script so that they live in with the standard pelican config file? Also explain these variables in more detail in these docs.
 * Copy the commit message(s) from the source repo (containing the markdown) and use it when commiting the resulting HTML to the deploy repo.

## Installing

### Prerequisites:

 * Install [setuptools](http://pypi.python.org/pypi/setuptools)
 * Install [pip](http://www.pip-installer.org/en/latest/installing.html with) `curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python` 
 * Install [pelican](http://pelican.notmyidea.org/en/2.8/getting_started.html#installing) with `sudo pip install pelican`
 ** Be sure to install markdown if required with `sudo pip install Markdown` and any themes you require with `pelican-themes` 
 * Install gitpython with `sudo easy_install gitpython`

### Installing pelicangit:

 * Clone git repo with `git clone git@github.com:theon/pelican-git.git`
 * Set the variables at the top of the script to appropriate values, especially the ones starting SOURCE_GIT and DEPLOY_GIT

#### Running Directly

 * Call the script with the same arguments you would call pelican. For example, I call it with `pelicangit.py -s /path/to/pelican.conf.py /path/to/markdown`
 ** *Important:* at the moment you have to call the script with the same user who owns the valid SSH keypair for the git repos

#### Running with Upstart

Upstart will keep pelican git long running (restart it if it crashed, or the machine reboots).
This git repo has an upstart config I have used on ubuntu running in Amazon EC2.

 * Update the upstart/pelicangit.conf `exec` line to use your pelican command. Only replace stuff after the double hyphen.
 * Update the upstart/pelicangit.conf `exec` line to run pelicangit as the user you want. Currently runs as user `ubuntu`.
 * Copy upstart/pelicangit.conf to /etc/init/
 * Run `sudo start pelicangit`

## Also See

[Blog article explaining why I created this script](http://theon.github.com/powering-your-blog-with-pelican-and-git.html)